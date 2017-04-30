from enum import Enum

class StatusCode(Enum):
    CLOSE_NORMAL = 1000         #Normal closure; the connection successfully completed whatever purpose for which it was created.
    CLOSE_GOING_AWAY = 1001     #The endpoint is going away, either because of a server failure or because the browser is navigating away from the page that opened the connection.
    CLOSE_PROTOCOL_ERROR = 1002 #The endpoint is terminating the connection due to a protocol error.
    CLOSE_UNSUPPORTED = 1003    #The connection is being terminated because the endpoint received data of a type it cannot accept (for example, a text-only endpoint received binary data).
    CLOSE_NO_STATUS = 1005      #Reserved.  Indicates that no status code was provided even though one was expected.
    CLOSE_ABNORMAL = 1006       #Reserved. Used to indicate that a connection was closed abnormally (that is, with no close frame being sent) when a status code is expected.
    UNSUPPORTED_DATA = 1007     #The endpoint is terminating the connection because a message was received that contained inconsistent data (e.g., non-UTF-8 data within a text message).
    POLICY_VIOLATION = 1008     #The endpoint is terminating the connection because it received a message that violates its policy. This is a generic status code, used when codes 1003 and 1009 are not suitable.
    CLOSE_TOO_LARGE = 1009      #The endpoint is terminating the connection because a data frame was received that is too large.
    MISSING_EXTENSION = 1010    #The client is terminating the connection because it expected the server to negotiate one or more extension, but the server didn't.
    INTERNAL_ERROR = 1011       #The server is terminating the connection because it encountered an unexpected condition that prevented it from fulfilling the request.
    SERVICE_RESTART = 1012      #The server is terminating the connection because it is restarting.
    TRY_AGAIN_LATER = 1013      #The server is terminating the connection due to a temporary condition, e.g. it is overloaded and is casting off some of its clients.
    TLS_HANDSHAKE = 1015        #Reserved. Indicates that the connection was closed due to a failure to perform a TLS handshake (e.g., the server certificate can't be verified).
