from flask import render_template, request, jsonify
from source.site.rest_api_impl import *
from source.site import app
import source.site.rest_api_impl as rpcapi

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1.0/parseSpeedStr', methods=['POST'])
def parseSpeedStr():
    reqData = request.get_json()
    speedStr = reqData['speedStr']
    response = rpcapi.parseSpeedStr(speedStr)
    return jsonify(response), 201


@app.route('/api/v1.0/parsePaceStr', methods=['POST'])
def parsePaceStr():
    reqData = request.get_json()
    paceStr = reqData['paceStr']
    response = rpcapi.parsePaceStr(paceStr)
    return jsonify(response), 201


@app.route('/api/v1.0/parseEventStr', methods=['POST'])
def parseTargetEventStr():
    reqData = request.get_json()
    targetEventStr = reqData['eventStr']
    response = rpcapi.parseTargetEventStr(targetEventStr)
    return jsonify(response), 201


@app.route('/api/v1.0/getEventTimeWithSpeed', methods=['POST'])
def getEventTimeWithSpeed():
    reqData = request.get_json()
    speedStr = reqData['speedStr']
    eventStr = reqData['eventStr']
    response = rpcapi.getEventTimeWithSpeed(speedStr, eventStr)
    return jsonify(response), 201