from flask import Flask, render_template, request, jsonify
import api.api as api

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# http://127.0.0.1:5000//api/v1.0/parseSpeedStr?speedStr=10kph
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
    app.run(debug=True)
