from enum import Enum


class State(Enum):
    CONNECTING = 1
    TIME_WAIT = 2
    OPEN = 3
    CLOSING = 4
    CLOSED = 5
    # more and fix this
