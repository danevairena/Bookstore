from api import db

# Import blueprint
from api.auth import bp

from api.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
from flask import redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from api.models import User
from werkzeug.urls import url_parse
from api.auth.email import send_password_reset_email

# The methods argument in the route decorator tells Flask that this view function 
# accepts GET and POST requests, overriding the default, which is to accept only GET requests.
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is logged in avoid navigating to /login page
    # The current_user variable comes from Flask-Login and can be used at any time during the handling to obtain 
    # the user object that represents the client of the request. The value of this variable can be a user object from the database, 
    # which Flask-Login reads through the user loader callback or a special anonymous user object if the user did not log in yet.
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        # To log the user in for real the first step is to load the user from the database. 
        # The username came with the form submission, so I can query the database with that to find the user.
        # The result of filter_by() is a query that only includes the objects that have a matching username.
        # Since there is going to be 1 or 0 results, the query is completed by calling first(), 
        # which will return the user object if it exists, or None if it does not.
        # If there is a match for the username that was provided, can next step is to check if the password with check_password()
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('auth.login'))
        # If the username and password are both correct, then the login_user() function will register the user as logged in, 
        # so that means that any future pages the user navigates to will have the current_user variable set to that user.
        login_user(user, remember=form.remember_me.data)
        # Right after the user is logged in, the value of the next query string argument is obtained. 
        # Flask provides a request variable that contains all the information that the client sent with the request - request.args
        next_page = request.args.get('next')
        # If the login URL does not have a next argument, then the user is redirected to the index page.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    # TODO ---------------
    return 

# Also need to offer users the option to log out of the application
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# View function that is going to handle user registrations
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Make sure the user that invokes this route is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Creates a new user with the username, email and password provided and then writes it to the database
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # Redirect to the login prompt so that the user can log in.
        return redirect(url_for('auth.login'))
    # TODO ----------
    return 

# Reset password request view function.
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # Check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    # send_password_reset_email() looks up the user by the email provided by the user in the form if 
    # the submitted form is validThen finds the user and send a password reset email
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        return redirect(url_for('auth.login'))
    # TODO --------
    return

# Password reset view function.
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    # determine who the user is by invoking the token verification method in the User class
    # This method returns the user if the token is valid, or None if not.
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    # If the token is valid, then there is a second form, in which the new password is requested.
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('auth.login'))
    # TODO ---------
    return 