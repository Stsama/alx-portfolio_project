from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Restaurant(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    telephone = db.Column(db.String(150))
    city = db.Column(db.String(150))
    area = db.Column(db.String(150))
    password = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Float())
    description = db.Column(db.Sting(200))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    telephone = db.Column(db.String(150))
    city = db.Column(db.String(150))
    area = db.Column(db.String(150))
    password = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)