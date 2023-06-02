from api import app, db
from api.forms import LoginForm, EditProfileForm, EmptyForm, PostForm
from flask import redirect, url_for, request
from flask_login import current_user, login_required
from api.models import Post, User
from datetime import datetime






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











