import socket

from websocket_lib.utilities import Utilities


class ClientSocket(object):
    handshake_done = False
    handshake_template = "HTTP/1.1 101 Switching Protocols\r\n" \
                         "Upgrade: Websocket\r\n" \
                         "Connection: Upgrade\r\n" \
                         "Sec-WebSocket-Accept: {}\r\n\r\n"

    def __init__(self, socket):
        self.socket = socket

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
