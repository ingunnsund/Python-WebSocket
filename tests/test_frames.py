from unittest import TestCase

from websocket_lib.frames import Frames
from websocket_lib.opcode import Opcode


class TestFrames(TestCase):

    def test_encode_text_frame(self):
        frames = Frames()
        expected_result = b'\x81\x05Hello'
        self.assertEqual(frames.encode_frame(Opcode.TEXT_FRAME, "Hello"), expected_result)
        self.assertNotEqual(frames.encode_frame(Opcode.TEXT_FRAME, "Hei"), expected_result)

    def test_decode_text_frame(self):
        """
        Test if method decodes payload data and if it returns the right opcode for text frame
        both results are text frames but payload data is different
        :return: 
        """
        frames = Frames()
        expected_result_message = "Hello World!"
        expected_result_opcode = Opcode.TEXT_FRAME
        result1_message, result1_opcode = frames.decode_message(b'\x81\x8c\xff\xb8\xbd\xbd\xb7\xdd\xd1\xd1\x90\x98\xea\xd2\x8d\xd4\xd9\x9c')
        result2_message, result2_opcode = frames.decode_message(b'\x81\x83!\xba+Ai\xdfB')

        # Test for result1
        self.assertEqual(result1_message, expected_result_message)
        self.assertEqual(result1_opcode, expected_result_opcode)

        # Test for result2
        self.assertNotEqual(result2_message, expected_result_message)
        self.assertEqual(result2_opcode, expected_result_opcode)

    def test_decode_pong_frame(self):
        """
        Test if method returns correct opcode. Test for payload data: test_decode_text_frame
        result1 is a pong frame, result2 is a text frame
        :return: 
        """
        frames = Frames()
        expected_result_opcode = Opcode.PONG_FRAME
        result1_message, result1_opcode = frames.decode_message(b"\x8a\x85\x37\xfa\x21\x3d\x7f\x9f\x4d\x51\x58")
        result2_message, result2_opcode = frames.decode_message(b'\x81\x83!\xba+Ai\xdfB')

        # Test for result1:
        self.assertEqual(result1_opcode, expected_result_opcode)

        # Test for result2:
        self.assertNotEqual(result2_opcode, expected_result_opcode)


    def test_decode_close_frame(self):
        self.assertTrue(True, True) #TODO: write test

    def test_decode_unmasked_frame(self):
        """
        Test if attempt to decode unmasked frame results in exception
        :return: 
        """
        frames = Frames()
        result = frames.decode_message(b'\x81\x05Hello')
        self.failureException(result)

    def test_decode_fragmented_frame(self):
        self.assertTrue(True, True) #TODO: write test