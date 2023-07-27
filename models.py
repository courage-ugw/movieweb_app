from flask_login import UserMixin


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
