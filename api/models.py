from datetime import datetime
from api import db

# The User class inherits from db.Model, a base class for all models from Flask-SQLAlchemy. 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
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