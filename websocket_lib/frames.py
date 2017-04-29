# FIN: final fragment
# RSV1,2,3: MUST be 0 unless an extension is negotiated that defines meanings for non-zero values.
# opcode:
""" *  %x0 denotes a continuation frame
    *  %x1 denotes a text frame
    *  %x2 denotes a binary frame
    *  %x3-7 are reserved for further non-control frames
    *  %x8 denotes a connection close
    *  %x9 denotes a ping
    *  %xA denotes a pong
    *  %xB-F are reserved for further control frames"""
# Mask: is masked
# Payload length:  7 bits, 7+16 bits, or 7+64 bits
# Masking key: 0 or 4 bytes

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

class Frames(object):

    # Encode message from server
    def encode_message(self, message):
        if len(message) == 0:
            return -1
        fin = "1"
        rsv1 = "0"
        rsv2 = "0"
        rsv3 = "0"
        byte_list = [] #list of integers
        opcode = "0001" #TEXT
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


    # Decode message from client
    def decode_message(self, message):
        byte_list = message




