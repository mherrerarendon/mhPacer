from flask import Flask, render_template, request, jsonify
# from flask_restful import Resource, Api
from source import api as rpcapi
import argparse

app = Flask(__name__)
# restServer = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


# class Rpc(Resource):
#     def get(self):
#         speedStr = request.args.get('speedStr')
#         response = rpcapi.parseSpeedStr(speedStr)
#         return jsonify(response)


# restServer.add_resource(Rpc, '/api/v1.0/parseSpeedStr')

@app.route('/api/v1.0/parseSpeedStr', methods=['GET'])
def parseSpeedStr():
    speedStr = request.args.get('speedStr')
    response = rpcapi.parseSpeedStr(speedStr)
    return jsonify(response)


@app.route('/api/v1.0/parsePaceStr', methods=['GET'])
def parsePaceStr():
    paceStr = request.args.get('paceStr')
    response = rpcapi.parsePaceStr(paceStr)
    return jsonify(response)


@app.route('/api/v1.0/parseEventStr', methods=['GET'])
def parseTargetEventStr():
    targetEventStr = request.args.get('eventStr')
    response = rpcapi.parseTargetEventStr(targetEventStr)
    return jsonify(response)


@app.route('/api/v1.0/getEventTimeWithSpeed', methods=['GET'])
def getEventTimeWithSpeed():
    speedStr = request.args.get('speedStr')
    eventStr = request.args.get('eventStr')
    response = rpcapi.getEventTimeWithSpeed(speedStr, eventStr)
    return jsonify(response)


if __name__ == '__main__':
    cli = argparse.ArgumentParser(
        description='Runs server for RunningPaceConverter.',
        epilog='Copyright 2020, Marco Herrera-Rendon. All Rights Reserved.')
    cli.add_argument('-d', '--debug', action="store_true", help='Runs server in debug mode')
    args = cli.parse_args()

    app.run(debug=args.debug, port=80, host='0.0.0.0')
