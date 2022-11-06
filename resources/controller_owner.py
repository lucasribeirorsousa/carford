import json
from libs.database import db
from libs.auth import login_is_required, decode_playload_in_token
from flask_restful import Resource
from flask import request, make_response, abort, jsonify
from models.model_carford import User, Customer, Owner

class OwnerAPI(Resource):
    def __init__(self, *args):
        self.current_user = decode_playload_in_token()
    
    @login_is_required
    def get(self):
        try:
            customer_id = request.args.get("customer_id")
            owners_all = []

            if customer_id:
                owners = Owner.query.filter_by(customer_id=int(customer_id)).all()
                
                if not owners:
                    return make_response(
                        jsonify({
                            "response": "This customer don't has vehicles!",
                            "status": 404}), 404)
                

                for owner in owners:
                    owners_all.append({
                            "id": owner.id,
                            "customer_id": owner.customer_id,
                            "vehicle_id": owner.vehicle_id,
                            "vehicle_color": owner.vehicle_color,
                            "vehicle_model": owner.vehicle_model,
                            "active": owner.active})

                return make_response(jsonify({"response":owners_all}),200)

            else:
                owners = Owner.query.all()

                for owner in owners:
                    owners_all.append({
                            "id": owner.id,
                            "customer_id": owner.customer_id,
                            "vehicle_id": owner.vehicle_id,
                            "vehicle_color": owner.vehicle_color,
                            "vehicle_model": owner.vehicle_model,
                            "active": owner.active})

                return make_response(jsonify({"response":owners_all}),200)

        except Exception as error:
            return make_response(jsonify({"response": str(error)}),503)
    
    @login_is_required
    def post(self):
        try:
            body = request.data
            if not body:
                return make_response(
                    jsonify({
                        "response": "Your request method invalid why not content data in body!",
                        "status": 403}), 403)

            body = json.loads(body)
            customer_id = body.get("customer_id")
            vehicle_color = body.get("vehicle_color")
            vehicle_model = body.get("vehicle_model")

            if not customer_id or not vehicle_color or not vehicle_model:
                return make_response(
                    jsonify({
                        "response": "Params: [customer_id, vehicle_color, vehicle_model] is required in your request method!",
                        "status": 403}), 403)
            
            customer = Customer.query.filter_by(id=int(customer_id)).first()

            if not customer:
                return make_response(
                    jsonify({
                        "response": "Customer not found with this id",
                        "status": 404}), 404)
            
            owners = Owner.query.filter_by(customer_id=int(customer_id)).all()

            if len(owners) >= 3:
                return make_response(
                    jsonify({
                        "response": "This Customer already has 3 vehicles!",
                        "status": 404}), 404)
            
            if vehicle_color.lower() not in ['amarelo','azul','cinza']:
                return make_response(
                    jsonify({
                        "response": "This vehicle color is invalid! Allowed colors: ['amerelo','azul','cinza']",
                        "status": 404}), 404)
            
            if vehicle_model.lower() not in ['hatch','sedan','conversível']:
                return make_response(
                    jsonify({
                        "response": "This vehicle model is invalid! Allowed models: ['hatch','sedan','conversível']",
                        "status": 404}), 404)

            try:
                new_owner = Owner(
                    customer_id=int(customer_id), 
                    vehicle_color=vehicle_color, 
                    vehicle_model=vehicle_model,
                    create_by=self.current_user.get("id"))

                db.session.add(new_owner)
                customer.owner = True
                db.session.commit()

                return make_response(jsonify({"response": "Owner created with successfully"},201))

            except Exception as error:
                db.session.rollback()
                return make_response(jsonify({"response": str(error)}),503)

        except Exception as error:
            return make_response(jsonify({"response": str(error)}),503)

    @login_is_required
    def put(self):
        try:
            raise Exception("This method is invalid or not implemented!")
        except Exception as error:
            return make_response(jsonify({"response": str(error)}),503)

    @login_is_required
    def delete(self):
        try:
            raise Exception("This method is invalid or not implemented!")
        except Exception as error:
            return make_response(jsonify({"response": str(error)}),503)
