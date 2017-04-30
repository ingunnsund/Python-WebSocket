from unittest import TestCase

from websocket_lib.utilities import Utilities


class TestUtilities(TestCase):
    def test_make_accept_key(self):
        sec_websocket_key = "x3JJHMbDL1EzLkh9GBhXDw=="
        result = Utilities.make_accept_key(sec_websocket_key)
        expected_result = "HSmrc0sMlYUkAGmm5OPpG2HaGWk="

        self.assertEqual(result, expected_result)

    def test_check_correct_handshake(self):
        handshake_request = "GET /chat HTTP/1.1\n" \
                            "Host: server.example.com\n" \
                            "Upgrade: websocket\n" \
                            "Connection: Upgrade\n" \
                            "Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==\n" \
                            "Sec-WebSocket-Protocol: chat, superchat\n" \
                            "Sec-WebSocket-Version: 13\n" \
                            "Origin: http://example.com\n\n"
        result = Utilities.check_correct_handshake(handshake_request)
        self.assertTrue(result)

    def test_handshake_http_version(self):
        # Test for checking if version 0.9 is incorrect (False) and 2.0 is correct (True)
        handshake_request_start = "GET /chat HTTP/"
        handshake_request_end = "\n" \
                                "Host: server.example.com\n" \
                                "Upgrade: websocket\n" \
                                "Connection: Upgrade\n" \
                                "Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==\n" \
                                "Sec-WebSocket-Protocol: chat, superchat\n" \
                                "Sec-WebSocket-Version: 13\n" \
                                "Origin: http://example.com\n\n"

        handshake_lower_version = handshake_request_start + "0.9" + handshake_request_end
        handshake_higher_version = handshake_request_start + "2.0" + handshake_request_end
        result_lower = Utilities.check_correct_handshake(handshake_lower_version)
        result_higher = Utilities.check_correct_handshake(handshake_higher_version)

        self.assertFalse(result_lower)
        self.assertTrue(result_higher)
