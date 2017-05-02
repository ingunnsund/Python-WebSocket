# Python-WebSocket    [![Build Status](https://api.travis-ci.com/ingunnsund/Python-WebSocket.svg?token=ZxxpdBJahNzv1GsguPxE&branch=master)](https://travis-ci.com/ingunnsund/Python-WebSocket)

A Python WebSocket library


## Features
- Supports handshake
- Multiple clients with threads
- Supports small messages in text or binary
  - fragmentation? comp^
- Ping/Pong
- Close with status and reason
- Extentions ?
- WSS ? 
- Timeout ?

## Installation

## Usage
This library is made easy like a interface that is only needed to be extended by the user of the library.
It can be done like this:
```python
class WebSocketExample(WebSocket):
```
There are some methods that needs to be overrided:
```python
def on_connection(self, new_client):

def on_error(self):

def on_message(self, new_message, sender):

def on_close(self, client_closed):
```

For example with chat see [code example](example)

## Dependencies

## Testing
See [unit tests](tests) and [Travis CI](https://travis-ci.com/ingunnsund/Python-WebSocket)

## License 
MIT License: Copyright © 2017 Ingunn Sund and Knut Kirkhorn
