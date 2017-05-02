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
            client = ClientSocket(connection, address, self)
            client.start()
            self.clients.append(client) # TODO: add remove from array
            self.on_connection(client)

    def start_server(self):
        self.start()

    def stop_server(self):
        """
        method for stopping the server, its thread and closing all client sockets  
        """
        self.server_running = False
        for client in self.clients:
            client.close_and_remove()
        self.stop()
        # TODO: stop thread?
        # TODO: close all sockets?

    def on_connection(self, new_client):
        """
        :param new_client: is the new client connecting to the web socket server
        """
        raise NotImplementedError("This method is abstract and meant to be extended")

    def on_message(self, new_message, sender):
        """
        :param new_message: is the message being sent
        :param sender: is the sender of the message (which is a ClientSocket object)
        """
        raise NotImplementedError("This method is abstract and meant to be extended")

    def on_close(self, client_closed):
        # TODO: status code/reason?
        raise NotImplementedError("This method is abstract and meant to be extended")

    def on_error(self):
        raise NotImplementedError("This method is abstract and meant to be extended")
