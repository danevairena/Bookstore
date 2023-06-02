from flask import Flask
from config import Config
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


app = Flask(__name__)
# Tell Flask to read and apply the config file
app.config.from_object(Config)
# As with other extensions, Flask-Login needs to be created and initialized
login = LoginManager(app)

# The database is going to be represented in the application by the database instance. 
# The database migration engine will also have an instance. 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from api import routes, models