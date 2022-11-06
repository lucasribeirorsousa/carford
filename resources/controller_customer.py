import json
from libs.database import db
from libs.auth import login_is_required, decode_playload_in_token
from flask_restful import Resource
from flask import request, make_response, abort, jsonify
from models.model_carford import User, Customer, Owner

class CustomerAPI(Resource):
    def __init__(self, *args):
        self.current_user = decode_playload_in_token()
    
    @login_is_required
    def get(self):
        try:
            customer_id = request.args.get("customer_id")
            customers_all = []

            if customer_id:
                customer = Customer.query.filter_by(id=int(customer_id)).first()
                
                if not customer:
                    return make_response(
                        jsonify({
                            "response": "Customer not found with this id!",
                            "status": 404}), 404)
                
                return make_response(
                    jsonify({
                        "response":{
                            "id": customer.id,
                            "fullname": customer.fullname,
                            "phone_number": customer.phone_number,
                            "cpf": customer.cpf,
                            "owner": customer.owner}}),200)
            else:
                customers = Customer.query.all()

                for customer in customers:
                    customers_all.append({
                            "id": customer.id,
                            "fullname": customer.fullname,
                            "phone_number": customer.phone_number,
                            "cpf": customer.cpf,
                            "owner": customer.owner})

                return make_response(jsonify({"response":customers_all}),200)

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
            email = body.get("email")
            fullname = body.get("fullname")
            phone_number = body.get("phone_number")
            cpf = body.get("cpf")

            if not email or not fullname or not phone_number or not cpf:
                return make_response(
                    jsonify({
                        "response": "Params: [email, fullname, phone_number, cpf] is required in your request method!",
                        "status": 403}), 403)
            
            customer = Customer.query.filter_by(cpf=cpf).first()

            if customer:
                return make_response(
                    jsonify({
                        "response": "Customer already exist with this cpf",
                        "status": 403}), 403)
            try:
                new_customer = Customer(
                    email=email, 
                    fullname=fullname, 
                    phone_number=phone_number,
                    cpf=cpf,
                    create_by=self.current_user.get("id"))

                db.session.add(new_customer)
                db.session.commit()   

                return make_response(jsonify({"response": "Customer created with successfully"},201))

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

