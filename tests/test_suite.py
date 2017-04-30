from unittest import TestSuite
from tests.test_utilities import TestUtilities
from tests.test_frames import TestFrames


def create_suite():
    test_suite = TestSuite()
    test_suite.addTest(TestUtilities())
    test_suite.addTest(TestFrames())

create_suite()
