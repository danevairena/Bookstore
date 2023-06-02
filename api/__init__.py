from flask import Flask, request, current_app
from config import Config
import os

# SQLAlchemy package is an Object Relational Mapper(ORM), that allows the application to manage 
# a database using high-level entities such as classes, objects and methods instead of tables and SQL.
# The job of the ORM is to translate the high-level operations into database commands.
from flask_sqlalchemy import SQLAlchemy

# Relational databases are centered around structured data, so when the structure changes 
# the data that is already in the database needs to be migrated to the modified structure
from flask_migrate import Migrate

# Flask-Login extension manages the user logged-in state, so that for example users can log in to the application 
# and then navigate to different pages while the application "remembers" that the user is logged in.
from flask_login import LoginManager

# Flask extension for sending e-mails
from flask_mail import Mail


# The database is going to be represented in the application by the database instance. 
# The database migration engine will also have an instance. 
db = SQLAlchemy()
migrate = Migrate()

# As with other extensions, Flask-Login needs to be created and initialized
login = LoginManager()

# Flask-Login provides feature that forces users to log in before they can view certain pages of the application. 
# If a user who is not logged in tries to view a protected page, flask will automatically redirect the user to the login form
# To implement this feature, Flask-Login needs to know what is the view function that handles logins.
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')

# To use Mail you need to create an instance - object of class Mail
mail = Mail()

# create_app() is a function that constructs a Flask application instance and tells Flask to read and apply the config file
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # The init_app() method must be invoked on the extension instances to bind it to the now known application.
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from api.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from api.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

# This import is at the bottom to avoid circular dependencies.
from api import routes, models