from hashlib import sha1
from base64 import b64encode


class Utilities(object):
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    MINIMUM_HTTP_VERSION = 1.1

    @staticmethod
    def make_accept_key(sec_key):
        total_key = sec_key + Utilities.GUID

        hash_key = sha1(total_key.encode()).digest()
        new_accept_key = b64encode(hash_key).decode()
        return new_accept_key

    @staticmethod
    def check_correct_handshake(client_handshake):
        # The opening handshake must be a GET request and be at least HTTP 1.1
        if not client_handshake.find("GET /") >= 0:
            return False
        if not client_handshake.find("HTTP/") >= 0:
            return False
        else:
            http_version = float(client_handshake.split("HTTP/")[1].split("\n")[0])
            if not http_version >= Utilities.MINIMUM_HTTP_VERSION:
                return False

        # The opening handshake must also include some HTTP headers:
        if not client_handshake.find("Host: ") >= 0:
            return False
        if not client_handshake.find("Upgrade: ") >= 0:
            # TODO: check if CONTAINING: websocket keyword
            return False
        if not client_handshake.find("Connection: ") >= 0:
            return False
        if not client_handshake.find("Sec-WebSocket-Version: 13") >= 0:
            return False

        # Returning True if all checks fails
        return True
