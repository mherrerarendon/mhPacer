from flask import render_template, request, jsonify
from source.site.rest_api_impl import *
from source.site import app
import source.site.rest_api_impl as rpcapi

@app.route('/')
def index():
    return render_template('index.html')

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