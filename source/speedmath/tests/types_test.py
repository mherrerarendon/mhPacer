import pytest
from source.speedmath.errCodes import smException, errCodes
from source.speedmath.types import Speed, Pace, Event, Time, GetValueAndUnitFromStr
from source.speedmath.common import DistanceUnits, TimeUnits


def assertFuncRaisesException(func, theErrorCode):
    with pytest.raises(smException) as e:
        func()
    assert e.value.error_code == theErrorCode

def test_parseDistanceUnit():
    assertFuncRaisesException(lambda: Event.parseDistanceUnit(None), errCodes.DISTANCE_UNIT_PARSE_ERR)
    assertFuncRaisesException(lambda: Event.parseDistanceUnit(''), errCodes.DISTANCE_UNIT_PARSE_ERR)
    assertFuncRaisesException(lambda: Event.parseDistanceUnit('1'), errCodes.DISTANCE_UNIT_PARSE_ERR)

    assert Event.parseDistanceUnit('kilometer') == DistanceUnits.KM
    assert Event.parseDistanceUnit('kilometers') == DistanceUnits.KM

    assert Event.parseDistanceUnit('mile') == DistanceUnits.Mile
    assert Event.parseDistanceUnit('miles') == DistanceUnits.Mile

    assert Event.parseDistanceUnit('meter') == DistanceUnits.Meter
    assert Event.parseDistanceUnit('meters') == DistanceUnits.Meter

    assert Event.parseDistanceUnit('m', TimeUnits.Second) == DistanceUnits.Meter
    assert Event.parseDistanceUnit('m', TimeUnits.Hour) == DistanceUnits.Mile
    assert Event.parseDistanceUnit('M') == DistanceUnits.Meter
    assert Event.parseDistanceUnit('k') == DistanceUnits.KM

def test_parseTimeUnit():
    assertFuncRaisesException(lambda: Time.parseTimeUnit(None), errCodes.TIME_UNIT_PARSE_ERR)
    assertFuncRaisesException(lambda: Time.parseTimeUnit(''), errCodes.TIME_UNIT_PARSE_ERR)
    assertFuncRaisesException(lambda: Time.parseTimeUnit('t'), errCodes.TIME_UNIT_PARSE_ERR)

    assert Time.parseTimeUnit('hour') == TimeUnits.Hour
    assert Time.parseTimeUnit('hours') == TimeUnits.Hour
    assert Time.parseTimeUnit('H') == TimeUnits.Hour
    assert Time.parseTimeUnit('h') == TimeUnits.Hour

    assert Time.parseTimeUnit('second') == TimeUnits.Second
    assert Time.parseTimeUnit('seconds') == TimeUnits.Second
    assert Time.parseTimeUnit('S') == TimeUnits.Second
    assert Time.parseTimeUnit('s') == TimeUnits.Second

    assert Time.parseTimeUnit('minute') == TimeUnits.Minute
    assert Time.parseTimeUnit('minutes') == TimeUnits.Minute
    assert Time.parseTimeUnit('M') == TimeUnits.Minute
    assert Time.parseTimeUnit('m') == TimeUnits.Minute

def test_parseSpeedString():
    speed = Speed.parseSpeedStr('12mph')
    assert speed == Speed(Event(12, DistanceUnits.Mile), Time(1, TimeUnits.Hour))

    speed = Speed.parseSpeedStr('12 mph')
    assert speed == Speed(Event(12, DistanceUnits.Mile), Time(1, TimeUnits.Hour))

    speed = Speed.parseSpeedStr('10 kilometer per hour')
    assert speed == Speed(Event(10, DistanceUnits.KM), Time(1, TimeUnits.Hour))

    speed = Speed.parseSpeedStr('10kph')
    assert speed == Speed(Event(10, DistanceUnits.KM), Time(1, TimeUnits.Hour))

    speed = Speed.parseSpeedStr('10mps')
    assert speed == Speed(Event(10, DistanceUnits.Meter), Time(1, TimeUnits.Second))

    speed = Speed.parseSpeedStr('12.5 mph')
    assert speed == Speed(Event(12.5, DistanceUnits.Mile), Time(1, TimeUnits.Hour))

def test_parseEventString():
    assert Event.parseEventStr('12m') == Event(12, DistanceUnits.Meter)
    assert Event.parseEventStr('10k') == Event(10, DistanceUnits.KM)

def test_getEventTimeDivider():
    assertFuncRaisesException(lambda: Speed.getEventTimeDivider('per per'), errCodes.PARSE_ERR)
    assertFuncRaisesException(lambda: Speed.getEventTimeDivider('p p'), errCodes.PARSE_ERR)
    assertFuncRaisesException(lambda: Speed.getEventTimeDivider('/ /'), errCodes.PARSE_ERR)

    assert Speed.getEventTimeDivider('per') == 'per'
    assert Speed.getEventTimeDivider('p') == 'p'
    assert Speed.getEventTimeDivider('/') == '/'

    assert Speed.getEventTimeDivider('something per something') == 'per'
    assert Speed.getEventTimeDivider('something p something') == 'p'
    assert Speed.getEventTimeDivider('something / something') == '/'

    assert Speed.getEventTimeDivider('somethingpersomething') == 'per'
    assert Speed.getEventTimeDivider('somethingpsomething') == 'p'
    assert Speed.getEventTimeDivider('something/something') == '/'

def assertValueAndUnitStr(actualValueUnitTuple, expectedValueUnitTuple):
    actualValue, actualUnitStr = actualValueUnitTuple
    expectedValue, expectedUnitStr = expectedValueUnitTuple
    assert actualValue == expectedValue
    assert actualUnitStr == expectedUnitStr

def test_GetValueAndUnitFromStr():
    assertValueAndUnitStr(GetValueAndUnitFromStr('12 miles'), (12, 'miles'))
    assertValueAndUnitStr(GetValueAndUnitFromStr('12miles'), (12, 'miles'))
    assertValueAndUnitStr(GetValueAndUnitFromStr('12m'), (12, 'm'))

    assertValueAndUnitStr(GetValueAndUnitFromStr('2 kilometers'), (2, 'kilometers'))
    assertValueAndUnitStr(GetValueAndUnitFromStr('2kilometers'), (2, 'kilometers'))
    assertValueAndUnitStr(GetValueAndUnitFromStr('2 k'), (2, 'k'))

    assertValueAndUnitStr(GetValueAndUnitFromStr('2 minutes'), (2, 'minutes'))
    assertValueAndUnitStr(GetValueAndUnitFromStr('2foo'), (2, 'foo'))

    assertValueAndUnitStr(GetValueAndUnitFromStr('2.1 minutes'), (2.1, 'minutes'))

def test_parsePaceStr():
    pace = Pace.parsePaceStr('12 minute mile')
    assert pace == Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile))

    pace = Pace.parsePaceStr('12 minutes per mile')
    assert pace == Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile))

    pace = Pace.parsePaceStr('12 min mile')
    assert pace == Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile))

    pace = Pace.parsePaceStr('12 min/mile')
    assert pace == Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile))

    pace = Pace.parsePaceStr('12min/mile')
    assert pace == Pace(Time(12, TimeUnits.Minute), Event(1, DistanceUnits.Mile))

    pace = Pace.parsePaceStr('12.1min/mile')
    assert pace == Pace(Time(12.1, TimeUnits.Minute), Event(1, DistanceUnits.Mile))
