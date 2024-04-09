from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Float())
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ordered = db.relationship('Food', secondary='user_food', backref='food' )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    telephone = db.Column(db.String(150))
    city = db.Column(db.String(150))
    area = db.Column(db.String(150))
    profile = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    foods = db.relationship('Food')
    orders = db.relationship('Food', secondary='user_food', backref='user' )

  
user_food = db.Table('user_food',
                    db.Column('id', db.Integer, primary_key=True),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('food_id', db.Integer, db.ForeignKey('food.id')),
                    db.Column('number_order', db.Integer, nullable=False)
                    )