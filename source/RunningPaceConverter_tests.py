import unittest

from SpeedStrParser import *
from RunningPaceConverter import RunningPaceConverter
from Types import *


class TestRunningPaceConverter(unittest.TestCase):
    def AssertEventConversion(self, event, distanceTargetUnit, expected):
        dummyTime = Time(1, Time.Hour)
        dummySpeed = Speed(event, dummyTime)
        rpc = RunningPaceConverter(dummySpeed)
        actual = rpc.GetEventWithUnit(distanceTargetUnit)
        self.assertEqual(round(actual, 2), round(expected, 2))

    def test_GetEventWithUnit(self):
        self.AssertEventConversion(Event(2, DistanceUnits.Mile), DistanceUnits.KM, 3.22)
        self.AssertEventConversion(Event(2, DistanceUnits.KM), DistanceUnits.Mile, 1.24)

    def AssertTimeConversion(self, time, targetUnit, expected):
        dummyEvent = Event(1, DistanceUnits.KM)
        dummySpeed = Speed(dummyEvent, time)
        rpc = RunningPaceConverter(dummySpeed)
        actual = rpc.GetTimeWithUnit(targetUnit)
        self.assertEqual(round(actual, 2), round(expected, 2))

    def test_GetTimeWithUnit(self):
        self.AssertTimeConversion(Time(2, TimeUnits.Hour), TimeUnits.Second, 7200)
        self.AssertTimeConversion(Time(1000, TimeUnits.Second), TimeUnits.Hour, 0.28)
        self.AssertTimeConversion(Time(7200, TimeUnits.Second), TimeUnits.Hour, 2)

    def test_GetSpeedInTargetUnits(self):
        speed = Speed(Event(12, DistanceUnits.KM), Time(1, TimeUnits.Hour))
        targetEventUnit = DistanceUnits.Meter
        targetTimeUnit = TimeUnits.Second
        speedInTargetUnits = rpc.GetSpeedInTargetUnits(speed, targetEventUnit, targetTimeUnit)
        self.assertEqual(speedInTargetUnits.event.distance, 12)
        self.assertEqual(speedInTargetUnits.event.unit, DistanceUnits.Meter)
        self.assertEqual(speedInTargetUnits.time.time, 1)
        self.assertEqual(speedInTargetUnits.time.unit, targetTimeUnit)

    def test_GetEventTimeWithSpeed(self):
        speed = Speed(Event(1, DistanceUnits.KM), Time(1, TimeUnits.Hour))
        event = Event(1, DistanceUnits.Mile)
        self.assertEqual(round(rpc.GetEventTimeWithSpeed(speed, event, TimeUnits.Hour), 2), 1.61)


if __name__ == '__main__':
    unittest.main()
