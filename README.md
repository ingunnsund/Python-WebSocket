# Python-WebSocket    [![Build Status](https://api.travis-ci.com/ingunnsund/Python-WebSocket.svg?token=ZxxpdBJahNzv1GsguPxE&branch=master)](https://travis-ci.com/ingunnsund/Python-WebSocket)

A Python WebSocket library


## Features
- Supports handshake
- Multiple clients with threads
- Supports messages in text or binary  
  - With fragmented frames if message length is large enough
  - Server <-> Client and Client1 <-> Server <-> Client2
- Possibilities for sending small files 
- Ping and Pong
- Close with status and reason
- Allows one extension (if some changes are made for the exact extension in the code)
  - For example: the permessage-deflate extension needs a decompression algorithm 
- Good error handling with custom exceptions
- Communicates with a webbrowser via JavaScript
- Timeout with ping and pong

### Future Implementation
- WSS (WebSocket Secure)
- Better extension solution
- Fragmented frames for sending a message that is of unknown size without having to buffer the message
  - Fragmented frames for multiplexing is implemented
- Send large files

## Installation
#### Clone code from github
```
git clone https://github.com/ingunnsund/Python-WebSocket
```

After clone is completed the library can be used like the [example code](example) or see [Usage section](https://github.com/ingunnsund/Python-WebSocket#usage)

## Usage
This library is made easy by using a interface that the user of the library has to extend.
It can be done like this:
```python
class WebSocketExample(WebSocket):
```
There are some methods that needs to be overrided:
```python
def on_connection(self, new_client):
  #Method that is called each time a new client connects to the server.

def on_error(self, error_message):
  #Method that is called each time an error occours with a client.

def on_message(self, new_message, sender):
  #Method that is called each time a message is sent to a client.
  #The message and the sender is passed on from the abstract method.

def on_close(self, client_closed):
  #Method that is called each time a client disconnects from the server.
```

For example with chat see [code example](example)


## Testing
See [unit tests](tests) and [Travis CI](https://travis-ci.com/ingunnsund/Python-WebSocket)

## License 
MIT License: Copyright © 2017 Ingunn Sund and Knut Kirkhorn
