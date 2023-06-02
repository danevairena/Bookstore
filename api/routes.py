from api import app, db
from api.forms import LoginForm, RegistrationForm
from flask import redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from api.models import User
from werkzeug.urls import url_parse

@app.route('/')


@app.route('/index')
# The way Flask-Login protects a view function against anonymous users is with a decorator called @login_required
@login_required
def index():
    return "Hello, World!"


# The methods argument in the route decorator tells Flask that this view function 
# accepts GET and POST requests, overriding the default, which is to accept only GET requests.
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is logged in avoid navigating to /login page
    # The current_user variable comes from Flask-Login and can be used at any time during the handling to obtain 
    # the user object that represents the client of the request. The value of this variable can be a user object from the database, 
    # which Flask-Login reads through the user loader callback or a special anonymous user object if the user did not log in yet.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
            return redirect(url_for('login'))
        # If the username and password are both correct, then the login_user() function will register the user as logged in, 
        # so that means that any future pages the user navigates to will have the current_user variable set to that user.
        login_user(user, remember=form.remember_me.data)
        # Right after the user is logged in, the value of the next query string argument is obtained. 
        # Flask provides a request variable that contains all the information that the client sent with the request - request.args
        next_page = request.args.get('next')
        # If the login URL does not have a next argument, then the user is redirected to the index page.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        
    # TODO ---------------
    return 


# view function that accepts and validates the data submitted by the user
def login():
    form = LoginForm()

    # When the browser sends the POST request, form.validate_on_submit() is going to gather all 
    # the data, run all the validators attached to fields, and if everything is all right 
    # it will return True, indicating that the data is valid and can be processed by the application.
    if form.validate_on_submit():
        # redirect() function navigates the browser to a different page, given as an argument.
        # url_for() generates an application URL. It uses use the function names instead of URLs.
        # Some URLs have dynamic components in them, so generating those URLs by hand may cause errors
        return redirect(url_for('index'))
    # TODO --------------
    return 404

# Also need to offer users the option to log out of the application
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# View function that is going to handle user registrations
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Make sure the user that invokes this route is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Creates a new user with the username, email and password provided and then writes it to the database
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # Redirect to the login prompt so that the user can log in.
        return redirect(url_for('login'))
    # TODO ----------
    return 