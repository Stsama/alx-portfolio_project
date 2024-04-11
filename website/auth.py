from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User, Food, Order
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import validators  # type: ignore
from constants.http_status_codes import *
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.post('/login')
def login():
    email = request.json.get('email', "")
    password = request.json.get('password', "")
        
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            return jsonify({
                'user':{
                    'username': user.username,
                    'email': user.email,
                    'profile': user.profile
                }
            }), HTTP_200_OK
        
    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED
        

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'User logged out successfully'}), HTTP_200_OK


@auth.post('/register')
def register():
        username = request.json['username']
        email = request.json['email']
        # is_admin = request.json['is_admin']
        profile = request.json['profile']
        password = request.json['password']
        
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'error': 'Your email already exists'}), HTTP_409_CONFLICT
        if len(username) < 2:
            return jsonify({'error': 'username is too short'}), HTTP_400_BAD_REQUEST
        if not username.isalnum() or ' ' in username:
            return jsonify({'error': 'username should be alphanumeric, also no spaces'}), HTTP_400_BAD_REQUEST
        if not validators.email(email):
            return jsonify({'error': 'Your email is not valid'}), HTTP_400_BAD_REQUEST
        if profile == "":
            return jsonify({'error': 'You must choose a profil'}), HTTP_400_BAD_REQUEST
        if len(password) < 4:
          return jsonify({'error': 'password is too short'}), HTTP_400_BAD_REQUEST
        
        new_user = User(username=username, email=email, profile=profile, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
            
        return jsonify({
            'message': 'user created',
            'user':{
                    'username': username, 'email':email, 'profile': profile
            } 
        })
            

@auth.route('/me')
def get_me():
    if current_user.is_authenticated:
        user = current_user
        return jsonify({
            'user':{
                'username': user.username,
                'email': user.email,
                'profile': user.profile
            }
        }), HTTP_200_OK 
    return jsonify({'error':'You should login before !!!'}), HTTP_401_UNAUTHORIZED


@auth.get('/users')
@login_required
def get_all_users():
    if current_user.is_admin:
        users = User.query.all()
        users_data = []
        for user in users:
            new={
                'username':user.username,
                'email':user.email,
                'profile':user.profile
            }
            users_data.append(new)
        return jsonify({
            'users': users_data
        }), HTTP_200_OK
    else:
        return jsonify({'error': 'You are not allowed to check this page'}), HTTP_401_UNAUTHORIZED
    