from flask import Blueprint, render_template, request, flash, redirect, url_for
from movieweb_app.data_manager.json_data_manager import JSONDataManager
from flask_login import login_user, login_required, logout_user, current_user
from movieweb_app.blueprints.users_manager.user_auth import SignupForm, SigninForm
from movieweb_app import bcrypt, models
from datetime import datetime
import secrets

# Initializing the Blueprint object
users_bp = Blueprint('users', __name__, template_folder='templates', static_folder='static',
                     static_url_path='users_manager/static', url_prefix='/users')

# Initializing the data manager object
data_manager = JSONDataManager('movies.json')


@users_bp.route('/', methods=['GET'])
def users_list():
    """ Displays the list of all users """

    users = data_manager.get_all_users

    if current_user.is_active:
        user = data_manager.get_user_by_id(current_user._id)
        users.remove(user)
    else:
        flash('Sign in to start Adding your favorite movies!')

    return render_template('users.html', users=users, current_user=current_user)


@users_bp.route('/user_movies/<int:user_id>', methods=['GET'])
@login_required
def user_movies(user_id):
    """ Displays a specific user's movies """
    user_movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user_movies=user_movies)


@users_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    """ Adds a new user """

    # Handle the form submission and user creation
    if request.method == 'POST':

        # Get username
        user_name = request.form.get('user_name')

        # Assign id to the user
        users = data_manager.get_all_users
        user_id = max([user['id'] for user in users]) + 1

        # Add user to users
        users.append({
            "id": user_id,
            "name": user_name,
            "movies": []
        })

        # Save users to JSON file
        data_manager.save_user(users)
        users_list()
    else:
        # Handles GET request
        return render_template('user_signup.html')


@users_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """ signup user into the app """

    # If user is already signed in and clicks on the `Get Started Button`
    # then redirect user to users_list
    if current_user.is_authenticated:
        return redirect(url_for('users.users_list'))

    # Initialize the sign-up form object
    form = SignupForm()

    if form.validate_on_submit():
        # Hash the user's password
        password_hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Convert the form data to a dictionary
        user = {
            "id": secrets.token_hex(4),
            "name": form.display_name.data,
            "username": form.username.data,
            "email": form.email.data,
            "password": password_hashed,
            "date_joined": datetime.utcnow().strftime('%d-%b-%Y'),
            "movies": []
        }

        # Save the user data to the JSON file using JSONDataManager
        data_manager.save_user(user)

        # Send Success Message to user
        flash('Your account has been created! You can now signin', 'success')

        return redirect(url_for('users.signin'))

    return render_template('user_signup.html', form=form)


@users_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    """ signup user into the app """

    # If user is already signed in and clicks on the `Get Started Button`
    # then redirect user to users_list
    if current_user.is_authenticated:
        return redirect(url_for('users.users_list'))

    # Initialize the sign-up form object
    form = SigninForm()

    if form.validate_on_submit():
        user = JSONDataManager('movies.json').get_user_by_email(form.email.data)

        if user and bcrypt.check_password_hash(user.get('password'), form.password.data):
            user_data = models.User(user.get('id', None), user.get('name', None), user.get('username', None),
                                    user.get('email', None),user.get('password', None), user.get('date_joined', None),
                                    user.get('movies', None))
            login_user(user_data)

            flash('Click `Account Tab` to add Movies', 'success')

            next_page = request.args.get('next')

            return redirect(next_page or url_for('users.users_list'))
        else:
            flash('Error: Please check your email and password', 'error')

    return render_template('user_signin.html', form=form)


@users_bp.route('/logout')
def signout():
    """ signout user from the app """

    logout_user()
    return redirect(url_for('home.home'))