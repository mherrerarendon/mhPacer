from ErrorCodes import RPCException, ErrorCodes
import json
import re
from Types import *


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

    @staticmethod
    def ParseEventStr(eventStr, timeUnit=None):
        match = re.search(r'(\d+)\s?(\S+)', eventStr)
        if match is None:
            raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse event string')
        event = Event()
        event.distance = Event.ParseDistanceStr(match.group(1))
        event.unit = Event.ParseDistanceUnit(match.group(2), timeUnit)
        return event

    @staticmethod
    def ParseDistanceStr(distanceStr):
        value = None
        if distanceStr is None:
            raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse value')
        try:
            value = int(distanceStr)
        except Exception:
            raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse value')
        return value

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

    def Serialize(self):
        serializeDistanceUnit = {DistanceUnits.Mile: 'mile',
                                 DistanceUnits.KM: 'kilometer',
                                 DistanceUnits.Meter: 'meter'}
        return {
            DISTANCE_KEY: self.distance,
            UNIT_KEY: serializeDistanceUnit[self.unit]
        }


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

    def ParseTimeStr(timeStr):
        time = Time()
        time.time = 1  # Assume 1 for time value for now
        time.unit = Time.ParseTimeUnit(timeStr)
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

    def Serialize(self):
        serializeTimeUnit = {TimeUnits.Hour: 'hour',
                             TimeUnits.Minute: 'minute',
                             TimeUnits.Second: 'second'}
        return {
            TIME_KEY: self.time,
            UNIT_KEY: serializeTimeUnit[self.unit]
        }


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
        reFormat = r'(\d+\s?\S+)\s?' + dividerStr + '\s?(\S+)'
        match = re.search(reFormat, speedStr)
        if match is None:
            raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse speed string')
        return match.group(1), match.group(2)

    @staticmethod
    def GetEventTimeDivider(speedStr):
        possibleDividers = [r'per', r'p', r'/']
        for divider in possibleDividers:
            reFormat = r'\s?' + divider + r'\s?'
            matchList = re.findall(reFormat, speedStr)
            if len(matchList) == 1:
                return divider
        raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse speed string')

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
