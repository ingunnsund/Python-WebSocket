import socket
from threading import Thread

from websocket_lib.utilities import Utilities


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
                    print("has handshaked")
                    # TODO: do stuff with message/frames?
                    print(received_bytes)
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
