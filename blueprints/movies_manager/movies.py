from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import current_user, login_required

from ...data_manager.json_data_manager import JSONDataManager
from ...movie_data_fetcher.movie_data_fetcher import MovieDataFetcher

# Constant
ONE = 1

# Movies Blueprint
movies_bp = Blueprint('movies', __name__, template_folder='templates', static_folder='static',
                      static_url_path='users_manager/static', url_prefix='/users/account/')

# Creating a data manager object
data_manager = JSONDataManager('movies.json')

# Creates instance the movie data fetcher object that fetches movies data from IMDb movies api
movies_data = MovieDataFetcher()


def unique_id_generator(user_id):
    user_movies = data_manager.get_user_movies(user_id)
    if not any(user_movies):
        return ONE

    return max([movie['id'] for movie in user_movies if movie is not None]) + ONE



def get_movies_data(movie_name, user_id):

    # Get movie data from imdb movie api
    movie_data = movies_data.get_movies_data(movie_name)
    if movie_data:
        try:
            user_movies_data = {
                "id": unique_id_generator(user_id),
                "name": movie_data['Title'],
                "genre": movie_data['Genre'],
                "year": movie_data['Year'],
                "rating": movie_data['imdbRating'],
                "watched": "No",
                "country": movie_data['Country'],
                "poster_url": movie_data['Poster'],
                "movie_plot": movie_data['Plot'],
                "movie_actors": movie_data['Actors'],
                "movie_trailer": movie_data['imdbID'],
                "awards": movie_data['Awards']
            }
            return user_movies_data
        except KeyError:
            pass


@movies_bp.route('<int:user_id>/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie(user_id):
    """ Adds movies to user's list """

    # Fetch user movies from JSON file
    user_movies = data_manager.get_user_movies(user_id)

    # Handle the form submission and movie addition
    if request.method == 'POST':

        # Gets movie_name from the form
        movie_name = request.form.get('movie_name')

        # Gets the new movie data from the api
        new_movies_data = get_movies_data(movie_name, user_id)

        # Adds movie to user's movie list
        user_movies.insert(0, new_movies_data)

        # Save movies to JSON file
        data_manager.save_user_movies(user_movies, user_id)

        flash(f'The {movie_name} has been add to your favourite movie list', 'success')

        # Redirect user to user_movies route to  display the list of user's movies
        return redirect(url_for('users.user_movies', user_id=user_id))

    else:
        # Handles GET request and displays the add movie form to the user
        return render_template('movies_manager.html', user_movies=user_movies, current_user=current_user)


@movies_bp.route('<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def update_movie(user_id, movie_id):
    """ Updates details of a specific movie in a user's movies list """

    # Fetch user movies from JSON file
    user_movies = data_manager.get_user_movies(user_id)

    movie_to_update = next((movie for movie in user_movies if (movie is not None) and (movie['id'] == movie_id)),
                           None)
    if request.method == 'GET':
        # Handle GET request and render the update movie html
        return render_template('update_movie.html',  user_id=user_id, user_movies=movie_to_update)
    else:
        for movie in user_movies:
            # Update movie detail
            if (movie is not None) and (movie['id'] == movie_id):
                movie['name_actors'] = request.form.get('movie_actors')
                movie['movie_genre'] = request.form.get('movie_genre')
                movie['movie_plot'] = request.form.get('movie_plot')
                break

        # Save movies to JSON file
        data_manager.save_user_movies(user_movies, user_id)

        flash(f'{movie_to_update["name"]} has been updated successfully', 'success')

        # Redirects user to the user movie list page
        return redirect(url_for('users.user_movies', user_id=user_id))



@movies_bp.route('<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(user_id, movie_id):
    """ Deletes a specific movie from a user's list """

    # Fetch user movies from JSON file
    user_movies = data_manager.get_user_movies(user_id)

    movie_to_delete = next((movie for movie in user_movies if (movie is not None) and (movie['id'] == movie_id) ), None)

    if movie_to_delete:
        user_movies.remove(movie_to_delete)

    # Save movies to JSON file
    data_manager.save_user_movies(user_movies, user_id)

    flash(f'{movie_to_delete["name"]} has been deleted successfully', 'success')

    # Redirects user to the user movie list page
    return redirect(url_for('users.user_movies', user_id=user_id))


@movies_bp.route('<int:user_id>/watched_movie/<int:movie_id>/<string:watched_status>', methods=['POST'])
@login_required
def watched_movie(user_id, movie_id, watched_status):
    """ Updates details of a specific movie in a user's movies list """

    # Fetch user movies from JSON file
    user_movies = data_manager.get_user_movies(user_id)

    for movie in user_movies:
        # Update the movie watched status
        if (movie is not None) and (movie['id'] == movie_id):
            if watched_status.lower() == 'no':
                movie['watched'] = 'Yes'
                break
            else:
                movie['watched'] = 'No'
                break

    # Save movies to JSON file
    data_manager.save_user_movies(user_movies, user_id)

    # Redirects user to the movies manager page
    return redirect(url_for('movies.add_movie', user_id=user_id))

