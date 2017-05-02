from websocket_lib.websocket import WebSocket
from websocket_lib.frames import Frames
from websocket_lib.state import State

"""
Example of usage with the web socket library
"""


class WebSocketExample(WebSocket):
    ip_address = "127.0.0.1"
    port_number = 3001
    backlog = 5

    def __init__(self):
        super().__init__(self.ip_address, self.port_number, self.backlog)

    def on_connection(self, new_client):
        print("New incoming client connection")

    def on_error(self):
        print("Client error")

    def on_message(self, new_message): #, sender):
        print("Received a message: ", new_message)
        frames = Frames()
        for client in self.clients:
            if client.state == State.OPEN and client:
                print("Client:", client)
                #client.send(frames.text_frame(new_message))

    def on_close(self, client_closed):
        print("Client closed: ", client_closed)

wsExample = WebSocketExample()
wsExample.start_server()
