# The Flask-WTF extension uses Python classes to represent web forms.
# A form class simply defines the fields of the form as class variables.

from flask_wtf import FlaskForm
# The field types used for this form,imported directly from the WTForms
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from api.models import User


class LoginForm(FlaskForm):
    # For each field, an object is created as a class variable in the LoginForm class.
    # Each field is given a description or label as a first argument.
    # The DataRequired validator simply checks that the field is not submitted empty.
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

# Registration form, so that users can register themselves through a web form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # The second validator - Email will ensure that what the user types in this field matches the structure of an email address
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')