from flask import Flask
from config import Config
# SQLAlchemy package is an Object Relational Mapper(ORM), that allows the application to manage 
# a database using high-level entities such as classes, objects and methods instead of tables and SQL.
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Tell Flask to read and apply the config file
app.config.from_object(Config)

from api import routes