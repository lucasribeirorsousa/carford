from flask import Flask
from libs.database import db
from flask_restful import Api
from flask_migrate import Migrate


app = Flask(__name__)

# config
app.secret_key = "<my_secret_key>"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///carford.db"

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)

# blueprints
from routes.bp_carford import blueprint_carford
app.register_blueprint(blueprint_carford)

# rest_apis
from  resources.controller_login import LoginAPI
from resources.controller_customer import CustomerAPI
from resources.controller_owner import OwnerAPI
api.add_resource(LoginAPI, "/", "/api/v1/login_api", endpoint="login_api")
api.add_resource(CustomerAPI, "/", "/api/v1/customer_api", endpoint="customer_api")
api.add_resource(OwnerAPI, "/", "/api/v1/owner_api", endpoint="owner_api")


