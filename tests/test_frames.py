from unittest import TestCase
from websocket_lib.frames import Frames

class TestFrames(TestCase):

    def test_encode_message(self):
        frames = Frames()
        expected_result = b'\x81\x05Hello'
        self.assertEqual(frames.encode_message("Hello", "0001"), expected_result)
        self.assertNotEqual(frames.encode_message("Hei", "0001"), expected_result)

    def test_decode_message(self):
        frames = Frames()
        expected_result = "Hello World!"
        self.assertEqual(frames.decode_message(b'\x81\x8c\xff\xb8\xbd\xbd\xb7\xdd\xd1\xd1\x90\x98\xea\xd2\x8d\xd4\xd9\x9c'), expected_result)
        self.assertNotEqual(frames.decode_message(b'\x81\x83!\xba+Ai\xdfB'), expected_result)
