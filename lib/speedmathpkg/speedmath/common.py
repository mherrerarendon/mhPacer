from enum import Enum, unique, auto
import re
from speedmath.errCodes import smException, errCodes


@unique
class DistanceUnits(Enum):
    Mile = auto()
    KM = auto()
    Meter = auto()


@unique
class TimeUnits(Enum):
    Second = auto()
    Minute = auto()
    Hour = auto()


KM_PER_MILE = 1.61
MILE_PER_KM = 1 / KM_PER_MILE

SECONDS_PER_HOUR = 3600
HOURS_PER_SECOND = 1 / SECONDS_PER_HOUR

TIME_KEY = 'time'
EVENT_KEY = 'event'
DISTANCE_KEY = 'distance'
UNIT_KEY = 'unit'


def GetSpeedAndPaceReFormat(dividerStr=''):
    return GetValueAndUnitReFormat(forceNumberValues=True) + r'\s?' + dividerStr + r'\s?' + GetValueAndUnitReFormat(forceNumberValues=False)


def GetValueAndUnitReFormat(forceNumberValues=False, theStr=None):
    if forceNumberValues or (theStr is not None and re.search(r'\d', theStr)):
        return r'(\d+\.?\d*)\s?(\S+)'
    else:
        return r'(\S+)'


def GetValueAndUnitFromStr(parseStr):
    reFormat = GetValueAndUnitReFormat(forceNumberValues=False, theStr=parseStr)
    match = re.search(reFormat, parseStr)
    if match is None or len(match.groups()) > 2:
        raise smException(errCodes.PARSE_ERR, 'Could not parse event string')
    elif len(match.groups()) == 1:
        # The groups match is the units, and there is no number, which means 1
        value = 1
        unitStr = match.group(1)
    elif len(match.groups()) == 2:
        try:
            value = int(match.group(1))
        except ValueError:
            value = float(match.group(1))
        except Exception:
            raise smException(errCodes.PARSE_ERR, 'Could not parse value')
        unitStr = match.group(2)
    return value, unitStr
