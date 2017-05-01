from socket import error as socketerror
from threading import Thread

from websocket_lib.utilities import Utilities
from websocket_lib.frames import Frames
from websocket_lib.status_code import StatusCode
from websocket_lib.opcode import Opcode
from websocket_lib.state import State


class ClientSocket(Thread):
    handshake_template = "HTTP/1.1 101 Switching Protocols\r\n" \
                         "Upgrade: Websocket\r\n" \
                         "Connection: Upgrade\r\n" \
                         "Sec-WebSocket-Accept: {}\r\n\r\n"
    BUFFER_SIZE = 1024
    NOT_CORRECT_HANDSHAKE = str.encode("HTTP/1.1 426 Upgrade Required\r\n"
                                       + "Content-Type: text/html\r\n"
                                       + "\r\n"
                                       + "<html><body>\r\n"
                                       + "<pre>Upgrade Required</pre>\r\n"
                                       + "</body></head>\r\n\r\n")

    def __init__(self, socket, websocket, state=State.CONNECTING):
        super().__init__()
        self.socket = socket
        self.websocket = websocket
        self.state = state

    def run(self):
        # Change this
        while True:
            try:
                received_bytes = self.receive(self.BUFFER_SIZE)
                if not received_bytes:
                    break

                if self.state == State.OPEN:
                    frame = Frames()
                    message_from_client = frame.decode_message(received_bytes)

                    #message_from_client[0] = message and [1] = opcode of the message
                    #TODO: check if message is a MESSAGE or a ping/pong
                    #print(message_from_client)
                    self.websocket.on_message(message_from_client[0])

                    #TODO: if ping from client -> send pong, if ping(client) and close(client) -> do not send pong, send close
                    #TODO: if ping(client) + ping(client) -> send one pong (not required, not important)

                    #TODO: if message from client = not masked -> decode_message will return FrameNotMaskedException, None
                    #TODO: ^ send close frame with status code: 1002 PROTOCOL_ERROR and close connection
                    #TODO: try/catch?

                    # Send a close frame test:
                    #self.send(frame.close_frame(StatusCode.CLOSE_NORMAL, "Test"))
                    ##self.send(frame.close_frame(StatusCode.CLOSE_GOING_AWAY, "Test"))
                    #self.send(frame.ping_frame("Hello"))
                    #self.send(frame.close_frame(StatusCode.CLOSE_NORMAL, "TEST"))
                    #self.state = State.CLOSING

                elif self.state == State.CONNECTING:
                    received_headers = received_bytes.decode()
                    if Utilities.check_correct_handshake(received_headers):
                        sec_websocket_key = received_headers.split("Sec-WebSocket-Key: ")[1].split("\r\n")[0]

                        self.do_handshake(sec_websocket_key)
                        # close_down = True
                    else:
                        self.send(self.NOT_CORRECT_HANDSHAKE)
                        print("The request from the client is not a correct handshake")
                        self.state = State.CLOSED
                        # TODO: check if correct
                        self.close()
                        self.websocket.clients.remove(self)
                elif self.state == State.CLOSING:
                    print("CLOSING")

            except socketerror as e:
                #TODO: check om denne må bytte om navnene
                print("Error: ")
                # TODO: print e?
                # TODO: Check type of error and then check if it is needed to close the client
                self.state = State.CLOSED
                self.close()

    def receive(self, buffer_size):
        return self.socket.recv(buffer_size)

    def send(self, message):
        

    def __send(self, message):
        self.socket.send(message)

    def close(self):
        # TODO: check if already closed
        # TODO: check if connecting
        self.websocket.on_close(self) # TODO: check what line is on top?
        self.socket.close()

    def do_handshake(self, sec_websocket_key):
        sec_websocket_accept = Utilities.make_accept_key(sec_websocket_key)
        handshake_response = str.encode(self.handshake_template.format(sec_websocket_accept))

        self.send(handshake_response)
        self.state = State.OPEN
