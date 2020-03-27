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
            'distance': ConvertDistanceToDistance(speed['distance'], speed['distanceUnit'], targetDistanceUnit),
            'distanceUnit': targetDistanceUnit,
            'time': ConvertTimeToTime(speed['time'], speed['timeUnit'], targetTimeUnit),
            'timeUnit': targetTimeUnit
        }
        return speedInTargetUnits

    @staticmethod
    def GetEventTimeFromSpeed(speedStr, targetEvent, targetTimeUnit):
        speed = SpeedStrParser.Parse(speedStr)
        speedInTargetUnits = GetSpeedInTargetUnits(speed, targetEvent['distanceUnit'], targetTimeUnit)
        return targetEvent['distance'] / speedInTargetUnits['distance'] * speedInTargetUnits['time']
