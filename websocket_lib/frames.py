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
from websocket_lib.opcode import Opcode


class Frames(object):

    def close_frame(self, status_code, reason=""):
        # Reason example: endpoint shutting down, endpoint recieved a frame too large, endpoint recieved a frame that does not conform to the format expected
        if not isinstance(status_code, StatusCode):
            raise TypeError('status_code must be an instance of StatusCode Enum')

        message = str(str(status_code.name) + " Reason: " + reason)
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
        if len(message) == 0:
            return -1
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

        elif message_length >= 126 and message_length <= 65535:
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

    # TODO: 0x37 0xfa 0x21 0x3d 0x7f 0x9f 0x4d -> \x37 osv


    # Decode message from client
    def decode_message(self, message):
        try:
            masked = (int(message[1]))
            if masked <= 127: #TODO: test this
                print("Frame from client is not masked")
                raise FrameNotMaskedException

            first_byte = int(message[0])

            if first_byte < 128: # FIN = 0
                print("Not fin") #TODO: legg inn fragmented frames
                opcode = -1
            else:
                if first_byte <= 143: # RSV1 = RSV2 = RSV3 = 0
                    opcode = first_byte-128
                    print(opcode)
                    opcode = Opcode(opcode)
                    if not isinstance(opcode, Opcode):
                        raise TypeError('opcode must be an instance of Opcode Enum')

                else:
                    print("RSV1, RSV2 eller RSV3 er lik 1")
                    opcode = -2


            print(bin(message[0]))
            decoded_message = []
            mask_start = 2
            if message[1] == 126:
                mask_start = 4
            if message[1] == 127:
                mask_start = 10


            data_start = mask_start + 4
            masks = message[mask_start:data_start] #[m for m in message[mask_start:data_start]]

            j = 0
            while data_start < len(message):
                decoded_message.append(chr(message[data_start] ^ masks[j%4]))
                data_start += 1
                j += 1

            return ''.join(decoded_message), opcode
        except FrameNotMaskedException as e:
            print("FrameNotMaskedException: ")
            print(e)
            return e, None


#TODO: exept. for non cont frame if fin = 0