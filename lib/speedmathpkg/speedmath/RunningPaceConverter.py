from speedmath.SpeedStrParser import Speed, Pace, Event, Time
from speedmath.Types import DistanceUnits, TimeUnits, KM_PER_MILE, MILE_PER_KM, HOURS_PER_SECOND, SECONDS_PER_HOUR


class RunningPaceConverter:
    def __init__(self, speed=None):
        self.speed = Speed() if speed is None else self.ToBaseSpeed(speed)

    @staticmethod
    def ToBaseSpeed(speed):
        speed.event = RunningPaceConverter.ToBaseEvent(speed.event)
        speed.time = RunningPaceConverter.ToBaseTime(speed.time)
        speed.Normalize()
        return speed

    @staticmethod
    def ToBaseEvent(event):
        # Base distance unit is kilometer
        # Only convert to kilometer
        distanceTable = {
            DistanceUnits.KM: lambda kms: kms,
            DistanceUnits.Mile: lambda miles: miles * KM_PER_MILE,
            DistanceUnits.Meter: lambda meters: meters / 1000
        }
        return Event(distanceTable[event.unit](event.distance), DistanceUnits.KM)

    def GetEventWithUnit(self, distanceUnit):
        # Only convert from kilometer
        distanceTable = {
            DistanceUnits.KM: lambda kms: kms,
            DistanceUnits.Mile: lambda kms: kms * MILE_PER_KM,
            DistanceUnits.Meter: lambda kms: kms * 1000
        }
        return Event(distanceTable[distanceUnit](self.speed.event.distance), distanceUnit)

    @staticmethod
    def ToBaseTime(time):
        # Base time unit is hour
        # Only convert to hour
        timeTable = {
            TimeUnits.Second: lambda seconds: seconds * HOURS_PER_SECOND,
            TimeUnits.Minute: lambda minutes: minutes / 60,
            TimeUnits.Hour: lambda hours: hours
        }
        return Time(timeTable[time.unit](time.time), TimeUnits.Hour)

    def GetTimeWithUnit(self, timeUnit):
        # Only convert from hour
        timeTable = {
            TimeUnits.Hour: lambda hours: hours,
            TimeUnits.Minute: lambda hours: hours * 60,
            TimeUnits.Second: lambda hours: hours * SECONDS_PER_HOUR
        }
        return Time(timeTable[timeUnit](self.speed.time.time), timeUnit)

    def GetSpeedInTargetUnits(self, targetDistanceUnit, targetTimeUnit):
        eventInTargetUnits = self.GetEventWithUnit(targetDistanceUnit)
        timeInTargetUnits = self.GetTimeWithUnit(targetTimeUnit)
        return Speed(eventInTargetUnits, timeInTargetUnits).Normalize()

    @staticmethod
    def GetEventTimeWithSpeed(speed, event, targetTimeUnit):
        rpc = RunningPaceConverter(speed)
        speedInTargetUnits = rpc.GetSpeedInTargetUnits(event.unit, targetTimeUnit)
        return Time(event.distance / speedInTargetUnits.event.distance, targetTimeUnit)

    @staticmethod
    def GetPaceFromSpeed(speed):
        if speed.time.unit != TimeUnits.Hour:
            raise Exception('Only time unit supported for speed->pace conversion is hours')
        pace = Pace()
        pace.time = Time(60 / speed.event.distance, TimeUnits.Minute)
        pace.event = Event(1, speed.event.unit)
        return pace

    @staticmethod
    def GetSpeedFromPace(pace):
        if pace.time.unit != TimeUnits.Minute:
            raise Exception('Only time unit supported for pace->speed conversion is minutes')
        speed = Speed()
        speed.event = Event(60 / pace.time.time, pace.event.unit)
        speed.time = Time(1, TimeUnits.Hour)
        return speed