from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from movieweb_app.data_manager.json_data_manager import JSONDataManager
from movieweb_app.models import User

# Move bcrypt and login_manager to the global scope
bcrypt = Bcrypt()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    # Query  data source to get the user by user_id
    user_data = JSONDataManager('movies.json').get_user_by_id(int(user_id))
    return User(user_data.get('id', None),
                user_data.get('name', None),
                user_data.get('username', None),
                user_data.get('email', None),
                user_data.get('password', None),
                user_data.get('date_joined', None),
                user_data.get('movies', None))


def create_app():
    app = Flask(__name__)

    # creating secret key for CSRF
    app.config['SECRET_KEY'] = '5722f4a3deabe7bb'

    # Initialize bcrypt and login_manager with the app instance
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # User will always be redirected here if they attempt to access any page that requires sign in
    login_manager.login_view = 'users.signin'
    login_manager.login_message_category = 'error'

    from movieweb_app.blueprints.index_page.home import home_bp
    from movieweb_app.blueprints.users_manager.users import users_bp
    from movieweb_app.blueprints.movies_manager.movies import movies_bp

    # Registering the blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(movies_bp)

    return app