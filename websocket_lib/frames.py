"""
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-------+-+-------------+-------------------------------+
 |F|R|R|R| opcode|M| Payload len |    Extended payload length    |
 |I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
 |N|V|V|V|       |S|             |   (if payload len==126/127)   |
 | |1|2|3|       |K|             |                               |
 +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
 |     Extended payload length continued, if payload len == 127  |
 + - - - - - - - - - - - - - - - +-------------------------------+
 |                               |Masking-key, if MASK set to 1  |
 +-------------------------------+-------------------------------+
 | Masking-key (continued)       |          Payload Data         |
 +-------------------------------- - - - - - - - - - - - - - - - +
 :                     Payload Data continued ...                :
 + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
 |                     Payload Data continued ...                |
 +---------------------------------------------------------------+
"""

from websocket_lib.exceptions import FrameNotMaskedException
from websocket_lib.status_code import StatusCode


class Frames(object):

    def close_frame(self, status_code, reason=""):
        # Reason example: endpoint shutting down, endpoint recieved a frame too large, endpoint recieved a frame that does not conform to the format expected
        if not isinstance(status_code, StatusCode):
            raise TypeError('status_code must be an instance of StatusCode Enum')

        #message = str(str(status_code.name) + " Reason: " + reason)
        message = reason
        return self.encode_message(str(message), "1000", status_code.value)

    def continuation_frame(self, message):
        return self.encode_message(message, "0000")

    def binary_frame(self, message):
        return self.encode_message(message, "0010")

    def text_frame(self, message):
        return self.encode_message(message, "0001")

    def ping_frame(self, message):
        return self.encode_message(message, "1001")

    def pong_frame(self, message):
        return self.encode_message(message, "1010")

    # Encode message from server
    def encode_message(self, message, opcode, status_code=0):
        #if len(message) == 0: #TODO: FIX THIS
        #    return -1
        fin = "1"
        rsv1 = "0"
        rsv2 = "0"
        rsv3 = "0"
        byte_list = []
        if not status_code == 0:
            #test = bytes(int(status_code))
            message_bytes = status_code.to_bytes(2, byteorder='big') + bytes(message, "ascii")
            print(status_code.to_bytes(2, byteorder='big'))
            print(message_bytes)
        else:
            message_bytes = bytes(message, "ascii")
        message_length = len(message_bytes)
        byte_list.append((int(fin + rsv1 + rsv2 + rsv3 + opcode, 2)))

        if message_length <= 125:
            byte_list.append(message_length)

        elif 126 <= message_length <= 65535:
            byte_list.append(126)
            byte_list.append((message_length >> 8) & 255)
            byte_list.append(message_length & 255)

        else:
            byte_list.append(127)
            byte_list.append((message_length >> 56) & 255)
            byte_list.append((message_length >> 48) & 255)
            byte_list.append((message_length >> 40) & 255)
            byte_list.append((message_length >> 32) & 255)
            byte_list.append((message_length >> 24) & 255)
            byte_list.append((message_length >> 16) & 255)
            byte_list.append((message_length >> 8) & 255)
            byte_list.append(message_length & 255)

        byte_list = bytes(byte_list)
        byte_list = byte_list + message_bytes
        return byte_list

    # Decode message from client
    def decode_message(self, message):
        try:
            masked = (int(message[1]))

            if masked <= 127: #TODO: test this
                print("errorrrr")
                raise FrameNotMaskedException

            decoded_message = []
            mask_start = 2
            if message[1] == 126:
                mask_start = 4
            if message[1] == 127:
                mask_start = 10

            data_start = mask_start + 4
            # [m for m in message[mask_start:data_start]]
            masks = message[mask_start:data_start]

            j = 0
            while data_start < len(message):
                decoded_message.append(chr(message[data_start] ^ masks[j%4]))
                data_start += 1
                j += 1

            return ''.join(decoded_message) #TODO: add extra return value
        except FrameNotMaskedException as e:
            print("frame exc") #TODO: print exception
            # TODO: The server MUST close the connection upon receiving a
            # TODO: frame that is not masked.  In this case, a server MAY send a Close
            # TODO: frame with a status code of 1002 (protocol error)
