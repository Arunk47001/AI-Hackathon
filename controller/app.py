# importing the libraries
from flask import Flask, jsonify, request, Response, make_response
from flask_cors import CORS
import logging
import json

from usecase.usecase_FarmerAgent import farmerImageTextChat, farmerAudioChat
from usecase.usercase_cropLossAgent import cropLossAgent, cropLossMarketPriceComp, cropLossSubsidy

app = Flask(__name__)
cors = CORS(app)


# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route('/farm/agent/chat', methods =['POST'])
def agentFM():
    try:
        messages = {}
        messages['user_name'] = request.form["user_name"]
        messages['session_id'] = request.form["session_id"]
        messages['question'] = request.form["question"]
        if "image" in request.files:
            file = request.files["image"]
            messages["images"] = file.read()
        data = farmerImageTextChat(messages)
        return Response(data,mimetype='text/plain'), 201
    except ValueError as err:
        print(err)
        return Response("Internal server error", mimetype="text/plain"), 500
    except KeyError as err:
        print(err)
        return jsonify({'error': 'Missing Parameter'}), 400

@app.route('/farm/agent/audio', methods =['POST'])
def agentAD():
    try:
        messages ={}
        messages['user_name'] = request.form["user_name"]
        messages['session_id'] = request.form["session_id"]
        if "audio" in request.files:
            file = request.files['audio']
            messages["audio"] = file.read()
        data = farmerAudioChat(messages)
        response = make_response(data)
        response.headers.set('Content-Type', 'audio/wav')
        response.headers.set('Content-Disposition', 'inline', filename='audiov1.wav')
        return response, 201
    except ValueError as err:
        print(err)
        return Response("Internal server error", mimetype="text/plain"), 500
    except KeyError as err:
        print(err)
        return jsonify({'error': 'Missing Parameter'}), 400


@app.route('/farm/agent/cropLoss', methods =['GET'])
def agentCP():
    try:
        data = cropLossAgent()
        return Response(data,mimetype='text/plain'), 200
    except ValueError as err:
        print(err)
        return Response("Internal server error", mimetype="text/plain"), 500
    except KeyError as err:
        print(err)
        return jsonify({'error': 'Missing Parameter'}), 400


@app.route('/farm/agent/marketComp', methods =['GET'])
def agentCMP():
    try:
        data = cropLossMarketPriceComp()
        return jsonify(data), 200
    except ValueError as err:
        print(err)
        return Response("Internal server error", mimetype="text/plain"), 500
    except KeyError as err:
        print(err)
        return jsonify({'error': 'Missing Parameter'}), 400


@app.route('/farm/agent/cropSubsidy', methods =['GET'])
def agentsub():
    try:
        data = cropLossSubsidy()
        return Response(data,mimetype='text/plain'), 200
    except ValueError as err:
        print(err)
        return Response("Internal server error", mimetype="text/plain"), 500
    except KeyError as err:
        print(err)
        return jsonify({'error': 'Missing Parameter'}), 400