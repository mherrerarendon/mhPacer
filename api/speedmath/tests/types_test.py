import unittest

from speedmath.errCodes import smException, errCodes
from speedmath.types import Speed, Pace, Event, Time, GetValueAndUnitFromStr
from speedmath.common import DistanceUnits, TimeUnits


class TestSpeedStrParser(unittest.TestCase):
    def assertFuncRaisesException(self, func, exception):
        with self.assertRaises(smException) as e:
            func()
        self.assertEqual(e.exception.error_code, exception)

    def test_parseDistanceUnit(self):
        self.assertFuncRaisesException(lambda: Event.parseDistanceUnit(None), errCodes.DISTANCE_UNIT_PARSE_ERR)
        self.assertFuncRaisesException(lambda: Event.parseDistanceUnit(''), errCodes.DISTANCE_UNIT_PARSE_ERR)
        self.assertFuncRaisesException(lambda: Event.parseDistanceUnit('1'), errCodes.DISTANCE_UNIT_PARSE_ERR)

        self.assertEqual(Event.parseDistanceUnit('kilometer'), DistanceUnits.KM)
        self.assertEqual(Event.parseDistanceUnit('kilometers'), DistanceUnits.KM)

        self.assertEqual(Event.parseDistanceUnit('mile'), DistanceUnits.Mile)
        self.assertEqual(Event.parseDistanceUnit('miles'), DistanceUnits.Mile)

        self.assertEqual(Event.parseDistanceUnit('meter'), DistanceUnits.Meter)
        self.assertEqual(Event.parseDistanceUnit('meters'), DistanceUnits.Meter)

        self.assertEqual(Event.parseDistanceUnit('m', TimeUnits.Second), DistanceUnits.Meter)
        self.assertEqual(Event.parseDistanceUnit('m', TimeUnits.Hour), DistanceUnits.Mile)
        self.assertEqual(Event.parseDistanceUnit('M'), DistanceUnits.Meter)
        self.assertEqual(Event.parseDistanceUnit('k'), DistanceUnits.KM)

    def test_parseTimeUnit(self):
        self.assertFuncRaisesException(lambda: Time.parseTimeUnit(None), errCodes.TIME_UNIT_PARSE_ERR)
        self.assertFuncRaisesException(lambda: Time.parseTimeUnit(''), errCodes.TIME_UNIT_PARSE_ERR)
        self.assertFuncRaisesException(lambda: Time.parseTimeUnit('t'), errCodes.TIME_UNIT_PARSE_ERR)

        self.assertEqual(Time.parseTimeUnit('hour'), TimeUnits.Hour)
        self.assertEqual(Time.parseTimeUnit('hours'), TimeUnits.Hour)
        self.assertEqual(Time.parseTimeUnit('H'), TimeUnits.Hour)
        self.assertEqual(Time.parseTimeUnit('h'), TimeUnits.Hour)

        self.assertEqual(Time.parseTimeUnit('second'), TimeUnits.Second)
        self.assertEqual(Time.parseTimeUnit('seconds'), TimeUnits.Second)
        self.assertEqual(Time.parseTimeUnit('S'), TimeUnits.Second)
        self.assertEqual(Time.parseTimeUnit('s'), TimeUnits.Second)

        self.assertEqual(Time.parseTimeUnit('minute'), TimeUnits.Minute)
        self.assertEqual(Time.parseTimeUnit('minutes'), TimeUnits.Minute)
        self.assertEqual(Time.parseTimeUnit('M'), TimeUnits.Minute)
        self.assertEqual(Time.parseTimeUnit('m'), TimeUnits.Minute)

    def test_parseSpeedString(self):
        speed = Speed.parseSpeedStr('12mph')
        self.assertEqual(speed, Speed(Event(12, DistanceUnits.Mile), Time(1, TimeUnits.Hour)))

        speed = Speed.parseSpeedStr('12 mph')
        self.assertEqual(speed, Speed(Event(12, DistanceUnits.Mile), Time(1, TimeUnits.Hour)))

        speed = Speed.parseSpeedStr('10 kilometer per hour')
        self.assertEqual(speed, Speed(Event(10, DistanceUnits.KM), Time(1, TimeUnits.Hour)))

        speed = Speed.parseSpeedStr('10kph')
        self.assertEqual(speed, Speed(Event(10, DistanceUnits.KM), Time(1, TimeUnits.Hour)))

        speed = Speed.parseSpeedStr('10mps')
        self.assertEqual(speed, Speed(Event(10, DistanceUnits.Meter), Time(1, TimeUnits.Second)))

        speed = Speed.parseSpeedStr('12.5 mph')
        self.assertEqual(speed, Speed(Event(12.5, DistanceUnits.Mile), Time(1, TimeUnits.Hour)))

    def test_parseEventString(self):
        self.assertEqual(Event.parseEventStr('12m'), Event(12, DistanceUnits.Meter))
        self.assertEqual(Event.parseEventStr('10k'), Event(10, DistanceUnits.KM))

    def test_getEventTimeDivider(self):
        self.assertFuncRaisesException(lambda: Speed.getEventTimeDivider('per per'), errCodes.PARSE_ERR)
        self.assertFuncRaisesException(lambda: Speed.getEventTimeDivider('p p'), errCodes.PARSE_ERR)
        self.assertFuncRaisesException(lambda: Speed.getEventTimeDivider('/ /'), errCodes.PARSE_ERR)

        self.assertEqual(Speed.getEventTimeDivider('per'), 'per')
        self.assertEqual(Speed.getEventTimeDivider('p'), 'p')
        self.assertEqual(Speed.getEventTimeDivider('/'), '/')

        self.assertEqual(Speed.getEventTimeDivider('something per something'), 'per')
        self.assertEqual(Speed.getEventTimeDivider('something p something'), 'p')
        self.assertEqual(Speed.getEventTimeDivider('something / something'), '/')

        self.assertEqual(Speed.getEventTimeDivider('somethingpersomething'), 'per')
        self.assertEqual(Speed.getEventTimeDivider('somethingpsomething'), 'p')
        self.assertEqual(Speed.getEventTimeDivider('something/something'), '/')

    def assertValueAndUnitStr(self, actualValueUnitTuple, expectedValueUnitTuple):
        actualValue, actualUnitStr = actualValueUnitTuple
        expectedValue, expectedUnitStr = expectedValueUnitTuple
        self.assertEqual(actualValue, expectedValue)
        self.assertEqual(actualUnitStr, expectedUnitStr)

    def test_GetValueAndUnitFromStr(self):
        self.assertValueAndUnitStr(GetValueAndUnitFromStr('12 miles'), (12, 'miles'))
        self.assertValueAndUnitStr(GetValueAndUnitFromStr('12miles'), (12, 'miles'))
        self.assertValueAndUnitStr(GetValueAndUnitFromStr('12m'), (12, 'm'))

        self.assertValueAndUnitStr(GetValueAndUnitFromStr('2 kilometers'), (2, 'kilometers'))
        self.assertValueAndUnitStr(GetValueAndUnitFromStr('2kilometers'), (2, 'kilometers'))
        self.assertValueAndUnitStr(GetValueAndUnitFromStr('2 k'), (2, 'k'))

        self.assertValueAndUnitStr(GetValueAndUnitFromStr('2 minutes'), (2, 'minutes'))
        self.assertValueAndUnitStr(GetValueAndUnitFromStr('2foo'), (2, 'foo'))

        self.assertValueAndUnitStr(GetValueAndUnitFromStr('2.1 minutes'), (2.1, 'minutes'))

    def test_parsePaceStr(self):
        pace = Pace.parsePaceStr('12 minute mile')
        self.assertEqual(pace, Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile)))

        pace = Pace.parsePaceStr('12 minutes per mile')
        self.assertEqual(pace, Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile)))

        pace = Pace.parsePaceStr('12 min mile')
        self.assertEqual(pace, Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile)))

        pace = Pace.parsePaceStr('12 min/mile')
        self.assertEqual(pace, Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile)))

        pace = Pace.parsePaceStr('12min/mile')
        self.assertEqual(pace, Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile)))

        pace = Pace.parsePaceStr('12.1min/mile')
        self.assertEqual(pace, Pace(Time(12.1, TimeUnits.Minute), Event(1, DistanceUnits.Mile)))


if __name__ == '__main__':
    unittest.main()
