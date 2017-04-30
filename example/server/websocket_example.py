from websocket_lib.websocket import WebSocket

"""
Example of usage with the web socket library
"""

ip_address = "127.0.0.1"
port_number = 3001
backlog = 5

web_socket = WebSocket(ip_address, port_number, backlog)
web_socket.start_server()
