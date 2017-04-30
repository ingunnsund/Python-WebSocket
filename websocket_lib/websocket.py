import socket

from websocket_lib.client_socket import ClientSocket


class WebSocket(object):

    IP_ADDRESS = "127.0.0.1"
    # TODO: legge til i konstruktør?
    server_running = True

    def __init__(self, port_number=80, backlog=5):
        self.port_number = port_number
        self.backlog = backlog
        #WSS
        #PROXY
        #THREADS

    def send_message(self):
        print("SEND_MESSAGE")

    def close_server(self):
        self.server_running = False

    def start_server(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((self.IP_ADDRESS, self.port_number))
        listen_socket.listen(self.backlog)
        print("WebSocket server running at: {}:{}...".format(self.IP_ADDRESS, self.port_number))

        while self.server_running:
            connection, address = listen_socket.accept()  # TODO. start thread med ny connection
            client = ClientSocket(connection)
            client.start()
            print("Incoming client connection from: ", address)


web_socket = WebSocket(3001)
print("Starting WebSocket server...")
web_socket.start_server()
