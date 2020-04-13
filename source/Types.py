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

TIME_KEY = 'time'
EVENT_KEY = 'event'
DISTANCE_KEY = 'distance'
UNIT_KEY = 'unit'
