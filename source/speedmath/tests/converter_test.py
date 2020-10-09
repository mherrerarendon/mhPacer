from source.speedmath.types import Speed, Event, Time, Pace
from source.speedmath.converter import Converter
from source.speedmath.common import DistanceUnits, TimeUnits

def assertEventConversion(event, expectedEvent):
    converter = Converter()
    converter.speed.event = Converter.toBaseEvent(event)
    actualEvent = converter.getEventWithUnit(expectedEvent.unit)
    actualEvent.distance = round(actualEvent.distance, 2)
    assert actualEvent == expectedEvent

# Legacy
def assertTimeConversion(time, expectedTime):
    converter = Converter()
    converter.speed.time = Converter.toBaseTime(time)
    actualTime = converter.getTimeWithUnit(expectedTime.unit)
    actualTime.time = round(actualTime.time, 2)
    assert actualTime == expectedTime

# Legacy
def test_getEventWithUnit():
    assertEventConversion(Event(2, DistanceUnits.Mile), Event(3.22, DistanceUnits.KM))
    assertEventConversion(Event(2, DistanceUnits.KM), Event(1.24, DistanceUnits.Mile))

# Legacy
def test_getTimeWithUnit():
    assertTimeConversion(Time(2, TimeUnits.Hour), Time(7200, TimeUnits.Second))
    assertTimeConversion(Time(1000, TimeUnits.Second), Time(0.28, TimeUnits.Hour))
    assertTimeConversion(Time(7200, TimeUnits.Second), Time(2, TimeUnits.Hour))

def assertSpeedConversion(speed, expectedSpeed):
    converter = Converter(speed)
    actualSpeed = converter.getSpeedInTargetUnits(expectedSpeed.event.unit, expectedSpeed.time.unit)
    actualSpeed.event.distance = round(actualSpeed.event.distance, 2)
    actualSpeed.time.time = round(actualSpeed.time.time, 2)
    assert actualSpeed == expectedSpeed

def test_getSpeedInTargetUnits():
    speed = Speed(Event(12, DistanceUnits.KM), Time(1, TimeUnits.Hour))
    expectedSpeed = Speed(Event(3.33, DistanceUnits.Meter), Time(1, TimeUnits.Second))
    assertSpeedConversion(speed, expectedSpeed)

    speed = Speed(Event(3.33, DistanceUnits.Meter), Time(1, TimeUnits.Second))
    expectedSpeed = Speed(Event(11.99, DistanceUnits.KM), Time(1, TimeUnits.Hour))
    assertSpeedConversion(speed, expectedSpeed)

    speed = Speed(Event(10, DistanceUnits.Mile), Time(1, TimeUnits.Hour))
    expectedSpeed = Speed(Event(16.10, DistanceUnits.KM), Time(1, TimeUnits.Hour))
    assertSpeedConversion(speed, expectedSpeed)

    speed = Speed(Event(10, DistanceUnits.KM), Time(1, TimeUnits.Hour))
    expectedSpeed = Speed(Event(6.21, DistanceUnits.Mile), Time(1, TimeUnits.Hour))
    assertSpeedConversion(speed, expectedSpeed)

def test_getEventTimeWithSpeed():
    speed = Speed(Event(1, DistanceUnits.KM), Time(1, TimeUnits.Hour))
    event = Event(1, DistanceUnits.Mile)
    actualTime = Converter.getEventTimeWithSpeed(speed, event, TimeUnits.Hour)
    assert round(actualTime.time, 2) == 1.61

def assertSpeedToPaceConversion(speed, expectedPace):
    actualPace = Converter.getPaceFromSpeed(speed)
    actualPace.time.time = round(actualPace.time.time, 2)
    assert actualPace == expectedPace

def test_getPaceFromSpeed():
    speed = Speed(Event(6, DistanceUnits.Mile), Time(1, TimeUnits.Hour))
    expectedPace = Pace(Time(10, TimeUnits.Minute), Event(1, DistanceUnits.Mile))
    assertSpeedToPaceConversion(speed, expectedPace)

    speed = Speed(Event(7, DistanceUnits.Mile), Time(1, TimeUnits.Hour))
    expectedPace = Pace(Time(8.57, TimeUnits.Minute), Event(1, DistanceUnits.Mile))
    assertSpeedToPaceConversion(speed, expectedPace)

    speed = Speed(Event(8, DistanceUnits.KM), Time(1, TimeUnits.Hour))
    expectedPace = Pace(Time(7.5, TimeUnits.Minute), Event(1, DistanceUnits.KM))
    assertSpeedToPaceConversion(speed, expectedPace)

def assertPaceToSpeedConversion(pace, expectedSpeed):
    actualSpeed = Converter.getSpeedFromPace(pace)
    actualSpeed.event.distance = round(actualSpeed.event.distance, 2)
    assert actualSpeed == expectedSpeed

def test_getSpeedFromPace():
    pace = Pace(Time(10, TimeUnits.Minute), Event(1, DistanceUnits.Mile))
    expectedSpeed = Speed(Event(6, DistanceUnits.Mile), Time(1, TimeUnits.Hour))
    assertPaceToSpeedConversion(pace, expectedSpeed)

    pace = Pace(Time(8.57, TimeUnits.Minute), Event(1, DistanceUnits.Mile))
    expectedSpeed = Speed(Event(7, DistanceUnits.Mile), Time(1, TimeUnits.Hour))
    assertPaceToSpeedConversion(pace, expectedSpeed)

    pace = Pace(Time(7.5, TimeUnits.Minute), Event(1, DistanceUnits.KM))
    expectedSpeed = Speed(Event(8, DistanceUnits.KM), Time(1, TimeUnits.Hour))
    assertPaceToSpeedConversion(pace, expectedSpeed)
