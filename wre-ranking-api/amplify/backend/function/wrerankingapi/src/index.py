from crypt import methods
import awsgi

from flask_cors import CORS
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)

# Constant variable with path prefix
BASE_ROUTE = "/seed"

def handler(event, context):
    return awsgi.response(app, event, context)

@app.route(BASE_ROUTE, methods=['GET'])
def seed():
    return jsonify(message="hello seed")

@app.route(BASE_ROUTE, methods=['POST'])
def perform_merge():
    request_json = request.get_json()

    men_first_startno=request_json.get("men_first_startno")
    women_first_startno=request_json.get("women_first_startno")

    print("Først startnummer menn: " + str(men_first_startno))
    print("Først startnummer damer: " + str(women_first_startno))

    return jsonify(message="merge performed")