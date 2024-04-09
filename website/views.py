from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/add_food')
@login_required
def add_restaurant():
    profile = current_user.profile
    if profile != "seller":
        flash('Sorry You must be a seller to access this page', category='error')
        return redirect(url_for('views.home'))
    return render_template('adding_food.html', user=current_user)