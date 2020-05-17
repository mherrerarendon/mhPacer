from flask import Flask, render_template, request, jsonify
from speedmath.errCodes import smException
from speedmath.converter import Converter
from speedmath.types import Speed, Pace, Event
from speedmath.common import TimeUnits

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# http://127.0.0.1:5000//api/v1.0/parseSpeedStr?speedStr=10kph
@app.route('/api/v1.0/parseSpeedStr', methods=['GET'])
def parseSpeedStr():
    response = {}
    try:
        speedStr = request.args.get('speedStr')
        speed = Speed.parseSpeedStr(speedStr)
        pace = Converter.getPaceFromSpeed(speed)
        response['data'] = {}
        response['data']['speed'] = speed.serialize()
        response['data']['pace'] = pace.serialize()
        response['exitcode'] = 0
    except smException as e:
        response['exitcode'] = e.error_code.value
        response['data'] = repr(e)
    return jsonify(response)


@app.route('/api/v1.0/parsePaceStr', methods=['GET'])
def parsePaceStr():
    response = {}
    try:
        paceStr = request.args.get('paceStr')
        pace = Pace.parsePaceStr(paceStr)
        speed = Converter.getSpeedFromPace(pace)
        response['data'] = {}
        response['data']['pace'] = pace.serialize()
        response['data']['speed'] = speed.serialize()
        response['exitcode'] = 0
    except smException as e:
        response['exitcode'] = e.error_code.value
        response['data'] = repr(e)
    return jsonify(response)


@app.route('/api/v1.0/parseEventStr', methods=['GET'])
def parseTargetEventStr():
    response = {}
    try:
        targetEventStr = request.args.get('eventStr')
        response['data'] = Event.parseEventStr(targetEventStr).serialize()
        response['exitcode'] = 0
    except smException as e:
        response['exitcode'] = e.error_code.value
        response['data'] = repr(e)
    return jsonify(response)


@app.route('/api/v1.0/getEventTimeWithSpeed', methods=['GET'])
def getEventTimeWithSpeed():
    response = {}
    try:
        speed = Speed.parseSpeedStr(request.args.get('speedStr'))
        targetEvent = Event.parseEventStr(request.args.get('eventStr'))

        # Assume client wants response in minutes
        time = Converter.getEventTimeWithSpeed(speed, targetEvent, TimeUnits.Minute)
        response['data'] = time.serialize()
        response['exitcode'] = 0
    except smException as e:
        response['exitcode'] = e.error_code.value
        response['data'] = repr(e)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
