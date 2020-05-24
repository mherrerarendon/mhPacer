from source import api
import unittest


class TestApi(unittest.TestCase):
    def test_parseSpeedStr(self):
        actualResponse = api.parseSpeedStr('')
        self.assertEqual(2, actualResponse['exitcode'])

        actualResponse = api.parseSpeedStr('dummy')
        self.assertEqual(2, actualResponse['exitcode'])

        actualResponse = api.parseSpeedStr('10')
        self.assertEqual(2, actualResponse['exitcode'])

        actualResponse = api.parseSpeedStr('10k')
        self.assertEqual(2, actualResponse['exitcode'])

        actualResponse = api.parseSpeedStr('10kph')
        self.assertEqual(0, actualResponse['exitcode'])

    def test_parsePaceStr(self):
        actualResponse = api.parsePaceStr('')
        self.assertEqual(2, actualResponse['exitcode'])

        actualResponse = api.parsePaceStr('dummy')
        self.assertEqual(2, actualResponse['exitcode'])

        actualResponse = api.parsePaceStr('10')
        self.assertEqual(2, actualResponse['exitcode'])

        actualResponse = api.parsePaceStr('10m')
        self.assertEqual(5, actualResponse['exitcode'])

        actualResponse = api.parsePaceStr('10 min mile')
        self.assertEqual(0, actualResponse['exitcode'])

    def test_parseTargetEventStr(self):
        actualResponse = api.parseTargetEventStr('')
        self.assertEqual(2, actualResponse['exitcode'])

        actualResponse = api.parseTargetEventStr('dummy')
        self.assertEqual(4, actualResponse['exitcode'])

        actualResponse = api.parseTargetEventStr('10')
        self.assertEqual(4, actualResponse['exitcode'])

        actualResponse = api.parseTargetEventStr('10m')
        self.assertEqual(0, actualResponse['exitcode'])

    def test_getEventTimeWithSpeed(self):
        actualResponse = api.getEventTimeWithSpeed('', '')
        self.assertEqual(2, actualResponse['exitcode'])

        actualResponse = api.getEventTimeWithSpeed('speedDummyStr', 'eventDummyStr')
        self.assertEqual(2, actualResponse['exitcode'])

        actualResponse = api.getEventTimeWithSpeed('10', 'm')
        self.assertEqual(2, actualResponse['exitcode'])

        actualResponse = api.getEventTimeWithSpeed('10kph', '400m')
        self.assertEqual(0, actualResponse['exitcode'])

        
if __name__ == '__main__':
    unittest.main()
