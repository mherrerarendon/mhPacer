import unittest

from speedmath.SpeedStrParser import Speed, Event, Time, Pace
from speedmath.RunningPaceConverter import RunningPaceConverter
from speedmath.Types import DistanceUnits, TimeUnits


class TestRunningPaceConverter(unittest.TestCase):
    # Legacy
    def AssertEventConversion(self, event, expectedEvent):
        rpc = RunningPaceConverter()
        rpc.speed.event = RunningPaceConverter.ToBaseEvent(event)
        actualEvent = rpc.GetEventWithUnit(expectedEvent.unit)
        actualEvent.distance = round(actualEvent.distance, 2)
        self.assertEqual(actualEvent, expectedEvent)

    # Legacy
    def AssertTimeConversion(self, time, expectedTime):
        rpc = RunningPaceConverter()
        rpc.speed.time = RunningPaceConverter.ToBaseTime(time)
        actualTime = rpc.GetTimeWithUnit(expectedTime.unit)
        actualTime.time = round(actualTime.time, 2)
        self.assertEqual(actualTime, expectedTime)

    # Legacy
    def test_GetEventWithUnit(self):
        self.AssertEventConversion(Event(2, DistanceUnits.Mile), Event(3.22, DistanceUnits.KM))
        self.AssertEventConversion(Event(2, DistanceUnits.KM), Event(1.24, DistanceUnits.Mile))

    # Legacy
    def test_GetTimeWithUnit(self):
        self.AssertTimeConversion(Time(2, TimeUnits.Hour), Time(7200, TimeUnits.Second))
        self.AssertTimeConversion(Time(1000, TimeUnits.Second), Time(0.28, TimeUnits.Hour))
        self.AssertTimeConversion(Time(7200, TimeUnits.Second), Time(2, TimeUnits.Hour))

    def AssertSpeedConversion(self, speed, expectedSpeed):
        rpc = RunningPaceConverter(speed)
        actualSpeed = rpc.GetSpeedInTargetUnits(expectedSpeed.event.unit, expectedSpeed.time.unit)
        actualSpeed.event.distance = round(actualSpeed.event.distance, 2)
        actualSpeed.time.time = round(actualSpeed.time.time, 2)
        self.assertEqual(actualSpeed, expectedSpeed)

    def test_GetSpeedInTargetUnits(self):
        speed = Speed(Event(12, DistanceUnits.KM), Time(1, TimeUnits.Hour))
        expectedSpeed = Speed(Event(3.33, DistanceUnits.Meter), Time(1, TimeUnits.Second))
        self.AssertSpeedConversion(speed, expectedSpeed)

        speed = Speed(Event(3.33, DistanceUnits.Meter), Time(1, TimeUnits.Second))
        expectedSpeed = Speed(Event(11.99, DistanceUnits.KM), Time(1, TimeUnits.Hour))
        self.AssertSpeedConversion(speed, expectedSpeed)

        speed = Speed(Event(10, DistanceUnits.Mile), Time(1, TimeUnits.Hour))
        expectedSpeed = Speed(Event(16.10, DistanceUnits.KM), Time(1, TimeUnits.Hour))
        self.AssertSpeedConversion(speed, expectedSpeed)

        speed = Speed(Event(10, DistanceUnits.KM), Time(1, TimeUnits.Hour))
        expectedSpeed = Speed(Event(6.21, DistanceUnits.Mile), Time(1, TimeUnits.Hour))
        self.AssertSpeedConversion(speed, expectedSpeed)

    def test_GetEventTimeWithSpeed(self):
        speed = Speed(Event(1, DistanceUnits.KM), Time(1, TimeUnits.Hour))
        event = Event(1, DistanceUnits.Mile)
        actualTime = RunningPaceConverter.GetEventTimeWithSpeed(speed, event, TimeUnits.Hour)
        self.assertEqual(round(actualTime.time, 2), 1.61)

    def AssertSpeedToPaceConversion(self, speed, expectedPace):
        actualPace = RunningPaceConverter.GetPaceFromSpeed(speed)
        actualPace.time.time = round(actualPace.time.time, 2)
        self.assertEqual(actualPace, expectedPace)

    def test_GetPaceFromSpeed(self):
        speed = Speed(Event(6, DistanceUnits.Mile), Time(1, TimeUnits.Hour))
        expectedPace = Pace(Time(10, TimeUnits.Minute), Event(1, DistanceUnits.Mile))
        self.AssertSpeedToPaceConversion(speed, expectedPace)

        speed = Speed(Event(7, DistanceUnits.Mile), Time(1, TimeUnits.Hour))
        expectedPace = Pace(Time(8.57, TimeUnits.Minute), Event(1, DistanceUnits.Mile))
        self.AssertSpeedToPaceConversion(speed, expectedPace)

        speed = Speed(Event(8, DistanceUnits.KM), Time(1, TimeUnits.Hour))
        expectedPace = Pace(Time(7.5, TimeUnits.Minute), Event(1, DistanceUnits.KM))
        self.AssertSpeedToPaceConversion(speed, expectedPace)

    def AssertPaceToSpeedConversion(self, pace, expectedSpeed):
        actualSpeed = RunningPaceConverter.GetSpeedFromPace(pace)
        actualSpeed.event.distance = round(actualSpeed.event.distance, 2)
        self.assertEqual(actualSpeed, expectedSpeed)

    def test_GetSpeedFromPace(self):
        pace = Pace(Time(10, TimeUnits.Minute), Event(1, DistanceUnits.Mile))
        expectedSpeed = Speed(Event(6, DistanceUnits.Mile), Time(1, TimeUnits.Hour))
        self.AssertPaceToSpeedConversion(pace, expectedSpeed)

        pace = Pace(Time(8.57, TimeUnits.Minute), Event(1, DistanceUnits.Mile))
        expectedSpeed = Speed(Event(7, DistanceUnits.Mile), Time(1, TimeUnits.Hour))
        self.AssertPaceToSpeedConversion(pace, expectedSpeed)

        pace = Pace(Time(7.5, TimeUnits.Minute), Event(1, DistanceUnits.KM))
        expectedSpeed = Speed(Event(8, DistanceUnits.KM), Time(1, TimeUnits.Hour))
        self.AssertPaceToSpeedConversion(pace, expectedSpeed)


if __name__ == '__main__':
    unittest.main()
