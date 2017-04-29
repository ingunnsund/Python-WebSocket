from hashlib import sha1
from base64 import b64encode


class Utilities(object):

    @staticmethod
    def make_accept_key(sec_key):
        GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        total_key = sec_key + GUID

        hash_key = sha1(total_key.encode()).digest()
        new_accept_key = b64encode(hash_key).decode()
        return new_accept_key
