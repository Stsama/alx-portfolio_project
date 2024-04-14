from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user


views = Blueprint('views', __name__)
# Display the home page
@views.route('/')
def home():
    return render_template('home.html')
