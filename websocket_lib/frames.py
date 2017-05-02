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
from websocket_lib.exceptions import CloseFrameTooLongException
from websocket_lib.status_code import StatusCode
from websocket_lib.opcode import Opcode


class Frames(object):

    def encode_frame(self, opcode, message="", status_code=None):
        try:
            if not isinstance(opcode, Opcode):
                raise TypeError('status_code must be an instance of StatusCode Enum')

            encoded_frames = []
            message_length = len(message)
            max_length_frame = 65535

            if message_length > max_length_frame:
                fin = 0
                if opcode == Opcode.CONNECTION_CLOSE_FRAME:
                    raise CloseFrameTooLongException
                encoded_frames.append(self.__encode_message(opcode, message[0:max_length_frame], status_code, fin))
                length_used = max_length_frame
                opcode = Opcode.CONTINUATION_FRAME
                while not length_used == message_length:
                    if (message_length - length_used) > max_length_frame:
                        encoded_frames.append(
                            self.__encode_message(opcode, message[length_used:(length_used + max_length_frame)],
                                                  status_code, fin))
                        length_used += max_length_frame

                    else:
                        fin = 128
                        encoded_frames.append(
                            self.__encode_message(opcode, message[length_used:(message_length + 1)], status_code, fin))
                        length_used = message_length

                return encoded_frames

            else:
                fin = 128
            if opcode == Opcode.CONNECTION_CLOSE_FRAME:  # TODO: ex if fin = 0, close is one frame
                if status_code is None:
                    encoded_frames.append(self.__encode_message(opcode, message, status_code, fin))
                    return encoded_frames
                else:
                    if not isinstance(status_code, StatusCode):
                        raise TypeError('status_code must be an instance of StatusCode Enum')
                    message = str(str(status_code.name) + " " + message)
                    encoded_frames.append(self.__encode_message(opcode, message, status_code, fin))
                    return encoded_frames
            encoded_frames.append(self.__encode_message(opcode, message, status_code, fin))
            return encoded_frames
        except CloseFrameTooLongException as e:
            print("CloseFrameTooLongException: the close frame can not be fragmented")
            print(e)
            return e, None
        except TypeError as e:
            print(e)
            return e, None


    # Encode message from server
    def __encode_message(self, opcode, message, status_code, fin):
        rsv1 = 0
        rsv2 = 0
        rsv3 = 0
        byte_list = []
        if not (status_code is None):
            #message_bytes = b'1001' + bytes(message, "ascii")
            #message_bytes = b'0000001111101001' + bytes(message, "ascii")
            #message_bytes = 0x000003E9.to_bytes(2, byteorder='big') + bytes(message, "ascii")
            #message_bytes = ((status_code.value >> 8) + (status_code.value % 256)).to_bytes(2, byteorder='big') + bytes(message, "ascii")
            message_bytes = 0x000003E9.to_bytes(2, byteorder='big') + bytes(message, "ascii")

            #print(status_code.value.to_bytes(2, byteorder='big'))
        else:
            message_bytes = bytes(message, "ascii")

        message_length = len(message_bytes)
        byte_list.append(fin + rsv1 + rsv2 + rsv3 + opcode.value)

        if message_length <= 125:
            byte_list.append(message_length)

        elif 126 <= message_length <= 65535:
            byte_list.append(126)
            byte_list.append((message_length >> 8) & 255)
            byte_list.append(message_length & 255)

        else:
            print("Frame capacity error")
            """
            byte_list.append(127)
            byte_list.append((message_length >> 56) & 255)
            byte_list.append((message_length >> 48) & 255)
            byte_list.append((message_length >> 40) & 255)
            byte_list.append((message_length >> 32) & 255)
            byte_list.append((message_length >> 24) & 255)
            byte_list.append((message_length >> 16) & 255)
            byte_list.append((message_length >> 8) & 255)
            byte_list.append(message_length & 255)"""

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
                    opcode = Opcode(opcode)
                    if not isinstance(opcode, Opcode):
                        raise TypeError('opcode must be an instance of Opcode Enum')

                else:
                    print("RSV1, RSV2 eller RSV3 er lik 1")
                    opcode = -2

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

            return ''.join(decoded_message), opcode
        except FrameNotMaskedException as e:
            print("FrameNotMaskedException: ")
            print(e)
            return e, None


#TODO: exept. for non cont frame if fin = 0