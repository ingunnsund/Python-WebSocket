from enum import Enum


class Opcode(Enum):
    CONTINUATION_FRAME = 0       # 0000 / %x0
    TEXT_FRAME = 1               # 0001 / %x1
    BINARY_FRAME = 2             # 0010 / %x2
    CONNECTION_CLOSE_FRAME = 8   # 1000 / %x8
    PING_FRAME = 9               # 1001 / %x9
    PONG_FRAME = 10              # 1010 / %xA
