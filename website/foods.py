from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import User, Food, Order
from . import db
import validators  # type: ignore
from constants.http_status_codes import *
from flask_login import login_user, login_required, logout_user, current_user

foods = Blueprint('foods', __name__)

@foods.get('/')
def get_all_foods():
    foods = Food.query.all()
    foods_data = []
    for food in foods:
        new={
            'id': food.id,
            'name':food.name,
            'price':food.price,
            'description':food.description,
            'user_id': food.user_id
        }
        foods_data.append(new)
    return jsonify({
        'foods': foods_data
    }), HTTP_200_OK
    
    
@foods.get('/<int:id>')
def get_food(id):
    food = Food.query.filter_by(id=id).first()
    if not food:
        return jsonify({
        'message': 'food not found'
    }), HTTP_404_NOT_FOUND

    return jsonify({
        'id': food.id,
        'name':food.name,
        'price':food.price,
        'description':food.description,
        'user_id': food.user_id
    }), HTTP_200_OK



@foods.get('/<int:id>')
def delete_food(id):
    food = Food.query.filter_by(id=id).first()
    if not food:
        return jsonify({
        'message': 'food not found'
    }), HTTP_404_NOT_FOUND
    db.session.delete(food)
    db.session.commit()
    return jsonify({
        'message': "deleted correctly"
    }), HTTP_200_OK


    
@foods.post('/create')
@login_required
def create_food():
    if current_user.profile == "seller":
        name = request.json['name']
        price = request.json['price']
        description = request.json['description']
        user_id = current_user.id
        
        if len(name) < 2:
            return jsonify({'error': 'name is too short'}), HTTP_400_BAD_REQUEST
        if price == 0:
            return jsonify({'error': 'price invalid'}), HTTP_400_BAD_REQUEST
        if len(description) < 20:
            return jsonify({'error': 'description must contain at least 20 characters'}), HTTP_400_BAD_REQUEST
        
        food = Food(name=name, price=price, description=description, user_id=user_id)
        db.session.add(food)
        db.session.commit()
        
        return jsonify({
            'message': 'food created successfully',
            'food': {
                'name':food.name,
                'price': food.price,
                'description': food.description,
            }
        })
    
    else:
        return jsonify({'error': 'You are not allowed to check this page'}), HTTP_401_UNAUTHORIZED