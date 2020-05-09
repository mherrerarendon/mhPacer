from ErrorCodes import RPCException, ErrorCodes
import json
import re
from Types import *


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
        raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse event string')
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
            raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse value')
        unitStr = match.group(2)
    return value, unitStr


class Event:
    def __init__(self, distance=0, unit=None):
        self.distance = distance
        self.unit = unit

    def __repr__(self):
        return json.dumps(self.Serialize())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.distance == other.distance and
                self.unit == other.unit)
        else:
            return False

    def Serialize(self):
        serializeDistanceUnit = {DistanceUnits.Mile: 'mile',
                                 DistanceUnits.KM: 'kilometer',
                                 DistanceUnits.Meter: 'meter'}
        return {
            DISTANCE_KEY: self.distance,
            UNIT_KEY: serializeDistanceUnit[self.unit]
        }

    @staticmethod
    def ParseEventStr(eventStr, timeUnit=None):
        distance, unitStr = GetValueAndUnitFromStr(eventStr)
        event = Event()
        event.distance = distance
        event.unit = Event.ParseDistanceUnit(unitStr, timeUnit)
        return event

    @staticmethod
    def ParseDistanceUnit(distanceUnitStr, timeUnit=None):
        if distanceUnitStr is None:
            raise RPCException(ErrorCodes.DISTANCE_UNIT_PARSE_ERR, 'Could not parse distance unit')
        distanceStrToEnum = {'mile': DistanceUnits.Mile,
                             'kilometer': DistanceUnits.KM,
                             'meter': DistanceUnits.Meter,
                             'km': DistanceUnits.KM,
                             'k': DistanceUnits.KM,
                             'm': DistanceUnits.Meter if timeUnit == TimeUnits.Second or timeUnit is None else DistanceUnits.Mile}
        for unitStr, unit in distanceStrToEnum.items():
            if unitStr in distanceUnitStr.lower():
                return unit
        raise RPCException(ErrorCodes.DISTANCE_UNIT_PARSE_ERR, 'Could not parse distance unit')


class Time:
    def __init__(self, time=0, unit=None):
        self.time = time
        self.unit = unit

    def __repr__(self):
        return json.dumps(self.Serialize())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                    self.time == other.time and
                    self.unit == other.unit)
        else:
            return False

    def Serialize(self):
        serializeTimeUnit = {TimeUnits.Hour: 'hour',
                             TimeUnits.Minute: 'minute',
                             TimeUnits.Second: 'second'}
        return {
            TIME_KEY: self.time,
            UNIT_KEY: serializeTimeUnit[self.unit]
        }

    def ParseTimeStr(timeStr):
        timeVal, unitStr = GetValueAndUnitFromStr(timeStr)
        time = Time()
        time.time = timeVal
        time.unit = Time.ParseTimeUnit(unitStr)
        return time

    @staticmethod
    def ParseTimeUnit(timeUnitStr):
        if timeUnitStr is None:
            raise RPCException(ErrorCodes.TIME_UNIT_PARSE_ERR, 'Could not parse time unit')
        timeStrToEnum = {'hour': TimeUnits.Hour,
                         'second': TimeUnits.Second,
                         'minute': TimeUnits.Minute,
                         'h': TimeUnits.Hour,
                         's': TimeUnits.Second,
                         'm': TimeUnits.Minute}
        for unitStr, unit in timeStrToEnum.items():
            if unitStr in timeUnitStr.lower():
                return unit
        raise RPCException(ErrorCodes.TIME_UNIT_PARSE_ERR, 'Could not parse time unit')


class Speed:
    def __init__(self, event=None, time=None):
        self.event = Event() if event is None else event
        self.time = Time() if time is None else time

    def __repr__(self):
        return json.dumps(self.Serialize())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.event == other.event and
                self.time == other.time)
        else:
            return False

    def Serialize(self):
        return {
            EVENT_KEY: self.event.Serialize(),
            TIME_KEY: self.time.Serialize()
        }

    def Normalize(self):
        timeValue = self.time.time
        self.event.distance /= timeValue
        self.time.time /= timeValue
        return self

    @staticmethod
    def ParseSpeedStr(speedStr):
        eventStr, timeStr = Speed.GetEventAndTimeStr(speedStr)
        speed = Speed()
        speed.time = Time.ParseTimeStr(timeStr)
        speed.event = Event.ParseEventStr(eventStr, speed.time.unit)
        return speed

    @staticmethod
    def GetEventAndTimeStr(speedStr):
        dividerStr = Speed.GetEventTimeDivider(speedStr)
        reFormat = GetSpeedAndPaceReFormat(dividerStr)
        match = re.search(reFormat, speedStr)
        if match is None:
            raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse speed string')
        return match.group(1) + match.group(2), match.group(3)

    @staticmethod
    def GetEventTimeDivider(speedStr):
        possibleDividers = [r'per', r'p', r'/']
        for divider in possibleDividers:
            reFormat = r'\s?' + divider + r'\s?'
            matchList = re.findall(reFormat, speedStr)
            if len(matchList) == 1:
                return divider
        raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse speed string')


class Pace:
    def __init__(self, time=None, event=None):
        self.time = Time() if time is None else time
        self.event = Event() if event is None else event

    def __repr__(self):
        return json.dumps(self.Serialize())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.time == other.time and
                self.event == other.event)
        else:
            return False

    def Serialize(self):
        return {
            TIME_KEY: self.time.Serialize(),
            EVENT_KEY: self.event.Serialize()
        }

    def Normalize(self):
        distanceValue = self.event.distance
        self.time.time /= distanceValue
        self.event.distance /= distanceValue
        return self

    @staticmethod
    def GetTimeEventDivider(paceStr):
        possibleDividers = [r'per', r'p', r'/']
        for divider in possibleDividers:
            reFormat = r'\s?' + divider + r'\s?'
            matchList = re.findall(reFormat, paceStr)
            if len(matchList) == 1:
                return divider
        return ''

    @staticmethod
    def GetTimeAndEventStr(paceStr):
        dividerStr = Pace.GetTimeEventDivider(paceStr)
        reFormat = GetSpeedAndPaceReFormat(dividerStr)
        match = re.search(reFormat, paceStr)
        if match is None:
            raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse pace string')
        return match.group(1) + match.group(2), match.group(3)

    @staticmethod
    def ParsePaceStr(paceStr):
        timeStr, eventStr = Pace.GetTimeAndEventStr(paceStr)
        pace = Pace()
        pace.time = Time.ParseTimeStr(timeStr)
        pace.event = Event.ParseEventStr(eventStr, pace.time.unit)
        return pace
