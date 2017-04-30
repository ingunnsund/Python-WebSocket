from websocket_lib.websocket import WebSocket

"""
Example of usage with the web socket library
"""

port_number = 3001
backlog = 5

web_socket = WebSocket(port_number, backlog)
web_socket.start_server()
