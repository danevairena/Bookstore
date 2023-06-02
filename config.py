# The configuration settings are defined as class variables inside the Config class.
# Flask and some of its extensions use the value of the secret key as a cryptographic key, useful to generate signatures or tokens.
# The Flask-WTF extension uses the secret key to protect web forms against a nasty attack called Cross-Site Request Forgery

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # The Flask-SQLAlchemy extension takes the location of the application's database from the SQLALCHEMY_DATABASE_URI configuration variable.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Sending a signal to the application every time a change is about to be made in the database is disabled
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    POSTS_PER_PAGE = 10