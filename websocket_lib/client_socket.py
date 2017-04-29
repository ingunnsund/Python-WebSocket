import socket


class ClientSocket(object):

    has_handshaked = False

    def __init__(self, socket):
        self.socket = socket

