# In Flask, a blueprint is a logical structure that represents a subset of the application.
from flask import Blueprint

# The contents of a blueprint are initially in a dormant state. To associate these elements, 
# the blueprint needs to be registered with the application. During the registration, all the elements 
# that were added to the blueprint are passed on to the application.
# The Blueprint class takes the name of the blueprint, the name of the base module
bp = Blueprint('errors', __name__)

# This import is at the bottom to avoid circular dependencies.
from api.errors import handler