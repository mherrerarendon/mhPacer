from flask import render_template, request, jsonify
from source.site.restApiImpl import *
from source.site import app
import source.site.restApiImpl as rpcapi

modelName = 'speedmath'
apiVersion = 'v1.0'

@app.route(f'/{modelName}/getEventTimeWithSpeed/{apiVersion}', methods=['POST'])
def getEventTimeWithSpeed():
    reqData = request.get_json()
    speedStr = reqData['speedStr']
    eventStr = reqData['eventStr']
    response = rpcapi.getEventTimeWithSpeed(speedStr, eventStr)
    return jsonify(response), 200