from source.speedmath.types import Speed, Pace, Event
from source.speedmath.converter import Converter
from source.speedmath.errCodes import smException
from source.speedmath.common import TimeUnits


def parseSpeedStr(speedStr):
    response = {}
    try:
        speed = Speed.parseSpeedStr(speedStr)
        pace = Converter.getPaceFromSpeed(speed)
        response['speed'] = speed.asdict()
        response['pace'] = pace.asdict()
        response['completeRequest'] = True
    except smException as e:
        response['completeRequest'] = False
        response['reason'] = repr(e)
    return response


def parsePaceStr(paceStr):
    response = {}
    try:
        pace = Pace.parsePaceStr(paceStr)
        speed = Converter.getSpeedFromPace(pace)
        response['pace'] = pace.asdict()
        response['speed'] = speed.asdict()
        response['completeRequest'] = True
    except smException as e:
        response['completeRequest'] = False
        response['reason'] = repr(e)
    return response


def parseTargetEventStr(targetEventStr):
    response = {}
    try:
        response['event'] = Event.parseEventStr(targetEventStr).asdict()
        response['completeRequest'] = True
    except smException as e:
        response['completeRequest'] = False
        response['reason'] = repr(e)
    return response


def getEventTimeWithSpeed(speedStr, eventStr):
    response = {}
    speed = Speed.parseSpeedStr(speedStr)
    targetEvent = Event.parseEventStr(eventStr)

    # Assume client wants response in minutes
    time = Converter.getEventTimeWithSpeed(speed, targetEvent, TimeUnits.Minute)
    response['time'] = time.asdict()
    return response
