import socket
from threading import Thread

from websocket_lib.client_socket import ClientSocket


class WebSocket(Thread):
    server_running = True

    def __init__(self, ip_address="127.0.0.1", port_number=80, backlog=5, extension="", rsv_number_extension=0):
        super().__init__()
        self.ip_address = ip_address
        self.port_number = port_number
        self.backlog = backlog
        self.clients = []
        self.extension = extension
        self.rsv_number_extension = rsv_number_extension

    def run(self):
        """
        Overrided method from the Thread class that make the web socket server run threaded
        """
        print("Starting WebSocket server...")
        # Start the server and listen for connections
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((self.ip_address, self.port_number))
        listen_socket.listen(self.backlog)
        print("WebSocket server running at: {}:{}...".format(self.ip_address, self.port_number))

        while self.server_running:
            # Set variable of the connection and the address of the incoming connection
            connection, address = listen_socket.accept()
            # Create a new client and start the thread to it.
            client = ClientSocket(connection, address, self)
            client.start()
            # Add the client to the list of clients
            self.clients.append(client)
            self.on_connection(client)

    def start_server(self):
        """
        Method for starting the server and its thread
        """
        self.start()

    def stop_server(self):
        """
        method for stopping the server, its thread and closing all client sockets  
        """
        self.server_running = False
        for client in self.clients:
            client.close_and_remove()
        # Stops the thread to the server
        self._stop()

    def on_connection(self, new_client):
        """
        Abstract method of when a client in the websockets client list is added (a client connects to the web socket
        server).
        This method is meant to be extended.
        :param new_client: is the new client connecting to the web socket server
        """
        raise NotImplementedError("This method is abstract and meant to be extended")

    def on_message(self, new_message, sender):
        """
        Abstract method of when a client in the websockets client list receives a message.
        This method is meant to be extended.
        :param new_message: is the message being sent
        :param sender: is the sender of the message (which is a ClientSocket object)
        """
        raise NotImplementedError("This method is abstract and meant to be extended")

    def on_close(self, client_closed):
        """
        Abstract method of when a client in the websockets client list closes/disconnects.
        This method is meant to be extended.
        :param client_closed: the client that is closed
        """
        # TODO: status code/reason?
        raise NotImplementedError("This method is abstract and meant to be extended")

    def on_error(self, error_message):
        """
        Abstract method of when a client in the websockets client list gets an error.
        This method is meant to be extended.
        :return: 
        """
        # TODO: add parameter to this method
        raise NotImplementedError("This method is abstract and meant to be extended")
