import unittest

from RunningPaceConverter import RunningPaceConverter as rpc
from Types import *


class TestRunningPaceConverter(unittest.TestCase):
    def AssertDistanceConversion(self, distance, units, targetUnits, expected):
        actual = rpc.ConvertDistanceToDistance(distance, units, targetUnits)
        self.assertEqual(round(actual, 2), round(expected, 2))

    def test_ConvertDistanceToDistance(self):
        self.AssertDistanceConversion(2, DistanceUnits.Mile, DistanceUnits.KM, 3.22)
        self.AssertDistanceConversion(2, DistanceUnits.KM, DistanceUnits.Mile, 1.24)

    def AssertTimeConversion(self, time, units, targetUnits, expected):
        actual = rpc.ConvertTimeToTime(time, units, targetUnits)
        self.assertEqual(round(actual, 2), round(expected, 2))

    def test_ConvertTimeToTime(self):
        self.AssertTimeConversion(2, TimeUnits.Hour, TimeUnits.Second, 7200)
        self.AssertTimeConversion(1000, TimeUnits.Second, TimeUnits.Hour, 0.28)
        self.AssertTimeConversion(7200, TimeUnits.Second, TimeUnits.Hour, 2)

    @staticmethod
    def CreateSpeed(distance, distanceUnit, time, timeUnit):
        speed = {
            'distance': 12,
            'distanceUnit': DistanceUnits.KM,
            'time': 1,
            'timeUnit': TimeUnits.Hour
        }
        return speed

    def test_GetSpeedInTargetUnits(self):
        speed = self.CreateSpeed(12, DistanceUnits.KM, 1, TimeUnits.Hour)
        targetEvent = {'distance': 400, 'distanceUnit': DistanceUnits.Meter}
        targetTimeUnit = TimeUnits.Second
        speedInTargetUnits = rpc.GetSpeedInTargetUnits(speed, targetEvent, targetTimeUnit)
        self.assertEqual(speedInTargetUnits['distance'], 12)
        self.assertEqual(speedInTargetUnits['distanceUnit'], DistanceUnits.Meter)
        self.assertEqual(speedInTargetUnits['time'], 1)
        self.assertEqual(speedInTargetUnits['timeUnit'], targetTimeUnit)

    def test_GetTimeFromSpeed(self):
        import pdb; pdb.set_trace()  # breakpoint 33a71a1c //
        self.assertEqual(rpc.GetEventTimeFromSpeed('1mph', '1000m'), (16100, TimeUnits.Second))


if __name__ == '__main__':
    unittest.main()
