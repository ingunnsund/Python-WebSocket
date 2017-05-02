from socket import error as socketerror
from threading import Thread

from websocket_lib.utilities import Utilities
from websocket_lib.frames import Frames
from websocket_lib.status_code import StatusCode
from websocket_lib.opcode import Opcode
from websocket_lib.state import State
from websocket_lib.exceptions import FrameNotMaskedException
from websocket_lib.exceptions import ExtensionException


class ClientSocket(Thread):
    BUFFER_SIZE = 1024

    def __init__(self, socket, address, websocket, state=State.CONNECTING):
        super().__init__()
        self.socket = socket
        self.address = address
        self.websocket = websocket
        self.state = state
        self.frame = Frames()
        self.message_list = []

    def run(self):
        """
        Overrided method in the Thread class and run the receiving in the socket class threaded.
        """

        # While the state is not CLOSED, the socket receive bytes and we check the received package
        while not self.state == State.CLOSED:
            try:
                received_bytes = self.receive(self.BUFFER_SIZE)
                if not received_bytes:
                    break

                # Check what state the client is in and then choose what to do with the received data
                if self.state == State.OPEN:
                    message_from_client, current_op_code, fin = self.frame.decode_message(received_bytes)

                    self.do_opcode_operation(message_from_client, current_op_code, fin)
                    # TODO: check if message is a MESSAGE or a ping/pong
                    # self.send(frame.encode_frame(Opcode.CONNECTION_CLOSE_FRAME, "Hei", StatusCode.CLOSE_GOING_AWAY))
                    # self.state = State.CLOSING


                    # TODO: exept. for non cont frame if fin = 0

                elif self.state == State.CONNECTING:
                    # If the client is in connecting state then it first sends a handshake
                    received_headers = received_bytes.decode()
                    if Utilities.check_correct_handshake(received_headers):
                        sec_websocket_key = received_headers.split("Sec-WebSocket-Key: ")[1].split("\r\n")[0]
                        self.do_handshake(sec_websocket_key)
                    else:
                        self.__send_bytes(Utilities.NOT_CORRECT_HANDSHAKE)
                        print("The request from the client is not a correct handshake")
                        self.close_and_remove()
                elif self.state == State.CLOSING:
                    message_from_client, current_op_code, fin = self.frame.decode_message(received_bytes)
                    # If the client is in CLOSING state and is receiving a CLOSE frame, then it can safely close itself.
                    if current_op_code == Opcode.CONNECTION_CLOSE_FRAME:
                        self.close_and_remove()

            except socketerror as e:
                print("Error: ")
                print(e)
                self.close_and_remove()
            except FrameNotMaskedException as fnme:
                print("FrameNotMaskedException: ")
                print(fnme)
                frame = Frames()
                self.__send_frames(self.frame.encode_frame(Opcode.CONNECTION_CLOSE_FRAME, "Frame was not masked",
                                    StatusCode.CLOSE_PROTOCOL_ERROR))
                self.close_and_remove()
            except ExtensionException as e:
                print("ExtensionException: ")
                print(e)
                frame = Frames()
                self.__send_frames(self.frame.encode_frame(Opcode.CONNECTION_CLOSE_FRAME, "Extension Exception",
                                    StatusCode.CLOSE_PROTOCOL_ERROR))

                self.close_and_remove()

    def do_opcode_operation(self, current_message, current_opcode, fin):
        if current_opcode == Opcode.TEXT_FRAME:  # or Opcode.BINARY_FRAME
            print("TEXT")
            if fin is False:
                self.message_list.append(current_message)
            else:
                self.websocket.on_message(current_message, self)

        elif current_opcode == Opcode.BINARY_FRAME:
            print("BINARY")
            if fin is False:
                self.message_list.append(current_message)
            else:
                self.websocket.on_message(current_message, self)

        elif current_opcode == Opcode.CONNECTION_CLOSE_FRAME:
            self.state = State.CLOSING

            # TODO: FIX THIS
            # self.send(self.frame.encode_frame(Opcode(current_opcode), current_message))
            self.__send_frames(self.frame.encode_frame(Opcode(current_opcode), "", StatusCode.CLOSE_NORMAL))
            self.close_and_remove()

        elif current_opcode == Opcode.CONTINUATION_FRAME:
            if fin is False:
                self.message_list.append(current_message)
            else:
                self.message_list.append(current_message)
                self.websocket.on_message(''.join(self.message_list), self)
                self.message_list = []

        elif current_opcode == Opcode.PING_FRAME:
            self.__send_frames(self.frame.encode_frame(Opcode.PONG_FRAME, current_message))

        elif current_opcode == Opcode.PONG_FRAME:
            print("PONG_FRAME")

    def close_and_remove(self):
        """
        Method for easier closing of the clients socket and then removing it from the websockets list of clients
        """
        self.state = State.CLOSED
        self.websocket.clients.remove(self)
        self.close()

    def receive(self, buffer_size):
        return self.socket.recv(buffer_size)

    # def send(self, message):

    def __send_bytes(self, message_bytes):
        self.socket.send(message_bytes)

    def __send_frames(self, message):
        for frame in message:
            self.socket.send(frame)

    def send(self, message):
        if isinstance(message, str):
            self.__send_frames(self.frame.encode_frame(Opcode.TEXT_FRAME, message))
        else:
            self.__send_frames(self.frame.encode_frame(Opcode.BINARY_FRAME, message))

    def close(self):
        """
        Method for closing the clients socket and calling the websockets method on_close so that the library can be
        overrided in an extended class and used easier 
        """
        # TODO: check if already closed
        # TODO: check if connecting
        self.websocket.on_close(self)
        self.socket.close()

    def do_handshake(self, sec_websocket_key):
        """
        Method for doing a handshake with the client. It uses the Utilities class to make a accept key and then sends
        the handshake with its headers created from the static variable handshake_template
        :param sec_websocket_key: is the "Sec-WebSocket-Key" from the header that is sent from the client
        """
        sec_websocket_accept = Utilities.make_accept_key(sec_websocket_key)

        handshake_format = Utilities.handshake_template.format(sec_websocket_accept, "")
        if (not self.websocket.extension == "") and (not self.websocket.rsv_number_extension == 0):
            extension = "\r\nSec-WebSocket-Extensions: " + self.websocket.extension
            handshake_format = Utilities.handshake_template.format(sec_websocket_accept, extension)

            if self.websocket.rsv_number_extension == 1:
                self.frame = Frames(rsv1_extension=True)
            elif self.websocket.rsv_number_extension == 2:
                self.frame = Frames(rsv2_extension=True)
            elif self.websocket.rsv_number_extension == 3:
                self.frame = Frames(rsv3_extension=True)
            else:
                handshake_format = Utilities.handshake_template.format(sec_websocket_accept, "")

        handshake_response = str.encode(handshake_format)
        self.__send_bytes(handshake_response)
        self.state = State.OPEN
        # The clients state is set to OPEN if the handshake is completed correctly
