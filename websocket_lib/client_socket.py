import socket


class ClientSocket(object):

    has_handshaked = False

    def __init__(self, socket):
        self.socket = socket

    def do_handshake(self):
        self.has_handshaked = True
