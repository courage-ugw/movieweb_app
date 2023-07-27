from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Creates the instance of Login Manager Class
login_manager = LoginManager()

# User will always be redirected here if they attempt to access any page that requires sign in
login_manager.login_view = 'users.signin'
login_manager.login_message_category = 'error'

# Creating the instance of Bycrypt Class
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    # creating secret key for CSRF
    app.config['SECRET_KEY'] = '5722f4a3deabe7bb'

    login_manager.init_app(app)
    bcrypt.init_app(app)

    from movieweb_app.blueprints.index_page.home import home_bp
    from movieweb_app.blueprints.users_manager.users import users_bp
    from movieweb_app.blueprints.movies_manager.movies import movies_bp

    # Registering the blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(movies_bp)

    return app
