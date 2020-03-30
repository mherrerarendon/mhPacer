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
            DISTANCE_KEY: 12,
            DISTANCE_UNIT_KEY: DistanceUnits.KM,
            TIME_KEY: 1,
            TIME_UNIT_KEY: TimeUnits.Hour
        }
        return speed

    def test_GetSpeedInTargetUnits(self):
        speed = self.CreateSpeed(12, DistanceUnits.KM, 1, TimeUnits.Hour)
        targetEvent = {DISTANCE_KEY: 400, DISTANCE_UNIT_KEY: DistanceUnits.Meter}
        targetTimeUnit = TimeUnits.Second
        speedInTargetUnits = rpc.GetSpeedInTargetUnits(speed, targetEvent[DISTANCE_UNIT_KEY], targetTimeUnit)
        self.assertEqual(speedInTargetUnits[DISTANCE_KEY], 12)
        self.assertEqual(speedInTargetUnits[DISTANCE_UNIT_KEY], DistanceUnits.Meter)
        self.assertEqual(speedInTargetUnits[TIME_KEY], 1)
        self.assertEqual(speedInTargetUnits[TIME_UNIT_KEY], targetTimeUnit)

    def test_GetEventTimeFromSpeed(self):
        event = {DISTANCE_KEY: 1, DISTANCE_UNIT_KEY: DistanceUnits.Mile}
        self.assertEqual(round(rpc.GetEventTimeFromSpeed('1kph', event, TimeUnits.Hour), 2), 1.61)


if __name__ == '__main__':
    unittest.main()
