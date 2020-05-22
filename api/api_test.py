# In order to run this tests, run this file directly. No pytest
import unittest

import api


class TestApp(unittest.TestCase):
    def test_parseSpeedStr(self):
        speed = api.parseSpeedStr('dummy')
        pass


if __name__ == '__main__':
    unittest.main()
