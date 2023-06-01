# The configuration settings are defined as class variables inside the Config class.
# Flask and some of its extensions use the value of the secret key as a cryptographic key, useful to generate signatures or tokens.
# The Flask-WTF extension uses the secret key to protect web forms against a nasty attack called Cross-Site Request Forgery

import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'