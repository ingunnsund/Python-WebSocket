from socket import error as socketerror
from threading import Thread

from websocket_lib.utilities import Utilities
from websocket_lib.frames import Frames
from websocket_lib.status_code import StatusCode
from websocket_lib.opcode import Opcode
from websocket_lib.state import State


class ClientSocket(Thread):
    handshake_template = "HTTP/1.1 101 Switching Protocols\r\n" \
                         "Upgrade: Websocket\r\n" \
                         "Connection: Upgrade\r\n" \
                         "Sec-WebSocket-Accept: {}\r\n\r\n"
    BUFFER_SIZE = 1024
    NOT_CORRECT_HANDSHAKE = str.encode("HTTP/1.1 426 Upgrade Required\r\n"
                                       + "Content-Type: text/html\r\n"
                                       + "\r\n"
                                       + "<html><body>\r\n"
                                       + "<pre>Upgrade Required</pre>\r\n"
                                       + "</body></head>\r\n\r\n")

    def __init__(self, socket, address, websocket, state=State.CONNECTING):
        super().__init__()
        self.socket = socket
        self.address = address
        self.websocket = websocket
        self.state = state

    def run(self):
        while not self.state == State.CLOSED:
            try:
                received_bytes = self.receive(self.BUFFER_SIZE)
                if not received_bytes:
                    break

                if self.state == State.OPEN:
                    frame = Frames()
                    message_from_client, current_op_code = frame.decode_message(received_bytes)

                    #message = "1234567" * 10000
                    message2 = "1122334" * 20000
                    #framess = frame.encode_frame(Opcode.TEXT_FRAME, message)
                    framesss = frame.encode_frame(Opcode.TEXT_FRAME, message2)
                    #for frame1 in framess:
                    #    print(frame1)
                    #    self.send(frame1)
                    for frame2 in framesss:
                        print(frame2)
                        self.send(frame2)
                    self.state = State.TIME_WAIT
                    #TODO: check if message is a MESSAGE or a ping/pong
                    #self.send(frame.encode_frame(Opcode.CONNECTION_CLOSE_FRAME, "Hei", StatusCode.CLOSE_GOING_AWAY))
                    #self.state = State.CLOSING

                    if current_op_code == Opcode.CONNECTION_CLOSE_FRAME:
                        #self.send() #TODO: send en frame med closing tilbake
                        #self.state = State.CLOSED
                        print("CONNECTION_CLOSED")
                        self.close_and_remove()

                    if current_op_code == Opcode.TEXT_FRAME: # or Opcode.BINARY_FRAME
                        self.websocket.on_message(message_from_client, self)

                    #TODO: if ping from client -> send pong, if ping(client) and close(client) -> do not send pong, send close
                    #TODO: if ping(client) + ping(client) -> send one pong (not required, not important)

                    #TODO: if message from client = not masked -> decode_message will return FrameNotMaskedException, None
                    #TODO: ^ send close frame with status code: 1002 PROTOCOL_ERROR and close connection
                    #TODO: try/catch?

                    # Send a close frame test:
                    #self.send(frame.close_frame(StatusCode.CLOSE_NORMAL, "Test"))
                    ##self.send(frame.close_frame(StatusCode.CLOSE_GOING_AWAY, "Test"))
                    #self.send(frame.ping_frame("Hello"))
                    #self.send(frame.close_frame(StatusCode.CLOSE_NORMAL, "TEST"))
                    #self.state = State.CLOSING


                    # TODO: exept. for non cont frame if fin = 0

                elif self.state == State.CONNECTING:
                    # If the client is in connecting state then it first sends a handshake
                    received_headers = received_bytes.decode()
                    if Utilities.check_correct_handshake(received_headers):
                        sec_websocket_key = received_headers.split("Sec-WebSocket-Key: ")[1].split("\r\n")[0]
                        self.do_handshake(sec_websocket_key)
                    else:
                        self.send(self.NOT_CORRECT_HANDSHAKE)
                        print("The request from the client is not a correct handshake")
                        self.close_and_remove()
                elif self.state == State.CLOSING:
                    #frame = Frames()
                    #print(frame.decode_message(received_bytes))
                    print("CLOSING")
                    #self.send(received_bytes)

            except socketerror as e:
                #TODO: check om denne må bytte om navnene
                print("Error: ")
                # TODO: print e?
                # TODO: Check type of error and then check if it is needed to close the client
                self.close_and_remove()

    def close_and_remove(self):
        self.state = State.CLOSED
        self.websocket.clients.remove(self)
        self.close()

    def receive(self, buffer_size):
        return self.socket.recv(buffer_size)

    #def send(self, message):

    def send(self, message):
        self.socket.send(message)

    def close(self):
        # TODO: check if already closed
        # TODO: check if connecting
        self.websocket.on_close(self)
        self.socket.close()

    def do_handshake(self, sec_websocket_key):
        sec_websocket_accept = Utilities.make_accept_key(sec_websocket_key)
        handshake_response = str.encode(self.handshake_template.format(sec_websocket_accept))

        self.send(handshake_response)
        self.state = State.OPEN
