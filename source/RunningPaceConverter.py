from SpeedStrParser import SpeedStrParser
from Types import *


class RunningPaceConverter:
    def __init__(self):
        pass

    distanceTable = {
        DistanceUnits.KM: {  # km to miles
            DistanceUnits.Mile: lambda kms: kms * MILE_PER_KM
        },
        DistanceUnits.Mile: {  # miles to km
            DistanceUnits.KM: lambda miles: miles * KM_PER_MILE
        }
    }

    timeTable = {
        TimeUnits.Second: {  # seconds to hours
            TimeUnits.Hour: lambda seconds: seconds * HOURS_PER_SECOND
        },
        TimeUnits.Hour: {  # hours to seconds
            TimeUnits.Second: lambda hours: hours * SECONDS_PER_HOUR
        }
    }

    @staticmethod
    def ConvertDistanceToDistance(distance, units, targetUnits):
        if units != targetUnits:
            return RunningPaceConverter.distanceTable[units][targetUnits](distance)
        else:
            return distance

    @staticmethod
    def ConvertTimeToTime(time, units, targetUnits):
        if units != targetUnits:
            return RunningPaceConverter.timeTable[units][targetUnits](time)
        else:
            return time

    @staticmethod
    def GetSpeedInTargetUnits(speed, targetDistanceUnit, targetTimeUnit):
        speedInTargetUnits = {
            DISTANCE_KEY: RunningPaceConverter.ConvertDistanceToDistance(speed[DISTANCE_KEY], speed[DISTANCE_UNIT_KEY], targetDistanceUnit),
            DISTANCE_UNIT_KEY: targetDistanceUnit,
            TIME_KEY: RunningPaceConverter.ConvertTimeToTime(speed[TIME_KEY], speed[TIME_UNIT_KEY], targetTimeUnit),
            TIME_UNIT_KEY: targetTimeUnit
        }
        return speedInTargetUnits

    @staticmethod
    def GetEventTimeFromSpeed(speedStr, targetEvent, targetTimeUnit):
        speed = SpeedStrParser.Parse(speedStr)
        speedInTargetUnits = RunningPaceConverter.GetSpeedInTargetUnits(speed, targetEvent[DISTANCE_UNIT_KEY], targetTimeUnit)
        return targetEvent[DISTANCE_KEY] / speedInTargetUnits[DISTANCE_KEY] * speedInTargetUnits[TIME_KEY]
