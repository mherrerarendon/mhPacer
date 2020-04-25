from flask import Flask, render_template, request, jsonify
import os
import sys

scriptDir = os.path.dirname(os.path.realpath(__file__))
sourceDir = os.path.abspath(os.path.join(scriptDir, 'source'))
sys.path.append(sourceDir)

from ErrorCodes import RPCException
from RunningPaceConverter import RunningPaceConverter
from SpeedStrParser import *
from Types import *

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
        response['data'] = Speed.ParseSpeedStr(speedStr).Serialize()
        response['exitcode'] = 0
    except RPCException as e:
        response['exitcode'] = e.error_code.value
        response['data'] = repr(e)
    return jsonify(response)


@app.route('/api/v1.0/parseEventStr', methods=['GET'])
def parseTargetEventStr():
    response = {}
    try:
        targetEventStr = request.args.get('eventStr')
        response['data'] = Event.ParseEventStr(targetEventStr).Serialize()
        response['exitcode'] = 0
    except RPCException as e:
        response['exitcode'] = e.error_code.value
        response['data'] = repr(e)
    return jsonify(response)


@app.route('/api/v1.0/getEventTimeWithSpeed', methods=['GET'])
def getEventTimeWithSpeed():
    response = {}
    try:
        speed = Speed.ParseSpeedStr(request.args.get('speedStr'))
        targetEvent = Event.ParseEventStr(request.args.get('eventStr'))

        # Assume client wants response in minutes
        time = RunningPaceConverter.GetEventTimeWithSpeed(speed, targetEvent, TimeUnits.Minute)
        response['data'] = time.Serialize()
        response['exitcode'] = 0
    except RPCException as e:
        response['exitcode'] = e.error_code.value
        response['data'] = repr(e)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
