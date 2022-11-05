from flask_restful import Resource
from flask import request, make_response, abort, jsonify
from models.model_carford import User

class CustomersAPI(Resource):
    def __init__(self, *args):
        pass

    def get(self):
        try:
            return make_response(jsonify({"response": "Olaa Cliente!" + request.method }),200)
        except Exception as error:
            return make_response(jsonify({"response": str(error)}),503)

    def post(self):
        try:
            # body = request.data
            # args = request.args
            return make_response(jsonify({"response": "Olá Cliente!" + request.method }),200)
        except Exception as error:
            return make_response(jsonify({"response": str(error)}),503)

    def put(self):
        try:
            return make_response(jsonify({"response": "Olá Cliente!" + request.method }),200)
        except Exception as error:
            return make_response(jsonify({"response": str(error)}),503)

    def delete(self):
        try:
            return make_response(jsonify({"response": "Olá Cliente!" + request.method }),200)
        except Exception as error:
            return make_response(jsonify({"response": str(error)}),503)

