import uuid
from datetime import datetime
from libs.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    fullname = db.Column(db.String(64), nullable=False)
    secret = db.Column(db.String(512), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    fullname = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    owner = db.Column(db.Boolean, default=False, nullable=False)
    create_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

class Owner(db.Model):
    __tablename__ = "owners"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    vehicle_id = db.Column(db.String(36), nullable=False, default=str(uuid.uuid1()))
    vehicle_color = db.Column(db.String(10), nullable=False)
    vehicle_model = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    create_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)