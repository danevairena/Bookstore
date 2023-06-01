# The Flask-WTF extension uses Python classes to represent web forms.
# A form class simply defines the fields of the form as class variables.

from flask_wtf import FlaskForm
# The field types used for this form,imported directly from the WTForms
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    # For each field, an object is created as a class variable in the LoginForm class.
    # Each field is given a description or label as a first argument.
    # The DataRequired validator simply checks that the field is not submitted empty.
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')