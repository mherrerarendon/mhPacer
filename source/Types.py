from enum import Enum, unique, auto


@unique
class DistanceUnits(Enum):
    Mile = auto()
    KM = auto()
    Meter = auto()


@unique
class TimeUnits(Enum):
    Second = auto()
    Hour = auto()


KM_PER_MILE = 1.61
MILE_PER_KM = 1 / KM_PER_MILE

SECONDS_PER_HOUR = 3600
HOURS_PER_SECOND = 1 / SECONDS_PER_HOUR

DISTANCE_KEY = 'distance'
DISTANCE_UNIT_KEY = 'distanceUnit'
TIME_KEY = 'time'
TIME_UNIT_KEY = 'timeUnit'
