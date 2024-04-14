from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import User, Food, Order
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import validators  # type: ignore
from constants.http_status_codes import *
from flask_login import login_user, login_required, logout_user, current_user

orders = Blueprint('orders', __name__)


# get all the orders with the need for admin authentication
@orders.get('/')
@login_required
def get_orders():
    if current_user.is_admin:
        orders = Order.query.all()
        orders_data = []
        for order in orders:
            new={
                'id': order.id,
                'user': order.user.username,
                'food': order.foods.name,
                'number_order': order.number
            }
            orders_data.append(new)
        return jsonify({
            'orders': orders_data
        }), HTTP_200_OK
    else:
            return jsonify({'error': 'You are not allowed to check this page'}), HTTP_401_UNAUTHORIZED
    

# get a single order with the need of admin authentication    
@orders.get('/<int:id>')
@login_required
def get_order(id):
    if current_user.is_admin:
        order = Order.query.filter_by(id=id).first()
        if not order:
            return jsonify({
            'message': 'order not found'
        }), HTTP_404_NOT_FOUND
    
        return jsonify({
            'id': order.id,
            'user_id': order.user_id,
            'email': order.user.email,
            'created_at':  order.created_at,
            'updated_at':  order.updated_at,
        }), HTTP_200_OK
    else:
        return jsonify({'error': 'You are not allowed to check this page'}), HTTP_401_UNAUTHORIZED
        

# post a single order with the need of user authentication 
@orders.post('/<int:id>')
@login_required
def order_food(id):
    user_id = current_user.id
    food_id = id
    number_order = request.json.get('number', "")
    if not isinstance(number_order, int):
        return jsonify({
            'error': 'Number of the order must be an integer'
        }), HTTP_400_BAD_REQUEST
    new_order = Order(user_id=user_id, food_id=food_id, number=number_order)
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({
        'message': 'Your order has been recieved',
        'user': new_order.user.username,
        'food': new_order.foods.name,
        "number": new_order.number
    }), HTTP_200_OK
    