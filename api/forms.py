# The Flask-WTF extension uses Python classes to represent web forms.
# A form class simply defines the fields of the form as class variables.

from flask_wtf import FlaskForm
# The field types used for this form,imported directly from the WTForms
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
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
    # Since this is a registration form, it is customary to ask the user to type the password two times to reduce the risk of a typo
    # password2 field uses another validator - EqualTo, which will make sure that its value is identical to the first password field.
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    # When you add any methods that match the pattern validate_<field_name>, WTForms takes those as custom validators 
    # and invokes them in addition to the stock validators.
    # Validating username and email is to make sure that the username and email address entered by the user are not already in the database
    # these two methods issue database queries expecting there will be no results. 
    # If a result exists, a validation error is triggered by raising an exception of type ValidationError
    # The message included as the argument in the exception will be the message that will be displayed next to the field for the user to see.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
# Profile editor form
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # TextAreaField is a multi-line box in which the user can enter text. To validate this field is used Length, which will make sure that 
    # the text entered is between 0 and 140 characters, which is the space I have allocated for the corresponding field in the database.
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')