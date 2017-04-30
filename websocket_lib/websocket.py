import socket

from websocket_lib.client_socket import ClientSocket


class WebSocket(object):

    IP_ADDRESS = "127.0.0.1"
    # TODO: legge til i konstruktør?
    server_running = True
    BUFFER_SIZE = 1024

    def __init__(self, port_number=80, backlog=5):
        self.port_number = port_number
        self.backlog = backlog
        #WSS
        #PROXY
        #THREADS

    def send_message(self):
        print("SEND_MESSAGE")

    def start_server(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((self.IP_ADDRESS, self.port_number))
        listen_socket.listen(self.backlog)
        print("WebSocket server running at: {}:{}...".format(self.IP_ADDRESS, self.port_number))

        while self.server_running:
            connection, address = listen_socket.accept()  # TODO. start thread med ny connection
            client = ClientSocket(connection)
            print("Incoming client connection from: ", address)

            try:
                received_bytes = client.receive(self.BUFFER_SIZE)
                if not received_bytes:
                    break

                received_headers = received_bytes.decode()

                if client.handshake_done:
                    print("has handshaked")
                    # TODO: do stuff with message/frames?
                else:
                    if self.check_client_handshake(received_headers):
                        sec_websocket_key = received_headers.split("Sec-WebSocket-Key: ")[1].split("\r\n")[0]

                        client.do_handshake(sec_websocket_key)
                        # close_down = True
                    else:
                        client.send(str.encode("HTTP/1.1 426 Upgrade Required\r\n"
                                               + "Content-Type: text/html\r\n"
                                               + "\r\n"
                                               + "<html><body>\r\n"
                                               + "<pre>Upgrade Required</pre>\r\n"
                                               + "</body></head>\r\n\r\n"))
                        print("The request from the client is not a correct handshake")
                        client.close()

            except socket.error as e:
                print("Error: ")
                # TODO: print e?

    @staticmethod
    def check_client_handshake(client_handshake):
        MINIMUM_HTTP_VERSION = 1.1 # TODO: fiks VARIABEL FOR DENNE
        # The openning handshake must be a GET request and be at least HTTP 1.1 #TODO: fiks høyere versjoner
        if not client_handshake.find("GET / HTTP/") >= 0:
            # TODO: can receive a handshake with higher version of HTTP than 1.1
            return False
        else:
            http_version = float(client_handshake.split("GET / HTTP/")[1].split("\n")[0])
            if not http_version >= MINIMUM_HTTP_VERSION:
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
