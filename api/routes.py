from api import app
from api.forms import LoginForm
from flask import redirect, url_for
from flask_login import current_user, login_user
from api.models import User

@app.route('/')


@app.route('/index')
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
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
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