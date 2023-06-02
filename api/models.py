from datetime import datetime
from api import db
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



# Flask-Login knows nothing about databases, so the extension expects that the application will 
# configure a user loader function, that can be called to load a user given the ID.
# The user loader is registered with Flask-Login with the @login.user_loader decorator. 
# The id that Flask-Login passes to the function as an argument needs to be a string
@login.user_loader
def load_user(id):
    return User.query.get(int(id))



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


# The new Post class will represent listings posted by users   
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(50))
    description = db.Column(db.String(200))
    # The timestamp field is going to be indexed, which is useful if you want to retrieve posts in chronological order
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # The user_id field references an id value from the users table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.post_title)