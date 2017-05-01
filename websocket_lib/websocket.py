import socket
from threading import Thread

from websocket_lib.client_socket import ClientSocket


class WebSocket(Thread):
    server_running = True

    def __init__(self, ip_address="127.0.0.1", port_number=80, backlog=5):
        super().__init__()
        self.ip_address = ip_address
        self.port_number = port_number
        self.backlog = backlog
        self.clients = []
        #WSS
        #PROXY
        #THREADS

    def run(self):
        print("Starting WebSocket server...")
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((self.ip_address, self.port_number))
        listen_socket.listen(self.backlog)
        print("WebSocket server running at: {}:{}...".format(self.ip_address, self.port_number))

        while self.server_running:
            connection, address = listen_socket.accept()  # TODO. start thread med ny connection
            client = ClientSocket(connection)
            client.start()
            self.on_connection(client)
            print("Incoming client connection from:", address)

    def start_server(self):
        self.start()

    def stop_server(self):
        self.server_running = False
        # TODO: stop thread?
        # TODO: close all sockets?

    def on_connection(self, new_client):
        self.clients.append(new_client)
        # TODO: Add more ?
        raise NotImplementedError("Use websocket..class")

    def on_message(self):
        raise NotImplementedError()

    def on_close(self):
        raise NotImplementedError()

    def on_error(self):
        raise NotImplementedError()


#web_socket = WebSocket("127.0.0.1", 3001)
#web_socket.start_server()
