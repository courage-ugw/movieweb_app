from movieweb_app.utils import login_manager
from movieweb_app.data_manager.json_data_manager import JSONDataManager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    # Query your database or data source to get the user by user_id
    user_data = JSONDataManager('movies.json').get_user_by_id(int(user_id))
    return User(user_data.get('id', None), user_data.get('name', None), user_data.get('username', None),
                user_data.get('email', None), user_data.get('password', None), user_data.get('date_joined', None),
                user_data.get('movies', None))


class User(UserMixin):
    def __init__(self, user_id, name, username, email, password, date_joined, movies):
        self._id = user_id
        self._name = name
        self._username = username
        self._email = email
        self._password = password
        self._date_joined = date_joined
        self._movies = movies

    def get_id(self):
        return str(self._id)

    def __repr__(self):
        return f"User({self._id}, {self._name}, {self._username}, {self._email}, {self._password}," \
               f" {self._date_joined}, {self._movies})"
