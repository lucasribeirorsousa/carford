from datetime import datetime
from libs.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    secret = db.Column(db.String(512), nullable=True)

# class Customer(db.Model):
#     pass

# class Owner(db.Model):
#     '''
#     '''
#     pass