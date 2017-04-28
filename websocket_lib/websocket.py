import socket
from hashlib import sha1
from base64 import b64encode


class WebSocket(object):

    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    IP_ADDRESS = "127.0.0.1" # TODO: legge til i konstruktør?
    server_running = True
    BUFFER_SIZE = 1024

    def __init__(self, port_number=80):
        self.port_number = port_number
        #WSS
        #PROXY
        #THREADS

    def do_handshake(self):
        print("HANDSHAKE")

    def send_message(self):
        print("SEND_MESSAGE")

    def make_accept_key(self, sec_key):
        hash_key = sha1(str.encode(sec_key)).digest()
        new_accept_key = b64encode(hash_key)
        return new_accept_key

    def start_server(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((self.IP_ADDRESS, self.port_number))
        listen_socket.listen(1)

        while self.server_running:
            connection, address = listen_socket.accept()

            close_down = False
            while not close_down:
                try:
                    received_bytes = connection.recv(self.BUFFER_SIZE)
                    if not received_bytes:
                        break

                    received_headers = received_bytes.decode("UTF-8")
                    #TESTING-PRINTS
                    print("Headers from client:")
                    print(received_headers)

                    # TODO: Check if the headers contains websocket
                    # TODO: sjekk om man trenger en host header
                    # TODO: må inneholde:
                    # TODO: - |Host|
                    # TODO: - |Upgrade|
                    # TODO: - |Connection|
                    # TODO: - |Sec-WebSocket-Version|.  The value of this header field MUST be 13.
                    # TODO: sjekk om "MAY CONTAINS headers"
                    # TODO: lage unittester for dette
                    # if received_headers.find("") >= 0 and received_headers.find("") >= 0:
                    # if received_headers.find("") >=

                    #TODO: blir alt som er igjen, BUG
                    sec_websocket_key = received_headers.split("Sec-WebSocket-Key: ")[1].split("\n")[0]
                    sec_websocket_accept = self.make_accept_key(sec_websocket_key)

                    connection.send(str.encode("""HTTP/1.1 101 Switching Protocols
                    Upgrade: websocket
                    Connection: Upgrade
                    Sec-WebSocket-Accept: {}
                    Sec-WebSocket-Protocol: chat

                    """.format(sec_websocket_accept)))
                    close_down = True

                except socket.error as e:
                    print("Error: ")
                    # TODO: print e?


wSocket = WebSocket()
wSocket.start_server()