from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Food, user_food
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged In successfully!', category='success')
                login_user(user, remember=True)
                if user.profile == 'seller':
                    return redirect(url_for('views.add_restaurant'))
                return redirect(url_for('views.home'))
            else:
                flash('Email or password may be incorrect try again', category='error')
        else:
            flash('Account does not exist', category='error')
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        city = request.form.get('city')
        area = request.form.get('area')
        telephone = request.form.get('telephone')
        profile = request.form.get('profile')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email already exist', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 2 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(city) < 2:
            flash('City must be greater than 2 characters.', category='error')
        elif len(area) < 2:
            flash('Area must be greater than 2 characters.', category='error')
        elif len(telephone) < 4:
            flash('Telephone must be greater than 4 characters.', category='error')
        elif profile == "":
            flash('You must choose a profile', category='error')
        elif password != confirm_password:
            flash('Passwords must match', category='error')
        elif len(password) < 4:
           flash('Password must be greater than 4 characters.', category='error')
        else:
            new_user = User(username=username, email=email, city=city, area=area, telephone=telephone, profile=profile, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully', category='success')
            return redirect(url_for('auth.login'))
    return render_template('sign_up.html', user="")
