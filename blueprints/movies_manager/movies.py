from flask import Blueprint, render_template, url_for, request, redirect
from movieweb_app.data_manager.json_data_manager import JSONDataManager
from movieweb_app.movie_data_fetcher.movie_data_fetcher import MovieDataFetcher

# Movies Blueprint
movies_bp = Blueprint('movies', __name__, template_folder='templates', static_folder='static',
                      static_url_path='users_manager/static', url_prefix='/users/account/')

# Creating a data manager object
data_manager = JSONDataManager('movies.json')

# Creates instance the movie data fetcher object that fetches movies data from IMDb movies api
movies_data = MovieDataFetcher()


@movies_bp.route('<int:user_id>')
def user_account(user_id):
    user = data_manager.get_user_by_id(user_id)
    return render_template('movies_manager.html', user=user)


@movies_bp.route('<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """ Adds movies to user's list """

    # Fetch user movies from JSON file
    user_movies = data_manager.get_user_movies(user_id)

    # Fetch all users
    users = data_manager.get_all_users

    # Handle the form submission and movie addition
    if request.method == 'POST':

        # Gets user_name from the form
        movie_name = request.form.get('movie_name')

        # Get movie data from imdb movie api*********************************************
        movie_data = movies_data.get_movies_data(movie_name)

        # If user's movies list is empty
        if not user_movies:
            user_movies.append({
                'id': 1,
                'name': movie_name,
                'director': movie_data['Director'],
                'year': movie_data['Year'],
                'rating': movie_data['imdbRating']
            })
        else:
            # otherwise create new id for new movie
            new_movie_id = max([movie['id'] for movie in user_movies]) + 1

            user_movies.append({
                'id': new_movie_id,
                'name': movie_name,
                'director': movie_data['Director'],
                'year': movie_data['Year'],
                'rating': movie_data['imdbRating']
            })

        # Add movie to user's movie list
        for user in users:
            if user['id'] == user_id:
                user['movies'] = user_movies

        # Redirect user to user_movies route to  display the list of user's movies
        return redirect(url_for('users.user_movies', user_id=user_id))

    else:
        # Handles GET request and displays the add movie form to the user
        return render_template('movies_manager.html')


@movies_bp.route('<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """ Updates details of a specific movie in a user's movies list """

    # Get user details
    user = data_manager.get_user_by_id(user_id)

    # Handle the form submission and movie update
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        movie_director = request.form.get('movie_director')
        movie_year = request.form.get('movie_year')
        movie_rating = request.form.get('movie_rating')

        for movie in user['movies']:
            if movie['id'] == movie_id:
                movie['name'] = movie_name
                movie['director'] = movie_director
                movie['year'] = movie_year
                movie['rating'] = movie_rating

        # Redirects user to the user movie list page
        return redirect(url_for('users.user_movies', user_id=user_id)), 200
    else:
        # Handle GET request and render the update movie html
        return render_template('update_movie.html', user=user), 200


@movies_bp.route('<int:user_id>/delete_movie/<int:movie_id>', methods=['GET'])
def delete_movie(user_id, movie_id):
    """ Deletes a specific movie from a user's list """

    # Get user details
    user = data_manager.get_user_by_id(user_id)

    # Gets the index of movie to be deleted
    movie_index = 0
    for movie in user['movies']:
        if movie['id'] == movie_id:
            movie_index = user['movies'].index(movie)
            break

    # Deletes the movie
    user['movies'].pop(movie_index)

    # Redirects user to the user movie list page
    return redirect(url_for('users.user_movies', user_id=user_id)), 200
