

class FrameNotMaskedException(Exception):
    pass
    """
    The server MUST close the connection upon receiving a
    frame that is not masked.  In this case, a server MAY send a Close
    frame with a status code of 1002 (protocol error) 
    """


class CloseFrameTooLongException(Exception):
    pass


class ExtensionException(Exception):
    pass


class TooLongMaxFrameException(Exception):
    pass