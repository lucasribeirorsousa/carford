import json, jwt
from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request, make_response, abort, jsonify, current_app
from hashlib import pbkdf2_hmac
from models.model_carford import User

class LoginAPI(Resource):
    def __init__(self, *args):
        pass

    def get(self):
        try:
            raise Exception("This method is invalid or not implemented!")
        except Exception as error:
            return make_response(jsonify({"response": str(error)}),503)

    def post(self):
        try:
            body = request.data
            if not body:
                return make_response(
                    jsonify({
                        "response": "Your request method invalid why not content data in body!",
                        "status": 403}), 403)

            body = json.loads(body)
            email = body.get("email")
            secret = body.get("secret")

            if not email or not secret:
                return make_response(
                    jsonify({
                        "response": "Params: [email, secret] is required in your request method!",
                        "status": 403}), 403)

            user = User.query.filter_by(email=email).first()
            if not user:
                return make_response(
                    jsonify({
                        "response": "User not found!",
                        "status": 404}), 404)

            pwhash = pbkdf2_hmac(
                "sha256",
                str.encode(secret.join(current_app.secret_key)),
                b"bad salt" * 2,
                500_000).hex()

            if email == user.email and pwhash == user.secret:
                playload = {
                    "user": json.dumps(
                        {
                            "id": user.id,
                            "email": user.email,
                            "name": user.fullname,
                        }
                    ),
                    "exp": datetime.utcnow() + timedelta(minutes=60),
                }
                token = jwt.encode(playload, current_app.secret_key, algorithm="HS256")
                resp = make_response(
                    jsonify({
                        "response": token.encode().decode("UTF-8"),
                        "status": 200}), 200)
                resp.set_cookie("x-access-token", token.encode().decode("UTF-8"))
                return resp
            else:
                return make_response(
                    jsonify({
                        "response": "User or Password is invalid!",
                        "status": 404}), 404)
        except Exception as error:
            return make_response(jsonify({"response": str(error)}),503)

    def put(self):
        try:
            raise Exception("This method is invalid or not implemented!")
        except Exception as error:
            return make_response(jsonify({"response": str(error)}),503)

    def delete(self):
        try:
            raise Exception("This method is invalid or not implemented!")
        except Exception as error:
            return make_response(jsonify({"response": str(error)}),503) 