import unittest

from speedmath.ErrorCodes import RPCException, ErrorCodes
from speedmath.SpeedStrParser import Speed, Pace, Event, Time, GetValueAndUnitFromStr
from speedmath.Types import DistanceUnits, TimeUnits


class TestSpeedStrParser(unittest.TestCase):
    def AssertFuncRaisesException(self, func, exception):
        with self.assertRaises(RPCException) as e:
            func()
        self.assertEqual(e.exception.error_code, exception)

    def test_Event_ParseDistanceUnit(self):
        self.AssertFuncRaisesException(lambda: Event.ParseDistanceUnit(None), ErrorCodes.DISTANCE_UNIT_PARSE_ERR)
        self.AssertFuncRaisesException(lambda: Event.ParseDistanceUnit(''), ErrorCodes.DISTANCE_UNIT_PARSE_ERR)
        self.AssertFuncRaisesException(lambda: Event.ParseDistanceUnit('1'), ErrorCodes.DISTANCE_UNIT_PARSE_ERR)

        self.assertEqual(Event.ParseDistanceUnit('kilometer'), DistanceUnits.KM)
        self.assertEqual(Event.ParseDistanceUnit('kilometers'), DistanceUnits.KM)

        self.assertEqual(Event.ParseDistanceUnit('mile'), DistanceUnits.Mile)
        self.assertEqual(Event.ParseDistanceUnit('miles'), DistanceUnits.Mile)

        self.assertEqual(Event.ParseDistanceUnit('meter'), DistanceUnits.Meter)
        self.assertEqual(Event.ParseDistanceUnit('meters'), DistanceUnits.Meter)

        self.assertEqual(Event.ParseDistanceUnit('m', TimeUnits.Second), DistanceUnits.Meter)
        self.assertEqual(Event.ParseDistanceUnit('m', TimeUnits.Hour), DistanceUnits.Mile)
        self.assertEqual(Event.ParseDistanceUnit('M'), DistanceUnits.Meter)
        self.assertEqual(Event.ParseDistanceUnit('k'), DistanceUnits.KM)

    def test_ParseTimeUnit(self):
        self.AssertFuncRaisesException(lambda: Time.ParseTimeUnit(None), ErrorCodes.TIME_UNIT_PARSE_ERR)
        self.AssertFuncRaisesException(lambda: Time.ParseTimeUnit(''), ErrorCodes.TIME_UNIT_PARSE_ERR)
        self.AssertFuncRaisesException(lambda: Time.ParseTimeUnit('t'), ErrorCodes.TIME_UNIT_PARSE_ERR)

        self.assertEqual(Time.ParseTimeUnit('hour'), TimeUnits.Hour)
        self.assertEqual(Time.ParseTimeUnit('hours'), TimeUnits.Hour)
        self.assertEqual(Time.ParseTimeUnit('H'), TimeUnits.Hour)
        self.assertEqual(Time.ParseTimeUnit('h'), TimeUnits.Hour)

        self.assertEqual(Time.ParseTimeUnit('second'), TimeUnits.Second)
        self.assertEqual(Time.ParseTimeUnit('seconds'), TimeUnits.Second)
        self.assertEqual(Time.ParseTimeUnit('S'), TimeUnits.Second)
        self.assertEqual(Time.ParseTimeUnit('s'), TimeUnits.Second)

        self.assertEqual(Time.ParseTimeUnit('minute'), TimeUnits.Minute)
        self.assertEqual(Time.ParseTimeUnit('minutes'), TimeUnits.Minute)
        self.assertEqual(Time.ParseTimeUnit('M'), TimeUnits.Minute)
        self.assertEqual(Time.ParseTimeUnit('m'), TimeUnits.Minute)

    def test_ParseSpeedString(self):
        speed = Speed.ParseSpeedStr('12mph')
        self.assertEqual(speed, Speed(Event(12, DistanceUnits.Mile), Time(1, TimeUnits.Hour)))

        speed = Speed.ParseSpeedStr('12 mph')
        self.assertEqual(speed, Speed(Event(12, DistanceUnits.Mile), Time(1, TimeUnits.Hour)))

        speed = Speed.ParseSpeedStr('10 kilometer per hour')
        self.assertEqual(speed, Speed(Event(10, DistanceUnits.KM), Time(1, TimeUnits.Hour)))

        speed = Speed.ParseSpeedStr('10kph')
        self.assertEqual(speed, Speed(Event(10, DistanceUnits.KM), Time(1, TimeUnits.Hour)))

        speed = Speed.ParseSpeedStr('10mps')
        self.assertEqual(speed, Speed(Event(10, DistanceUnits.Meter), Time(1, TimeUnits.Second)))

        speed = Speed.ParseSpeedStr('12.5 mph')
        self.assertEqual(speed, Speed(Event(12.5, DistanceUnits.Mile), Time(1, TimeUnits.Hour)))

    def test_ParseEventString(self):
        self.assertEqual(Event.ParseEventStr('12m'), Event(12, DistanceUnits.Meter))
        self.assertEqual(Event.ParseEventStr('10k'), Event(10, DistanceUnits.KM))

    def test_GetEventTimeDivider(self):
        self.AssertFuncRaisesException(lambda: Speed.GetEventTimeDivider('per per'), ErrorCodes.PARSE_ERR)
        self.AssertFuncRaisesException(lambda: Speed.GetEventTimeDivider('p p'), ErrorCodes.PARSE_ERR)
        self.AssertFuncRaisesException(lambda: Speed.GetEventTimeDivider('/ /'), ErrorCodes.PARSE_ERR)

        self.assertEqual(Speed.GetEventTimeDivider('per'), 'per')
        self.assertEqual(Speed.GetEventTimeDivider('p'), 'p')
        self.assertEqual(Speed.GetEventTimeDivider('/'), '/')

        self.assertEqual(Speed.GetEventTimeDivider('something per something'), 'per')
        self.assertEqual(Speed.GetEventTimeDivider('something p something'), 'p')
        self.assertEqual(Speed.GetEventTimeDivider('something / something'), '/')

        self.assertEqual(Speed.GetEventTimeDivider('somethingpersomething'), 'per')
        self.assertEqual(Speed.GetEventTimeDivider('somethingpsomething'), 'p')
        self.assertEqual(Speed.GetEventTimeDivider('something/something'), '/')

    def AssertValueAndUnitStr(self, actualValueUnitTuple, expectedValueUnitTuple):
        actualValue, actualUnitStr = actualValueUnitTuple
        expectedValue, expectedUnitStr = expectedValueUnitTuple
        self.assertEqual(actualValue, expectedValue)
        self.assertEqual(actualUnitStr, expectedUnitStr)

    def test_GetValueAndUnitFromStr(self):
        self.AssertValueAndUnitStr(GetValueAndUnitFromStr('12 miles'), (12, 'miles'))
        self.AssertValueAndUnitStr(GetValueAndUnitFromStr('12miles'), (12, 'miles'))
        self.AssertValueAndUnitStr(GetValueAndUnitFromStr('12m'), (12, 'm'))

        self.AssertValueAndUnitStr(GetValueAndUnitFromStr('2 kilometers'), (2, 'kilometers'))
        self.AssertValueAndUnitStr(GetValueAndUnitFromStr('2kilometers'), (2, 'kilometers'))
        self.AssertValueAndUnitStr(GetValueAndUnitFromStr('2 k'), (2, 'k'))

        self.AssertValueAndUnitStr(GetValueAndUnitFromStr('2 minutes'), (2, 'minutes'))
        self.AssertValueAndUnitStr(GetValueAndUnitFromStr('2foo'), (2, 'foo'))

        self.AssertValueAndUnitStr(GetValueAndUnitFromStr('2.1 minutes'), (2.1, 'minutes'))

    def test_ParsePaceStr(self):
        pace = Pace.ParsePaceStr('12 minute mile')
        self.assertEqual(pace, Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile)))

        pace = Pace.ParsePaceStr('12 minutes per mile')
        self.assertEqual(pace, Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile)))

        pace = Pace.ParsePaceStr('12 min mile')
        self.assertEqual(pace, Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile)))

        pace = Pace.ParsePaceStr('12 min/mile')
        self.assertEqual(pace, Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile)))

        pace = Pace.ParsePaceStr('12min/mile')
        self.assertEqual(pace, Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile)))

        pace = Pace.ParsePaceStr('12.1min/mile')
        self.assertEqual(pace, Pace(Time(12.1, TimeUnits.Minute), Event(1, DistanceUnits.Mile)))


if __name__ == '__main__':
    unittest.main()
