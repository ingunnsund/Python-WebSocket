from unittest import TestSuite
from tests.test_utilities import TestUtilities


def create_suite():
    test_suite = TestSuite()
    test_suite.addTest(TestUtilities())

create_suite()
