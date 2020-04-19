import unittest

from ErrorCodes import RPCException, ErrorCodes
from SpeedStrParser import *
from Types import *


class TestStringMethods(unittest.TestCase):
    def AssertFuncRaisesException(self, func, exception):
        with self.assertRaises(RPCException) as e:
            func()
        self.assertEqual(e.exception.error_code, exception)

    def test_Event_ParseDistanceStr(self):
        self.AssertFuncRaisesException(lambda: Event.ParseDistanceStr(None), ErrorCodes.PARSE_ERR)
        self.AssertFuncRaisesException(lambda: Event.ParseDistanceStr(''), ErrorCodes.PARSE_ERR)
        self.AssertFuncRaisesException(lambda: Event.ParseDistanceStr('d'), ErrorCodes.PARSE_ERR)
        self.assertEqual(Event.ParseDistanceStr('12'), 12)

    def test_Event_ParseDistanceUnit(self):
        self.AssertFuncRaisesException(lambda: Event.ParseDistanceUnit(None), ErrorCodes.DISTANCE_UNIT_PARSE_ERR)
        self.AssertFuncRaisesException(lambda: Event.ParseDistanceUnit(''), ErrorCodes.DISTANCE_UNIT_PARSE_ERR)
        self.AssertFuncRaisesException(lambda: Event.ParseDistanceUnit('1'), ErrorCodes.DISTANCE_UNIT_PARSE_ERR)
        self.assertEqual(Event.ParseDistanceUnit('m'), DistanceUnits.Mile)
        self.assertEqual(Event.ParseDistanceUnit('M'), DistanceUnits.Mile)
        self.assertEqual(Event.ParseDistanceUnit('k'), DistanceUnits.KM)

    def test_ParseTimeUnit(self):
        self.AssertFuncRaisesException(lambda: Time.ParseTimeUnit(None), ErrorCodes.TIME_UNIT_PARSE_ERR)
        self.AssertFuncRaisesException(lambda: Time.ParseTimeUnit(''), ErrorCodes.TIME_UNIT_PARSE_ERR)
        self.AssertFuncRaisesException(lambda: Time.ParseTimeUnit('t'), ErrorCodes.TIME_UNIT_PARSE_ERR)
        self.assertEqual(Time.ParseTimeUnit('h'), TimeUnits.Hour)
        self.assertEqual(Time.ParseTimeUnit('H'), TimeUnits.Hour)
        self.assertEqual(Time.ParseTimeUnit('s'), TimeUnits.Second)

    def test_ParseSpeedString(self):
        speed = Speed.ParseSpeedStr('12mph')
        self.assertEqual(speed.event.distance, 12)
        self.assertEqual(speed.event.unit, DistanceUnits.Mile)
        self.assertEqual(speed.time.time, 1)
        self.assertEqual(speed.time.unit, TimeUnits.Hour)

    def test_ParseEventString(self):
        event = Event.ParseEventStr('12m')
        self.assertEqual(event.distance, 12)
        self.assertEqual(event.unit, DistanceUnits.Mile)


if __name__ == '__main__':
    unittest.main()
