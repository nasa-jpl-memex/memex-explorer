import unittest

from tests.test_front_page import ServerUpTest


def suite():
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(ServerUpTest))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()

try:
    runner.run(test_suite)
except:
    pass



