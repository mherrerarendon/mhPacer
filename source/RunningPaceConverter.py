from SpeedStrParser import *
from Types import *


class RunningPaceConverter:
    def __init__(self, speed=Speed()):
        self.speed = speed if speed == Speed() else self.ToBaseSpeed(speed)

    def ToBaseSpeed(self, speed):
        self.speed.event = self.ToBaseEvent(speed.event)
        self.speed.time = self.ToBaseTime(speed.time)
        self.speed.Normalize()

    @staticmethod
    def ToBaseEvent(event):
        # Base distance unit is kilometer
        # Only convert to kilometer
        distanceTable = {
            DistanceUnits.KM: lambda kms: kms,
            DistanceUnits.Mile: lambda miles: miles * KM_PER_MILE
        }
        return Event(distanceTable[event.unit](event.distance), DistanceUnits.KM)

    def GetEventWithUnit(self, distanceUnit):
        # Only convert from kilometer
        distanceTable = {
            DistanceUnits.KM: lambda kms: kms,
            DistanceUnits.Mile: lambda kms: kms * MILE_PER_KM
        }
        return Event(distanceTable[distanceUnit](self.event.distance), distanceUnit)

    @staticmethod
    def ToBaseTime(time):
        # Base time unit is hour
        # Only convert to hour
        timeTable = {
            TimeUnits.Second: lambda seconds: seconds * HOURS_PER_SECOND,
            TimeUnits.Hour: lambda hours: hours
        }
        return Time(timeTable[time.unit](time.time), Time.Hour)

    def GetTimeWithUnit(self, timeUnit):
        # Only convert from hour
        timeTable = {
            TimeUnits.Hour: lambda hours: hours,
            TimeUnits.Second: lambda hours: hours * SECONDS_PER_HOUR
        }
        return Time(timeTable[timeUnit](self.time.time), timeUnit)

    def GetSpeedInTargetUnits(self, targetDistanceUnit, targetTimeUnit):
        eventInTargetUnits = self.GetEventWithUnit(targetDistanceUnit)
        timeInTargetUnits = self.GetTimeWithUnit(targetTimeUnit)
        return Speed(eventInTargetUnits, timeInTargetUnits).Normalize()

    @staticmethod
    def GetEventTimeWithSpeed(speed, event, targetTimeUnit):
        rpc = RunningPaceConverter(speed)
        speedInTargetUnits = rpc.GetSpeedInTargetUnits(event.unit, targetTimeUnit)
        return event.distance / speedInTargetUnits.event.distance
