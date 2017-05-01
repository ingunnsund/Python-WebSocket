from websocket_lib.websocket import WebSocket

"""
Example of usage with the web socket library
"""

ip_address = "127.0.0.1"
port_number = 3001
backlog = 5

#web_socket = WebSocket(ip_address, port_number, backlog)
#web_socket.start_server()


class WebSocketExample(WebSocket):

    def __init__(self):
        super().__init__(ip_address, port_number, backlog)

    def on_connection(self, new_client):
        print("New incoming client connection")

    def on_error(self):
        print("Client error")

    def on_message(self):
        print("Received a message")

    def on_close(self):
        print("Client closed")

wsExample = WebSocketExample()
wsExample.start_server()
