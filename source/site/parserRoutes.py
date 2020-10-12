from flask import request, jsonify
from source.site.restApiImpl import *
from source.site import app
import source.site.restApiImpl as rpcapi

modelName = 'parser'
apiVersion = 'v1.0'

@app.route(f'/{modelName}/parseSpeedStr/{apiVersion}', methods=['POST'])
def parseSpeedStr():
    reqData = request.get_json()
    speedStr = reqData['speedStr']
    response = rpcapi.parseSpeedStr(speedStr)
    return jsonify(response), 200

@app.route(f'/{modelName}/parsePaceStr/{apiVersion}', methods=['POST'])
def parsePaceStr():
    reqData = request.get_json()
    paceStr = reqData['paceStr']
    response = rpcapi.parsePaceStr(paceStr)
    return jsonify(response), 200

@app.route(f'/{modelName}/parseEventStr/{apiVersion}', methods=['POST'])
def parseTargetEventStr():
    reqData = request.get_json()
    targetEventStr = reqData['eventStr']
    response = rpcapi.parseTargetEventStr(targetEventStr)
    return jsonify(response), 200