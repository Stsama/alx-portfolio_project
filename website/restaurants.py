from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import User, Food, Order
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import validators  # type: ignore
from constants.http_status_codes import *
from flask_login import login_user, login_required, logout_user, current_user

restaurants = Blueprint('restaurants', __name__)
# get all the restaurants with no need for authentication
@restaurants.get('/')
def get_all_restaurants():
    users = User.query.filter_by(profile="seller").all()
    users_data = []
    for user in users:
        new={
            "id": user.id,
            'username':user.username,
            'email':user.email,
            'profile':user.profile
        }
        users_data.append(new)
    return jsonify({
        'restaurants': users_data
    }), HTTP_200_OK
 
# get a single restaurant providing an Id with no need for authentication 
@restaurants.get('/<int:id>')
def get_a_restaurants(id):
    
    restaurant = User.query.filter_by(id=id, profile="seller").first()
    if not restaurant:
        return jsonify({
        'message': 'restaurant not found'
    }), HTTP_404_NOT_FOUND
    
    return jsonify({
        'id': restaurant.id,
        'username':restaurant.username,
        'email':restaurant.email,
        'created_at': restaurant.created_at,
        'updated_at': restaurant.updated_at,
    }), HTTP_200_OK
    

# delete a single restaurant providing an Id with the need for authentication 
@restaurants.delete('/<int:id>')
@login_required
def delete_a_restaurants(id):
    if current_user.is_admin:
        restaurant = User.query.filter_by(id=id, profile="seller").first()
        if not restaurant:
            return jsonify({
            'message': 'restaurant not found'
        }), HTTP_404_NOT_FOUND
    db.session.delete(restaurant)
    db.session.commit()
    
    return jsonify({
        'message': "Deleted successfully"}), HTTP_204_NO_CONTENT