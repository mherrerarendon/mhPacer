from ErrorCodes import RPCException, ErrorCodes
import re
from Types import *


class Event:
    def __init__(self):
        self.distance = 0
        self.unit = None

    @staticmethod
    def ParseEventStr(eventStr):
        match = re.search(r'(\d+)(\S)', eventStr)
        if match is None:
            raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse event string')
        event = Event()
        event.distance = Event.ParseDistanceStr(match.group(1))
        event.unit = Event.ParseDistanceUnit(match.group(2))
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
    def ParseDistanceUnit(distanceUnitStr):
        if distanceUnitStr is None:
            raise RPCException(ErrorCodes.DISTANCE_UNIT_PARSE_ERR, 'Could not parse distance unit')
        distanceStrToEnum = {'m': DistanceUnits.Mile, 'k': DistanceUnits.KM}
        if distanceUnitStr.lower() not in distanceStrToEnum:
            raise RPCException(ErrorCodes.DISTANCE_UNIT_PARSE_ERR, 'Could not parse distance unit')
        return distanceStrToEnum[distanceUnitStr.lower()]

    def Serialize(self):
        serializeDistanceUnit = {DistanceUnits.Mile: 'mile', DistanceUnits.KM: 'kilometer'}
        return {
            DISTANCE_KEY: self.distance,
            UNIT_KEY: serializeDistanceUnit[self.unit],
        }


class Time:
    def __init__(self):
        self.time = 0
        self.unit = None

    def ParseTimeStr(timeStr):
        time = Time()
        time.time = 1  # Assume 1 for time value for now
        time.unit = Time.ParseTimeUnit(timeStr)
        return time

    @staticmethod
    def ParseTimeUnit(timeUnitStr):
        if timeUnitStr is None:
            raise RPCException(ErrorCodes.TIME_UNIT_PARSE_ERR, 'Could not parse time unit')
        timeStrToEnum = {'h': TimeUnits.Hour, 's': TimeUnits.Second}
        if timeUnitStr.lower() not in timeStrToEnum:
            raise RPCException(ErrorCodes.TIME_UNIT_PARSE_ERR, 'Could not parse time unit')
        return timeStrToEnum[timeUnitStr.lower()]

    def Serialize(self):
        serializeTimeUnit = {TimeUnits.Hour: 'hour', TimeUnits.Second: 'second'}
        return {
            TIME_KEY: self.time,
            UNIT_KEY: serializeTimeUnit[self.unit]
        }


class Speed:
    def __init__(self):
        self.event = Event()
        self.time = Time()

    @staticmethod
    def ParseSpeedStr(speedStr):
        eventStr, timeStr = Speed.GetEventAndTimeStr(speedStr)
        speed = Speed()
        speed.event = Event.ParseEventStr(eventStr)
        speed.time = Time.ParseTimeStr(timeStr)
        return speed

    @staticmethod
    def GetEventAndTimeStr(speedStr):
        match = re.search(r'(\d+\S)p(\S)', speedStr)
        if match is None:
            raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse speed string')
        return match.group(1), match.group(2)

    def Serialize(self):
        return {
            EVENT_KEY: self.event.Serialize(),
            TIME_KEY: self.time.Serialize()
        }
