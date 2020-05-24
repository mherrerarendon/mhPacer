from source.speedmath.types import Speed, Pace, Event
from source.speedmath.converter import Converter
from source.speedmath.errCodes import smException
from source.speedmath.common import TimeUnits


def parseSpeedStr(speedStr):
    response = {}
    try:
        speed = Speed.parseSpeedStr(speedStr)
        pace = Converter.getPaceFromSpeed(speed)
        response['data'] = {}
        response['data']['speed'] = speed.serialize()
        response['data']['pace'] = pace.serialize()
        response['exitcode'] = 0
    except smException as e:
        response['exitcode'] = e.error_code.value
        response['data'] = repr(e)
    return response


def parsePaceStr(paceStr):
    response = {}
    try:
        pace = Pace.parsePaceStr(paceStr)
        speed = Converter.getSpeedFromPace(pace)
        response['data'] = {}
        response['data']['pace'] = pace.serialize()
        response['data']['speed'] = speed.serialize()
        response['exitcode'] = 0
    except smException as e:
        response['exitcode'] = e.error_code.value
        response['data'] = repr(e)
    return response


def parseTargetEventStr(targetEventStr):
    response = {}
    try:
        response['data'] = Event.parseEventStr(targetEventStr).serialize()
        response['exitcode'] = 0
    except smException as e:
        response['exitcode'] = e.error_code.value
        response['data'] = repr(e)
    return response


def getEventTimeWithSpeed(speedStr, eventStr):
    response = {}
    try:
        speed = Speed.parseSpeedStr(speedStr)
        targetEvent = Event.parseEventStr(eventStr)

        # Assume client wants response in minutes
        time = Converter.getEventTimeWithSpeed(speed, targetEvent, TimeUnits.Minute)
        response['data'] = time.serialize()
        response['exitcode'] = 0
    except smException as e:
        response['exitcode'] = e.error_code.value
        response['data'] = repr(e)
    return response
