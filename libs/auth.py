import jwt, json
import traceback
from flask import request, redirect, current_app, make_response, jsonify
from functools import wraps

def login_is_required(f):
    """ AUTH using JWT """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        try:
            # token jwt in header
            if request.cookies.get("x-access-token"):
                token = request.cookies.get("x-access-token")

            if not request.cookies.get("x-access-token"):
                token = request.headers.get("Authorization")

        except Exception:
            traceback.print_exc()
            return redirect("/login")

        # return 401 if not token
        if not token:
            if "/api/" in request.url:
                return make_response(jsonify({
                    "response": "401 Unauthorized/Token Expired. Please reflesh your agent.",
                    "status": 401}), 401)
            else:
                return redirect("/login")

        try:
            # parse of token
            data = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])

        except Exception:
            traceback.print_exc()
            if "/api/" in request.url:
                return make_response(jsonify({
                    "response": "401 Unauthorized/Token Expired. Please reflesh your agent.",
                    "status": 401}), 401)
            else:
                return redirect("/login")

        return f(*args, **kwargs)
    return decorated

def decode_playload_in_token() -> dict:
    """ Decode Playload in Token """
    try:
        playload = jwt.decode(
            request.cookies.get("x-access-token") if request.cookies.get("x-access-token") else request.headers.get("Authorization"),
            current_app.secret_key,
            algorithms=["HS256"])
        return json.loads(playload.get("user"))

    except Exception:
        return jsonify({"playload": None})