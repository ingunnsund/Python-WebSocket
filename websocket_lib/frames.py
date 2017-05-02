""" Illustration of frames (from https://tools.ietf.org/html/rfc6455)
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
from websocket_lib.exceptions import ExtensionException
from websocket_lib.exceptions import TooLongMaxFrameException
from websocket_lib.status_code import StatusCode
from websocket_lib.opcode import Opcode


class Frames(object):

    def __init__(self, max_length_frame=65535, rsv1_extension=False, rsv2_extension=False, rsv3_extension=False):
        try:
            if max_length_frame > 16777215:           # 3 bytes
                raise TooLongMaxFrameException("Too long max length for frame")
            self.max_length_frame = max_length_frame
            self.rsv1_extension = rsv1_extension
            self.rsv2_extension = rsv2_extension
            self.rsv3_extension = rsv3_extension
        except TooLongMaxFrameException as e:
            print("TooLongMaxFrameException")
            print(e)

    def encode_frame(self, opcode, message="", status_code=None, rsv1=0, rsv2=0, rsv3=0):
        """
        This function encodes a frame from server to client
        :param opcode: Enum of frame types 
        :param message: Message sent with frame, default: message=""
        :param status_code: Enum of status codes for close frame, default: status_code=None
        :param rsv1: Extension
        :param rsv2: Extension
        :param rsv3: Extension
        :return: the function returns a list of encoded frames (encoded_frames)
        """
        try:
            if not isinstance(opcode, Opcode):
                raise TypeError('status_code must be an instance of StatusCode Enum')

            encoded_frames = []
            message_length = len(message)

            if message_length > self.max_length_frame:          # Check if the frame should be fragmented
                fin = 0                                         # FIN = 0
                if opcode == Opcode.CONNECTION_CLOSE_FRAME:     # Close frames can not ble fragmented
                    raise CloseFrameTooLongException
                encoded_frames.append(
                    self.__encode_message(opcode, message[0:self.max_length_frame], status_code, fin,
                                          rsv1, rsv2, rsv3))    # Adding first full frame to encoded_frames
                length_used = self.max_length_frame                  # length_used is a variable to keep track of how much of the message is framed
                opcode = Opcode.CONTINUATION_FRAME              # Set opcode to continuation frame
                while not length_used == message_length:        # while the whole message is not framed
                    if (message_length - length_used) > self.max_length_frame:   # if a whole frame can be filled up with the message
                        encoded_frames.append(
                            self.__encode_message(opcode, message[length_used:(length_used + self.max_length_frame)],
                                                  status_code, fin, rsv1, rsv2, rsv3))
                        length_used += self.max_length_frame

                    else:                                       # if one frame is enough to fit what is left of the message
                        fin = 128                               # FIN = 1
                        encoded_frames.append(
                            self.__encode_message(opcode, message[length_used:(message_length + 1)], status_code, fin,
                                                  rsv1, rsv2, rsv3))
                        length_used = message_length

                return encoded_frames
            else:
                fin = 128                                       # Not a fragmented frame, FIN = 1

            if opcode == Opcode.CONNECTION_CLOSE_FRAME:         # if the frame is a close frame
                if status_code is None:                         # if there is no status code
                    encoded_frames.append(self.__encode_message(opcode, message, status_code, fin, rsv1, rsv2, rsv3))
                    return encoded_frames
                else:
                    if not isinstance(status_code, StatusCode): # if the status code is not a valid status code from the StatusCode Enum
                        raise TypeError('status_code must be an instance of StatusCode Enum')
                    message = str(str(status_code.name) + " " + message)    # message = reason from the status code + message
                    encoded_frames.append(self.__encode_message(opcode, message, status_code, fin, rsv1, rsv2, rsv3))
                    return encoded_frames
            else:
                if not status_code is None:                     # Frame that is not a close frame should not have a status code
                    status_code = None
                encoded_frames.append(self.__encode_message(opcode, message, status_code, fin, rsv1, rsv2, rsv3))
                return encoded_frames
        except CloseFrameTooLongException as e:
            print("CloseFrameTooLongException: the close frame can not be fragmented")
            print(e)
            return e, None
        except TypeError as e:
            print(e)
            return e, None

    def __check_extension(self, rsv1, rsv2, rsv3):
        try:
            if (not rsv1 == 0) and self.rsv1_extension == False:
                raise ExtensionException("rsv1 can not be 1 if no extension is added")
            if (not rsv2 == 0) and self.rsv2_extension == False:
                raise ExtensionException("rsv1 can not be 1 if no extension is added")
            if (not rsv3 == 0) and self.rsv3_extension == False:
                raise ExtensionException("rsv1 can not be 1 if no extension is added")

            return True
        except ExtensionException as e:
            print("ExtensionException")
            print(e)
            return False

    def __encode_message(self, opcode, message, status_code, fin, rsv1, rsv2, rsv3):
        """
        "Private" help function for the encode_frame function 
        :param opcode: Enum of frame types 
        :param message: Message sent with frame
        :param status_code: Enum of status codes for close frame
        :param fin: if the frame is the last frame sent (fragmentation)
        :param rsv1: Extension
        :param rsv2: Extension
        :param rsv3: Extension
        :return: the method returns byte_list: the frame in bytes
        """
        try:
            if not self.__check_extension(rsv1, rsv2, rsv3):                # Check if rsv is 1 when no extension is added
                raise ExtensionException("rsv1/rsv2/rsv3 can not be 1 if no extension is added")
            if rsv1 == 1:                                                   # Change to correct value
                rsv1 = 64
            if rsv2 == 1:                                                   # Change to correct value
                rsv2 = 32
            if rsv3 == 1:                                                   # Change to correct value
                rsv3 = 16

            byte_list = []
            if not (status_code is None):                                   # if the frame is a close frame
                message_bytes = status_code.value.to_bytes(2, byteorder='big') + bytes(message, "ascii")
            else:
                if isinstance(message, str):
                    #message_bytes = bytes(message)#, "ascii")
                    message_bytes = message.encode()                        # message_bytes is the message in bytes
                else:
                    message_bytes = message

            message_length = len(message_bytes)
            byte_list.append(fin + rsv1 + rsv2 + rsv3 + opcode.value)       # Adding the first byte to the byte_list

            if message_length <= 125:
                byte_list.append(message_length)                            # No additional bytes required

            elif 126 <= message_length <= 65535:
                byte_list.append(126)                                       # Two additional bytes
                byte_list.append((message_length >> 8) & 255)
                byte_list.append(message_length & 255)

            else:
                byte_list.append(127)                                       # Eight additional bytes
                byte_list.append((message_length >> 56) & 255)              # The number of extra bytes is decided by the max_lenght_frame in the function encode_frame
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
        except ExtensionException as e:
            return None

    def decode_message(self, message):
        """
        Function for decoding messages from client to server
        :param message: bytes recieved from client
        :return: the function returns the decoded message, opcode and fin
        """
        try:
            masked = (int(message[1]))
            if masked < 128:                                        # Check if incoming message is masked
                print("Frame from client is not masked")
                raise FrameNotMaskedException

            first_byte = int(message[0])

            if first_byte < 128:                                    # Check value of FIN and set fin
                fin = False
            else:
                fin = True

            opcode = first_byte%16                                  # Find opcode from the first byte
            opcode = Opcode(opcode)
            if not isinstance(opcode, Opcode):                      # Check if found opcode is a valid opcode
                raise TypeError('opcode must be an instance of Opcode Enum')

            decoded_message = []
            mask_start = 2                                          # Check where mask key starts
            if message[1] == 126:
                mask_start = 4
            if message[1] == 127:
                mask_start = 10
            data_start = mask_start + 4
            masks = message[mask_start:data_start]                  # Mask = mask key

            j = 0
            while data_start < len(message):                        # Unmasks message and adding to the decoded message list
                mess = message[data_start] ^ masks[j%4]
                if opcode is Opcode.BINARY_FRAME:
                    decoded_message.append(bin(mess))               # Can also be chr(mess)
                else:
                    decoded_message.append(chr(mess))
                data_start += 1
                j += 1

            return ''.join(decoded_message), opcode, fin
        except FrameNotMaskedException as e:
            print("FrameNotMaskedException: ")
            print(e)
            return e, None, False
        except ExtensionException as e:
            print("ExtensionException: ")
            print(e)
            return e, None, False
        except TypeError as e:
            print("TypeError")
            print(e)
            return e, None, False
