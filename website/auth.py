from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        city = request.form.get('city')
        area = request.form.get('area')
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if len(username) < 2:
            flash('Username must be greater than 2 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(city) < 2:
            flash('City must be greater than 2 characters.', category='error')
        elif len(area) < 2:
            flash('Area must be greater than 2 characters.', category='error')
        elif len(telephone) < 4:
            flash('Telephone must be greater than 4 characters.', category='error')
        elif password != confirm_password:
            flash('Passwords must match', category='error')
        elif len(password) < 4:
           flash('Password must be greater than 4 characters.', category='error')
        else:
            flash('Account created successfully', category='success')
        
    return render_template('sign_up.html')