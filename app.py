from flask import Flask, render_template, request, jsonify
from source import api
import argparse

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1.0/parseSpeedStr', methods=['GET'])
def parseSpeedStr():
    speedStr = request.args.get('speedStr')
    response = api.parseSpeedStr(speedStr)
    return jsonify(response)


@app.route('/api/v1.0/parsePaceStr', methods=['GET'])
def parsePaceStr():
    paceStr = request.args.get('paceStr')
    response = api.parsePaceStr(paceStr)
    return jsonify(response)


@app.route('/api/v1.0/parseEventStr', methods=['GET'])
def parseTargetEventStr():
    targetEventStr = request.args.get('eventStr')
    response = api.parseTargetEventStr(targetEventStr)
    return jsonify(response)


@app.route('/api/v1.0/getEventTimeWithSpeed', methods=['GET'])
def getEventTimeWithSpeed():
    speedStr = request.args.get('speedStr')
    eventStr = request.args.get('eventStr')
    response = api.getEventTimeWithSpeed(speedStr, eventStr)
    return jsonify(response)


if __name__ == '__main__':
    cli = argparse.ArgumentParser(
        description='Runs server for RunningPaceConverter.',
        epilog='Copyright 2020, Marco Herrera-Rendon. All Rights Reserved.')
    cli.add_argument('-d', '--debug', action="store_true", help='Runs server in debug mode')
    args = cli.parse_args()

    app.run(debug=args.debug, port=80)
