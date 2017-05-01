print("test")

from websocket_lib.frames import Frames

frames = Frames()
test, opcode = frames.decode_message(b"\x8a\x85\x37\xfa\x21\x3d\x7f\x9f\x4d\x51\x58") #(b'\x81\x83!\xba+Ai\xdfB')
print("pong-frame:")
print(test)
print(opcode)


test2, test3 = frames.decode_message(b'\x81\x05Hello')