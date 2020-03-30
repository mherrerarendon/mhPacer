import unittest

from ErrorCodes import RPCException, ErrorCodes
from SpeedStrParser import SpeedStrParser
from Types import *


class TestStringMethods(unittest.TestCase):
    def AssertFuncRaisesException(self, func, exception):
        with self.assertRaises(RPCException) as e:
            func()
        self.assertEqual(e.exception.error_code, exception)

    def test_ParseValue(self):
        self.AssertFuncRaisesException(lambda: SpeedStrParser.ParseValue(None), ErrorCodes.PARSE_ERR)
        self.AssertFuncRaisesException(lambda: SpeedStrParser.ParseValue(''), ErrorCodes.PARSE_ERR)
        self.AssertFuncRaisesException(lambda: SpeedStrParser.ParseValue('d'), ErrorCodes.PARSE_ERR)
        self.assertEqual(SpeedStrParser.ParseValue('12'), 12)

    def test_ParseDistanceUnit(self):
        self.AssertFuncRaisesException(lambda: SpeedStrParser.ParseDistanceUnit(None), ErrorCodes.DISTANCE_UNIT_PARSE_ERR)
        self.AssertFuncRaisesException(lambda: SpeedStrParser.ParseDistanceUnit(''), ErrorCodes.DISTANCE_UNIT_PARSE_ERR)
        self.AssertFuncRaisesException(lambda: SpeedStrParser.ParseDistanceUnit('1'), ErrorCodes.DISTANCE_UNIT_PARSE_ERR)
        self.assertEqual(SpeedStrParser.ParseDistanceUnit('m'), DistanceUnits.Mile)
        self.assertEqual(SpeedStrParser.ParseDistanceUnit('M'), DistanceUnits.Mile)
        self.assertEqual(SpeedStrParser.ParseDistanceUnit('k'), DistanceUnits.KM)

    def test_ParseTimeUnit(self):
        self.AssertFuncRaisesException(lambda: SpeedStrParser.ParseTimeUnit(None), ErrorCodes.TIME_UNIT_PARSE_ERR)
        self.AssertFuncRaisesException(lambda: SpeedStrParser.ParseTimeUnit(''), ErrorCodes.TIME_UNIT_PARSE_ERR)
        self.AssertFuncRaisesException(lambda: SpeedStrParser.ParseTimeUnit('t'), ErrorCodes.TIME_UNIT_PARSE_ERR)
        self.assertEqual(SpeedStrParser.ParseTimeUnit('h'), TimeUnits.Hour)
        self.assertEqual(SpeedStrParser.ParseTimeUnit('H'), TimeUnits.Hour)
        self.assertEqual(SpeedStrParser.ParseTimeUnit('s'), TimeUnits.Second)

    def test_ParseSpeedString(self):
        speed = SpeedStrParser.Parse('12mph')
        self.assertEqual(speed[DISTANCE_KEY], 12)
        self.assertEqual(speed[DISTANCE_UNIT_KEY], DistanceUnits.Mile)
        self.assertEqual(speed[TIME_KEY], 1)
        self.assertEqual(speed[TIME_UNIT_KEY], TimeUnits.Hour)


if __name__ == '__main__':
    unittest.main()
