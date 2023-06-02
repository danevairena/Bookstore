from api import app, db
from api.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm, ResetPasswordRequestForm
from api.forms import ResetPasswordForm
from flask import redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from api.models import Post, User
from werkzeug.urls import url_parse
from datetime import datetime
from api.email import send_password_reset_email

@app.route('/', methods=['GET', 'POST'])

@app.route('/index', methods=['GET', 'POST'])
# The way Flask-Login protects a view function against anonymous users is with a decorator called @login_required
@login_required
def index():
    # The form processing logic inserts a new Post record into the database.
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        # Redirecting is to avoid re-submitting the form like re-fresh page does
        return redirect(url_for('index'))
    # Display real posts
    # Determine the page number to display, either from the page query string argument or a default 
    # of 1, and then use the paginate() method to retrieve only the desired page of results.
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    # The next_url and prev_url in these two view functions are going to be set to a URL returned by 
    # url_for() only if there is a page in that direction.
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    # TODO ---------
    return 

# Works like the home page, but it shows posts from all user, instead of only the followed ones
@app.route('/explore')
@login_required
def explore():
    # Determine the page number to display, either from the page query string argument or a default 
    # of 1, and then use the paginate() method to retrieve only the desired page of results.
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    # The next_url and prev_url in these two view functions are going to be set to a URL returned by 
    # url_for() only if there is a page in that direction.
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    # TODO ---------
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



# User profile view function
# URL component that is surrounded by < and > is dynamic - <username>
@app.route('/user/<username>')
@login_required
def user(username):
    # Try to load the user from the database using a query by the username.
    # first_or_404(), which works exactly like first() when there are results, 
    # but in the case that there are no results automatically sends a 404 error back to the client.
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    # url_for() function need the extra username argument, because they are pointing back at the user profile page, 
    # which has this username as a dynamic component of the URL
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    # Follow or unfollow button needs instance of an EmptyForm object (then pass it)
    # To reuse the EmptyForm() instance for both the follow and unfollow forms, you need to pass a value argument when rendering the submit button
    form = EmptyForm()
    # TODO ------------
    return 

# Recording the last visit time for a user
# The @before_request decorator register the decorated function to be executed right before the view function
# This is code that I want to execute before any view function in the application, and I can have it in a single place.
@app.before_request
def before_request():
    # checks if the current_user is logged in, and in that case sets the last_seen field to the current time
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # Commit the database session, so that the change made above is written to the database
        db.session.commit()


# Edit profile view function
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    # If validate_on_submit() returns True - copy the data from the form into the user object and then write the object to the database.
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for('edit_profile'))
    # Check request.method, which will be GET for the initial request, and POST for a submission that failed validation
    # If the browser sent a GET request, need to respond by providing an initial version of the form template
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    # TODO -------------
    return 


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    # The only reason why the validate_on_submit() call can fail is if the CSRF token is missing or invalid, 
    # so in that case just redirect the application back to the home page
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:        
            return redirect(url_for('index'))
        if user == current_user:
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    # The only reason why the validate_on_submit() call can fail is if the CSRF token is missing or invalid, 
    # so in that case just redirect the application back to the home page
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            return redirect(url_for('index'))
        if user == current_user:
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))