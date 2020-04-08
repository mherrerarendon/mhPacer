from flask import Flask, render_template, request, jsonify
import os
import sys

scriptDir = os.path.dirname(os.path.realpath(__file__))
sourceDir = os.path.abspath(os.path.join(scriptDir, 'source'))
sys.path.append(sourceDir)

from ErrorCodes import RPCException
from SpeedStrParser import SpeedStrParser

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# http://127.0.0.1:5000//api/v1.0/parseSpeedStr?speedStr=10kph
@app.route('/api/v1.0/parseSpeedStr', methods=['GET'])
def parseSpeedStr():
    import pdb; pdb.set_trace()  # breakpoint 69090786 //
    response = {}
    try:
        speedStr = request.args.get('speedStr')
        response['data'] = SpeedStrParser.SerializeSpeed(SpeedStrParser.Parse(speedStr))
        response['exitcode'] = 0
    except RPCException as e:
        response['exitcode'] = e.error_code.value
        response['data'] = repr(e)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
