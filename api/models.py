from datetime import datetime
from api import db, login
from flask import current_app
# Werkzeug implements password hashing - the password is transformed into a long encoded string 
# through a series of cryptographic operations that have no known reverse operation, which means 
# that a person that obtains the hashed password will be unable to use it to obtain the original password.
# The verification process is done with a second function from Werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
# Flask-Login provides class called UserMixin that includes generic implementations that are appropriate for most user model classes
from flask_login import UserMixin
from api import login
# MD5 hashes of the user's email address and generates profile avatars
from hashlib import md5
from time import time
# JSON Web Token
import jwt


# This is an auxiliary table that has no data other than the foreign keys, so it's created without an associated model class
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


# The User class inherits from db.Model, a base class for all models from Flask-SQLAlchemy. 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # db.relationship is not an actual database field, but a high-level view of the relationship between users and posts
    # For a one-to-many relationship, a db.relationship field is normally defined on the "one" side, 
    # and is used as a convenient way to get access to the "many".
    # The first argument to db.relationship is the model class that represents the "many" side of the relationship.
    # The backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object.
    # This will add a post.author expression that will return the user given a post
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    # db.relationship function is used to define the relationship in the model class
    # This relationship links User instances to other User instances
    # Example: let's say that for a pair of users linked by this relationship, the left side user is following the right side user. 
    # The relationship is defined as seen from the left side user with the name followed, because when I query this relationship 
    # from the left side I will get the list of followed users (i.e those on the right side)
    followed = db.relationship(
        # 'User' is the right side entity of the relationship (the left side entity is the parent class)
        # secondary configures the association table that is used for this relationship
        'User', secondary=followers,
        # primaryjoin indicates the condition that links the left side entity (the follower user) with the association table.
        primaryjoin=(followers.c.follower_id == id),
        # secondaryjoin indicates the condition that links the right side entity (the followed user) with the association table.
        secondaryjoin=(followers.c.followed_id == id),
        # backref defines how this relationship will be accessed from the right side entity.
        # lazy is similar to the parameter of the same name in the backref, but this one applies to the left side query instead of the right side.
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    # The __repr__ method tells Python how to print objects of this class
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # With the two methods below, a user object is now able to do secure password verification, 
    # without the need to ever store original passwords.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # The avatar() method of the User class returns the URL of the user's avatar image, scaled to the requested size in pixels.
    def avatar(self, size):
        # To generate the MD5 hash, first need to convert the email to lower case, as this is required by the Gravatar service. 
        # Then, because the MD5 support in Python works on bytes and not on strings, encode the string as bytes before passing it on to the hash function
        # For users that don't have an avatar registered, an "identicon" image will be generated
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    
    # The follow() and unfollow() methods use the append() and remove() methods of the relationship object
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # The is_following() method issues a query on the followed relationship to check if a link between two users already exists. 
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    # Query to obtain the posts from followed users
    def followed_posts(self):
        # First query that returns followed posts by the user 
        # With the join() the database to creates a temporary table that combines data from posts and followers tables
        # The filter() call selects the items in the joined table that have the follower_id column set to this user (keep only the entries that have this user as a follower)
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        # Second query that returns the user's own posts
        own = Post.query.filter_by(user_id=self.id)
        # The "union" operator to combine the two queries into a single one.
        # order_by query sorts the results by the timestamp field of the post in descending order - the first result will be the most recent post
        return followed.union(own).order_by(Post.timestamp.desc())

    # Token generation and verification methods
    # The get_reset_password_token() function returns a JWT token as a string, which is generated directly by the jwt.encode() function.
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')
    # The verify_reset_password_token() is a static method, which means that it can be invoked directly from the class.
    # This method takes a token and attempts to decode it by invoking PyJWT's jwt.decode() function
    @staticmethod
    def verify_reset_password_token(token):
        # If the token cannot be validated or is expired, an exception will be raised, the error will be catched and then returns None to the caller.
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        # If the token is valid, then the value of the reset_password key from the token's payload is the ID of the user, so I can load the user and return it.
        return User.query.get(id)

# Flask-Login knows nothing about databases, so the extension expects that the application will 
# configure a user loader function, that can be called to load a user given the ID.
# The user loader is registered with Flask-Login with the @login.user_loader decorator. 
# The id that Flask-Login passes to the function as an argument needs to be a string
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# The new Post class will represent listings posted by users   
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(50))
    description = db.Column(db.String(200))
    # The timestamp field is going to be indexed, which is useful if you want to retrieve posts in chronological order
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # The user_id field references an id value from the users table
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.post_title)