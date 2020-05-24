import json
import re
from .common import DistanceUnits, TimeUnits, DISTANCE_KEY, TIME_KEY, UNIT_KEY, EVENT_KEY, GetValueAndUnitFromStr, GetSpeedAndPaceReFormat
from .errCodes import smException, errCodes


class Event:
    def __init__(self, distance=0, unit=None):
        self.distance = distance
        self.unit = unit

    def __repr__(self):
        return json.dumps(self.serialize())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.distance == other.distance and
                    self.unit == other.unit)
        else:
            return False

    def serialize(self):
        serializeDistanceUnit = {DistanceUnits.Mile: 'mile',
                                 DistanceUnits.KM: 'kilometer',
                                 DistanceUnits.Meter: 'meter'}
        return {
            DISTANCE_KEY: self.distance,
            UNIT_KEY: serializeDistanceUnit[self.unit]
        }

    @staticmethod
    def parseEventStr(eventStr, timeUnit=None):
        distance, unitStr = GetValueAndUnitFromStr(eventStr)
        event = Event()
        event.distance = distance
        event.unit = Event.parseDistanceUnit(unitStr, timeUnit)
        return event

    @staticmethod
    def parseDistanceUnit(distanceUnitStr, timeUnit=None):
        if distanceUnitStr is None:
            raise smException(errCodes.DISTANCE_UNIT_PARSE_ERR, 'Could not parse distance unit')
        distanceUnitStr = distanceUnitStr.lower()
        distanceStrToEnum = {'mile': DistanceUnits.Mile,
                             'kilometer': DistanceUnits.KM,
                             'meter': DistanceUnits.Meter,
                             'km': DistanceUnits.KM,
                             'k': DistanceUnits.KM,
                             'm': DistanceUnits.Meter if timeUnit == TimeUnits.Second or timeUnit is None else DistanceUnits.Mile}
        for unitStr, unit in distanceStrToEnum.items():
            if distanceUnitStr.lower().startswith(unitStr):
                return unit
        raise smException(errCodes.DISTANCE_UNIT_PARSE_ERR, 'Could not parse distance unit')


class Time:
    def __init__(self, time=0, unit=None):
        self.time = time
        self.unit = unit

    def __repr__(self):
        return json.dumps(self.serialize())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.time == other.time and
                    self.unit == other.unit)
        else:
            return False

    def serialize(self):
        serializeTimeUnit = {TimeUnits.Hour: 'hour',
                             TimeUnits.Minute: 'minute',
                             TimeUnits.Second: 'second'}
        return {
            TIME_KEY: self.time,
            UNIT_KEY: serializeTimeUnit[self.unit]
        }

    def parseTimeStr(timeStr):
        timeVal, unitStr = GetValueAndUnitFromStr(timeStr)
        time = Time()
        time.time = timeVal
        time.unit = Time.parseTimeUnit(unitStr)
        return time

    @staticmethod
    def parseTimeUnit(timeUnitStr):
        if timeUnitStr is None:
            raise smException(errCodes.TIME_UNIT_PARSE_ERR, 'Could not parse time unit')
        timeStrToEnum = {'hour': TimeUnits.Hour,
                         'second': TimeUnits.Second,
                         'minute': TimeUnits.Minute,
                         'h': TimeUnits.Hour,
                         's': TimeUnits.Second,
                         'm': TimeUnits.Minute}
        for unitStr, unit in timeStrToEnum.items():
            if unitStr in timeUnitStr.lower():
                return unit
        raise smException(errCodes.TIME_UNIT_PARSE_ERR, 'Could not parse time unit')


class Speed:
    def __init__(self, event=None, time=None):
        self.event = Event() if event is None else event
        self.time = Time() if time is None else time

    def __repr__(self):
        return json.dumps(self.serialize())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.event == other.event and
                    self.time == other.time)
        else:
            return False

    def serialize(self):
        return {
            EVENT_KEY: self.event.serialize(),
            TIME_KEY: self.time.serialize()
        }

    def normalize(self):
        timeValue = self.time.time
        self.event.distance /= timeValue
        self.time.time /= timeValue
        return self

    @staticmethod
    def parseSpeedStr(speedStr):
        eventStr, timeStr = Speed.getEventAndTimeStr(speedStr)
        speed = Speed()
        speed.time = Time.parseTimeStr(timeStr)
        speed.event = Event.parseEventStr(eventStr, speed.time.unit)
        return speed

    @staticmethod
    def getEventAndTimeStr(speedStr):
        dividerStr = Speed.getEventTimeDivider(speedStr)
        reFormat = GetSpeedAndPaceReFormat(dividerStr)
        match = re.search(reFormat, speedStr)
        if match is None:
            raise smException(errCodes.PARSE_ERR, 'Could not parse speed string')
        return match.group(1) + match.group(2), match.group(3)

    @staticmethod
    def getEventTimeDivider(speedStr):
        possibleDividers = [r'per', r'p', r'/']
        for divider in possibleDividers:
            reFormat = r'\s?' + divider + r'\s?'
            matchList = re.findall(reFormat, speedStr)
            if len(matchList) == 1:
                return divider
        raise smException(errCodes.PARSE_ERR, 'Could not parse speed string')


class Pace:
    def __init__(self, time=None, event=None):
        self.time = Time() if time is None else time
        self.event = Event() if event is None else event

    def __repr__(self):
        return json.dumps(self.serialize())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.time == other.time and
                    self.event == other.event)
        else:
            return False

    def serialize(self):
        return {
            TIME_KEY: self.time.serialize(),
            EVENT_KEY: self.event.serialize()
        }

    def normalize(self):
        distanceValue = self.event.distance
        self.time.time /= distanceValue
        self.event.distance /= distanceValue
        return self

    @staticmethod
    def getTimeEventDivider(paceStr):
        possibleDividers = [r'per', r'p', r'/']
        for divider in possibleDividers:
            reFormat = r'\s?' + divider + r'\s?'
            matchList = re.findall(reFormat, paceStr)
            if len(matchList) == 1:
                return divider
        return ''

    @staticmethod
    def getTimeAndEventStr(paceStr):
        dividerStr = Pace.getTimeEventDivider(paceStr)
        reFormat = GetSpeedAndPaceReFormat(dividerStr)
        match = re.search(reFormat, paceStr)
        if match is None:
            raise smException(errCodes.PARSE_ERR, 'Could not parse pace string')
        return match.group(1) + match.group(2), match.group(3)

    @staticmethod
    def parsePaceStr(paceStr):
        timeStr, eventStr = Pace.getTimeAndEventStr(paceStr)
        pace = Pace()
        pace.time = Time.parseTimeStr(timeStr)
        pace.event = Event.parseEventStr(eventStr, pace.time.unit)
        return pace
