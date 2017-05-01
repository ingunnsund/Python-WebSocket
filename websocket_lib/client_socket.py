import socket
from threading import Thread

from websocket_lib.utilities import Utilities
from websocket_lib.frames import Frames
from websocket_lib.status_code import StatusCode
from websocket_lib.opcode import Opcode


class ClientSocket(Thread):
    handshake_done = False
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
    close_sent = False

    def __init__(self, socket):
        super().__init__()
        self.socket = socket

    def run(self):
        # Change this
        while True:
            try:
                received_bytes = self.receive(self.BUFFER_SIZE)
                if not received_bytes:
                    break

                if self.handshake_done:
                    frame = Frames()
                    message_from_client = frame.decode_message(received_bytes)
                    print("Message from client: ", message_from_client)
                    #self.send(frame.encode_message("Hei tilbake"))
                    #self.send(frame.text_frame("test"))



                    if not self.close_sent:
                        print("test")
                        self.send(frame.encode_frame(Opcode.CONNECTION_CLOSE_FRAME, "Test", StatusCode.CLOSE_GOING_AWAY))
                        self.close_sent = True
                    #self.send(frame.encode_message("test", "0001"))
                    #self.send(frame.encode_frame(Opcode.TEXT_FRAME, "Test knuti"))


                    #TODO: if message from client = not masked -> decode_message will return FrameNotMaskedException, None
                    #TODO: ^ send close frame with status code: 1002 PROTOCOL_ERROR and close connection
                    #TODO: try/catch?
                else:
                    received_headers = received_bytes.decode()
                    if Utilities.check_correct_handshake(received_headers):
                        sec_websocket_key = received_headers.split("Sec-WebSocket-Key: ")[1].split("\r\n")[0]

                        self.do_handshake(sec_websocket_key)
                        # close_down = True
                    else:
                        self.send(self.NOT_CORRECT_HANDSHAKE)
                        print("The request from the client is not a correct handshake")
                        self.close()

            except socket.error as e:
                print("Error: ")
                # TODO: print e?
                # TODO: Check type of error and then check if it is needed to close the client
                self.close()

    def receive(self, buffer_size):
        return self.socket.recv(buffer_size)

    def send(self, message):
        self.socket.send(message)

    def close(self):
        self.socket.close()

    def do_handshake(self, sec_websocket_key):
        sec_websocket_accept = Utilities.make_accept_key(sec_websocket_key)
        handshake_response = str.encode(self.handshake_template.format(sec_websocket_accept))

        self.send(handshake_response)
        self.handshake_done = True
