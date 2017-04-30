from websocket_lib.frames import Frames

test = Frames()

print(test.encode_message("test"))

#print(test.decode_message(b'\x81\x04test'))
print(test.decode_message(b'\x81\x8c\xff\xb8\xbd\xbd\xb7\xdd\xd1\xd1\x90\x98\xea\xd2\x8d\xd4\xd9\x9c'))
print(test.decode_message(b'\x81\x83!\xba+Ai\xdfB'))
print(test.decode_message(b'\x81\x85\x37\xfa\x21\x3d\x7f\x9f\x4d\x51\x58'))



