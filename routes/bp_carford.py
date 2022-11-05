from flask import Blueprint, make_response, render_template

blueprint_carford = Blueprint(
    "bp_carford",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/routes/static")

@blueprint_carford.route("/", methods=["GET"])
def index() -> make_response:
    return make_response(render_template("index.html"), 200)

@blueprint_carford.route("/login", methods=["POST", "GET"])
def login() -> make_response:
    return make_response(render_template("login.html"), 200)

