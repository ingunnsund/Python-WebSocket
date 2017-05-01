from websocket_lib.websocket import WebSocket

"""
Example of usage with the web socket library
"""

ip_address = "127.0.0.1"
port_number = 3001
backlog = 5


class WebSocketExample(WebSocket):

    def __init__(self):
        super().__init__(ip_address, port_number, backlog)

    def on_connection(self, new_client):
        print("New incoming client connection")

    def on_error(self):
        print("Client error")

    def on_message(self, new_message):
        print("Received a message: ", new_message)
        for client in self.clients:
            #client
            print(client)

    def on_close(self, client_closed):
        print("Client closed: ", client_closed)

wsExample = WebSocketExample()
wsExample.start_server()
