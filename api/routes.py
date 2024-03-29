from mmap import PAGESIZE
from api import app, db
from api.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm, ResetPasswordRequestForm
from api.forms import ResetPasswordForm, MessageForm
from flask import jsonify, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from api.models import Post, User, Message, Notification
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

@app.route('/homefeed', methods=['GET'])
def homefeed():
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
    return posts


@app.route('/userfeed', methods=['GET'])
@login_required
def userfeed():
    """Retrieve the user's post feed"""
    user = current_user().paginate(
        page=PAGESIZE, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    return user.followed_posts_select()

# Works like the home page, but it shows posts from all user, instead of only the followed ones
@app.route('/explore')
def explore():
    # Determine the page number to display, either from the page query string argument or a default 
    # of 1, and then use the paginate() method to retrieve only the desired page of results.
    page = request.args.get('page', 1, type=int)
    posts = Post.select().all().paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    # The next_url and prev_url in these two view functions are going to be set to a URL returned by 
    # url_for() only if there is a page in that direction.
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    
    return posts

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
    

# Reset password request view function.
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # Check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    # send_password_reset_email() looks up the user by the email provided by the user in the form if 
    # the submitted form is validThen finds the user and send a password reset email
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        return redirect(url_for('login'))
    # TODO --------
    return

# Password reset view function.
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # determine who the user is by invoking the token verification method in the User class
    # This method returns the user if the token is valid, or None if not.
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    # If the token is valid, then there is a second form, in which the new password is requested.
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    # TODO ---------
    return 

# View function to handle sending private message
@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
# The action of sending a private message is carried out by adding a new Message instance to the database.
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        # Update notifications for the user
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        return redirect(url_for('main.user', username=recipient))
    # TODO -------------
    return 

# View messages route
# Works in a similar way to the index and explore pages, including full support for pagination
@app.route('/messages')
@login_required
def messages():
    # update the User.last_message_read_time field with the current time
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    # Querying the Message model for the list of messages, sorted by timestamp from newer to older.
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page=page, per_page=app.config['MESSAGES_PER_PAGE'],
            error_out=False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    # TODO -------
    return 

# Route that the client can use to retrieve notifications for the logged in user
@app.route('/notifications')
@login_required
# Function that returns a JSON payload with a list of notifications for the user. Each notification is given as a dictionary 
# with three elements, the notification name, the additional data that pertains to the notification (such as the message count), 
# and the timestamp. The notifications are delivered in the order they were created, from oldest to newest.
def notifications():
    # The since option can be included in the query string of the request URL, with the unix timestamp of the starting time, 
    # as a floating point number. Only notifications that occurred after this time will be returned if this argument is included.
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

