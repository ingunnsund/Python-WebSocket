import socket
from hashlib import sha1
from base64 import b64encode

from websocket_lib.client_socket import ClientSocket


class WebSocket(object):

    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    IP_ADDRESS = "127.0.0.1"
    # TODO: legge til i konstruktør?
    server_running = True
    BUFFER_SIZE = 1024

    handshake_response = "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: {}\r\n"

    def __init__(self, port_number=80, backlog=5):
        self.port_number = port_number
        self.backlog = backlog
        #WSS
        #PROXY
        #THREADS

    def send_message(self):
        print("SEND_MESSAGE")

    def make_accept_key(self, sec_key):
        hash_key = sha1(str.encode(sec_key)).digest()
        new_accept_key = b64encode(hash_key)
        return new_accept_key

    def start_server(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((self.IP_ADDRESS, self.port_number))
        listen_socket.listen(self.backlog)

        while self.server_running:
            connection, address = listen_socket.accept() #TODO. start thread med ny connection
            client = ClientSocket(connection)

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
                    print("\n-------\n")

                    if client.has_handshaked:
                        print("has handshaked")
                        #TODO: do stuff with message/frames?
                    else:
                        if self.check_client_handshake(received_headers):
                            sec_websocket_key = received_headers.split("Sec-WebSocket-Key: ")[1].split("\n")[0]
                            sec_websocket_accept = self.make_accept_key(sec_websocket_key).decode("UTF-8")

                            temp_handshake_response = str.encode(self.handshake_response.format(sec_websocket_accept))

                            connection.send(temp_handshake_response)

                            print("Sendt response:")
                            print(temp_handshake_response.decode("UTF-8"))
                            print("-----")

                            close_down = True
                        else:
                            connection.send(str.encode("HTTP/1.1 426 Upgrade Required\r\n"
                                             +"Content-Type: text/html\r\n"
                                             +"\r\n"
                                             + "<html><body>\r\n"
                                             + "<pre>Upgrade Required</pre>\r\n"
                                             + "</body></head>\r\n\r\n"))
                            print("not correctly displayed handshake")
                            connection.close()
                            close_down = True


                except socket.error as e:
                    print("Error: ")
                    # TODO: print e?

    @staticmethod
    def check_client_handshake(client_handshake):
        # The openning handshake must be a GET request and be at least HTTP 1.1 #TODO: fiks høyere versjoner
        if not client_handshake.find("GET / HTTP/1.1") >= 0:
            # TODO: can receive a handshake with higher version of HTTP than 1.1
            return False

        # TODO: "The handshake MUST be a valid HTTP request as specified by"
        # TODO: Check if the headers contains websocket
        # TODO: sjekk om man trenger en host header
        # TODO: må inneholde:
        # TODO: - |Host|
        # TODO: - |Upgrade|
        # TODO: - |Connection|
        # TODO: - |Sec-WebSocket-Version|.  The value of this header field MUST be 13.
        # TODO: sjekk om "MAY CONTAINS headers"
        # TODO: lage unittester for dette

        # The opening handshake must also include some HTTP headers:
        if not client_handshake.find("Host: ") >= 0:
            return False
        if not client_handshake.find("Upgrade: ") >= 0:
            #TODO: check if CONTAINING: websocket keyword
            return False
        if not client_handshake.find("Connection: ") >= 0:
            return False
        if not client_handshake.find("Sec-WebSocket-Version: 13") >= 0:
            return False

        # Returning True if all checks fails
        return True


web_socket = WebSocket(3001)
print("Starting WebSocket server...")
web_socket.start_server()
print("WebSocket server running...")
