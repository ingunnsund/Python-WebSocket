from websocket_lib.websocket import WebSocket
from websocket_lib.state import State

"""
Example of usage with the web socket library
"""


class WebSocketExample(WebSocket):
    # Variables for use of server
    ip_address = "127.0.0.1"
    port_number = 3001
    backlog = 5
    # Timeout if no frame is sent or received after 300 seconds then the server sends a PING_FRAME to the client.
    ping_timeout = 300            # Or use for compression extension:
    extension = ""                # "permessage-deflate"
    extension_number_rsv = 0      # 1
    max_length_frame = 65535

    def __init__(self):
        super().__init__(self.ip_address, self.port_number, self.backlog, self.ping_timeout, self.max_length_frame,
                         self.extension, self.extension_number_rsv)

    def on_connection(self, new_client):
        print("New incoming client connection from:", new_client.address)

    def on_error(self, error_message):
        print("Client error: " + error_message)

    def on_message(self, new_message, sender):
        print("Received a message (from:", sender.address, "): ", new_message)
        for client in self.clients:
            if client.state == State.OPEN and client:
                print("Client:", client)
                client.send(new_message)

    def on_close(self, client_closed):
        print("Client closed: ", client_closed)

wsExample = WebSocketExample()
wsExample.start_server()
