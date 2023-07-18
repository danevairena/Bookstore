from datetime import datetime, timedelta
from api import db, app
from flask import url_for
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
import json, base64, os
import sqlalchemy as sa
from sqlalchemy import orm as so



# Flask-Login knows nothing about databases, so the extension expects that the application will 
# configure a user loader function, that can be called to load a user given the ID.
# The user loader is registered with Flask-Login with the @login.user_loader decorator. 
# The id that Flask-Login passes to the function as an argument needs to be a string
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# This is an auxiliary table that has no data other than the foreign keys, so it's created without an associated model class
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# PaginatedAPIMixin class implemented in a generic way, that any models that need pagination can inherit from
class PaginatedAPIMixin(object):
    @staticmethod
    # The to_collection_dict() method produces a dictionary with the user collection representation, including the items, _meta and _links sections
    # The first three arguments are a Flask-SQLAlchemy query object, a page number and a page size - determine what are the items that are going to be returned.
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # The paginate() method of the query object obtains a page worth of items
        resources = query.paginate(page=page, per_page=per_page,
                                   error_out=False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                # kwargs - additional keyword arguments
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

# The User class inherits from db.Model, a base class for all models from Flask-SQLAlchemy. 
class User(PaginatedAPIMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # adding a token attribute to the user model
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

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

    # The two relationships will return messages sent and received for a given user, and on the Message side of the relationship 
    # will add author and recipient back references.
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    # The last_message_read_time field will have the last time the user visited the messages page, and will be used to determine if there are 
    # unread messages, which will all have a timestamp newer than this field.
    last_message_read_time = db.Column(db.DateTime)

    # Relationship with the notification model
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

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

    def followed_posts_select(self):
        Author = so.aliased(User)
        return Post.select().join(Post.author.of_type(Author)).join(
            Author.followers, isouter=True).group_by(Post).where(
                sa.or_(Post.author == self, User.id == self.id))
    
    # Token generation and verification methods
    # The get_reset_password_token() function returns a JWT token as a string, which is generated directly by the jwt.encode() function.
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
    # The verify_reset_password_token() is a static method, which means that it can be invoked directly from the class.
    # This method takes a token and attempts to decode it by invoking PyJWT's jwt.decode() function
    @staticmethod
    def verify_reset_password_token(token):
        # If the token cannot be validated or is expired, an exception will be raised, the error will be catched and then returns None to the caller.
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        # If the token is valid, then the value of the reset_password key from the token's payload is the ID of the user, so I can load the user and return it.
        return User.query.get(id)

    # The new_messages() helper method actually uses last_message_read_time field to return how many unread messages the user has.
    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()
    
    # This method not only adds a notification for the user to the database, but also ensures that if a notification with the same name already exists, it is removed first.
    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    # to_dict() method converts a user object to a Python representation, which will then be converted to JSON
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            # last_seen field is generated through the isoformat() method
            # The Z at the end is ISO 8601's timezone code for UTC
            'last_seen': self.last_seen.isoformat() + 'Z',
            'about_me': self.about_me,
            'post_count': self.posts.count(),
            'follower_count': self.followers.count(),
            'followed_count': self.followed.count(),
            # Hypermedia links
            # url_for() is used to generate the URLs (which currently point to the placeholder view functions, defined in users.py)
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'followers': url_for('api.get_followers', id=self.id),
                'followed': url_for('api.get_followed', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        # Include the email only when users request their own data
        # include_email flag to determine if that field gets included in the representation or not
        if include_email:
            data['email'] = self.email
        return data
    
    # from_dict() method that achieves the conversion from a Python dictionary to a model
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            # check if I there is a value provided in the data argument, and if there is setattr() sets the new value in the corresponding attribute for the object
            if field in data:
                setattr(self, field, data[field])
        # The new_user argument determines if this is a new user registration, which means that a password is included.
        if new_user and 'password' in data:
            self.set_password(data['password'])

    # The get_token() method returns a token for the user. The token is generated as a random string that is encoded in base64 so that all the characters 
    # are in the readable range. Before a new token is created, this method checks if a currently assigned token has at least a minute left before expiration, 
    # and in that case the existing token is returned.
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    # When working with tokens it is always good to have a strategy to revoke a token immediately, instead of only relying on the expiration date
    # The revoke_token() method makes the token currently assigned to the user invalid, simply by setting the expiration date to one second before the current time.
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    # The check_token() method is a static method that takes a token as input and returns the user this token belongs to as a response. 
    # If the token is invalid or expired, the method returns None.
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

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
    
    
# Message model extends the database to support private messages
# There are two user foreign keys, one for the sender and one for the recipient. The User model can get relationships for these two users, 
# plus a new field that indicates what was the last time users read their private messages
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


# Notification model to keep track of notifications for all users
# A notification is going to have a name, an associated user, a Unix timestamp and a payload
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    # The payload is going to be different for each type of notification, so I'm writing it as a JSON string, 
    # as that will allow me to write lists, dictionaries or single values such as numbers or strings.
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))

