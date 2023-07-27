import json
from os.path import dirname, join, exists
from .data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    # Root Path to the file folder
    _project_root = dirname(dirname(__file__))

    def __init__(self, filename):
        file_path = join(self._project_root, 'data', filename)
        self.filename = file_path

    def create_file(self):
        """ Creates file if file does not exist. If file exists, do nothing"""
        if not exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump([], file)

    @property
    def get_all_users(self):
        """ Loads file and returns all users """

        # If file does not exists, create the file, else do nothing
        self.create_file()

        try:
            with open(self.filename, 'r') as json_file:
                data = json.load(json_file)
            return data
        except json.JSONDecodeError as e:
            print("JSON Decode Error: {e}")
            return None

    def get_user_movies(self, user_id):
        """ Return a list of all movies for a given user """
        users = self.get_all_users

        for user in users:
            if user['id'] == user_id:
                return user['movies']

    def get_user_by_id(self, user_id):
        """ Return a user with a given user_id """
        users = self.get_all_users
        for user in users:
            if user['id'] == user_id:
                return user
        # If user not found, return None
        return None

    def get_user_by_username(self, username):
        """ """
        users = self.get_all_users
        for user in users:
            if user['username'] == username:
                return user
        return None

    def get_user_by_email(self, email):
        """ """
        users = self.get_all_users
        for user in users:
            if user["email"] == email:
                return user
        return None

    def save_user(self, user):
        """ Saves users to the Json file """

        users = self.get_all_users
        users.append(user)

        with open(self.filename, 'w') as file:
            json.dump(users, file, indent=4)

    def save_users(self, users):
        """ Saves users to the Json file """

        with open(self.filename, 'w') as file:
            json.dump(users, file, indent=4)

    def save_user_movies(self, user_movies, user_id):
        """ Saves users to the Json file """

        users = self.get_all_users
        for user in users:
            if user['id'] == user_id:
                user['movies'] = user_movies

        with open(self.filename, 'w') as file:
            json.dump(users, file, indent=4)


class MoviesInfo:
    def __init__(self, movies_lst: list):
        self._movies = movies_lst

    @property
    def total_favourite_movies(self):
        return len(self._movies)

    @property
    def high_rated_movies(self):
        return len([movie['rating'] if 'rating' in self._movies and movie['rating'] > 7 else None for movie in \
                    self._movies])

    @property
    def worst_movie_rating(self):
        movie_ratings = [float(movie['rating']) for movie in self._movies if (movie is not None) and (movie['rating']  != 'N/A')]
        if movie_ratings:
            return min(movie_ratings)
        return movie_ratings

    @property
    def recent_movie_release(self):
        return len([movie['year'] if 'year' in self._movies and movie['year'] > 2021 else None for movie in \
                    self._movies])

    @property
    def total_movies_watched(self):

        watched_movies_count = 0
        for movie in self._movies:
            if (movie is not None) and (movie['watched'].lower() == 'yes'):
                watched_movies_count += 1
        return watched_movies_count

    @property
    def total_movies_with_award(self):

        movies_award_count = 0
        for movie in self._movies:
            if (movie is not None) and (movie['awards'].lower() != 'n/a'):
                movies_award_count += 1
        return movies_award_count

    @property
    def movies_count_by_countries(self):

        movies_country_count = {}

        for movie in self._movies:
            if movie is not None:
                if  ',' in movie['country']:
                    country_1, country_2 = movie['country'].split(',')[:2]
                    if country_1 not in movies_country_count:
                        movies_country_count[country_1] = 1
                    elif country_2 not in movies_country_count:
                        movies_country_count[country_2] = 1
                    else:
                        movies_country_count[country_1] += 1
                        movies_country_count[country_2] += 1
                else:
                    if movie['country'] not in movies_country_count:
                        movies_country_count[movie['country']] = 1
                    else:
                        movies_country_count[movie['country']] += 1
        if movies_country_count:
            return sorted(movies_country_count.items(), key=lambda item: item[1], reverse=True)[:2]
        return movies_country_count

    @property
    def top_rated_movie_name(self):

        movies_and_ratings = {}

        for movie in self._movies:
            if (movie is not None) and (movie['name'] not in movies_and_ratings):
                if movie['rating'] != 'N/A':
                    movies_and_ratings[movie['name']] = float(movie['rating'])
        if movies_and_ratings:
            return sorted(movies_and_ratings.items(), key=lambda item: item[1], reverse=True)[0]

        return movies_and_ratings
