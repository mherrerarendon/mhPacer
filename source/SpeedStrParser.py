from ErrorCodes import RPCException, ErrorCodes
import re
from Types import *


class SpeedStrParser:
    @staticmethod
    def Parse(speedStr):
        match = re.search(r'(\d+)(\S)p(\S)', speedStr)
        if match is None:
            raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse speed string')
        speed = {
            DISTANCE_KEY: SpeedStrParser.ParseValue(match.group(1)),
            DISTANCE_UNIT_KEY: SpeedStrParser.ParseDistanceUnit(match.group(2)),
            TIME_KEY: 1,  # Assume 1 hour in 12kph, for example
            TIME_UNIT_KEY: SpeedStrParser.ParseTimeUnit(match.group(3))
        }
        return speed

    @staticmethod
    def SerializeSpeed(speed):
        serializeDistanceUnit = {DistanceUnits.Mile: 'mile', DistanceUnits.KM: 'kilometer'}
        serializeTimeUnit = {TimeUnits.Hour: 'hour', TimeUnits.Second: 'second'}
        return {
            DISTANCE_KEY: speed[DISTANCE_KEY],
            DISTANCE_UNIT_KEY: serializeDistanceUnit[speed[DISTANCE_UNIT_KEY]],
            TIME_KEY: speed[TIME_KEY],
            TIME_UNIT_KEY: serializeTimeUnit[speed[TIME_UNIT_KEY]]
        }

    @staticmethod
    def ParseValue(valueStr):
        value = None
        if valueStr is None:
            raise RPCException(ErrorCodes.PARSE_ERR, 'Could not parse value')
        try:
            value = int(valueStr)
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

    @staticmethod
    def ParseTimeUnit(timeUnitStr):
        if timeUnitStr is None:
            raise RPCException(ErrorCodes.TIME_UNIT_PARSE_ERR, 'Could not parse time unit')
        timeStrToEnum = {'h': TimeUnits.Hour, 's': TimeUnits.Second}
        if timeUnitStr.lower() not in timeStrToEnum:
            raise RPCException(ErrorCodes.TIME_UNIT_PARSE_ERR, 'Could not parse time unit')
        return timeStrToEnum[timeUnitStr.lower()]
