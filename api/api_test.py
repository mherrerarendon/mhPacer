# In order to run this tests, run this file directly. No pytest
import unittest

import api


class TestApp(unittest.TestCase):
    def test_parseSpeedStr(self):
        speed = api.parseSpeedStr('dummy')
        print(speed)
        self.assertEqual(1, 1)
        pass


if __name__ == '__main__':
    unittest.main()
