from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '3a691505c8917500f1197a470745c6c7'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    
    
    from .views import views
    from .auth import auth
    from .foods import foods
    from .orders import orders
    from .restaurants import restaurants
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/api/v1/auth")
    app.register_blueprint(foods, url_prefix="/api/v1/foods")
    app.register_blueprint(orders, url_prefix="/api/v1/orders")
    app.register_blueprint(restaurants, url_prefix="/api/v1/restaurants")
    # app.register_blueprint(api, url_prefix="/api/v1/ressorces")
    
    from .models import Food, User, Order
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app


def create_database(app):
        with app.app_context():
            if not path.exists('website/' + DB_NAME):
                db.create_all()
                print('Created Database!')