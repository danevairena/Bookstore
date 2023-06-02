# The Flask-WTF extension uses Python classes to represent web forms.
# A form class simply defines the fields of the form as class variables.

from flask_wtf import FlaskForm
# The field types used for this form,imported directly from the WTForms
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length
from api.models import User

# Profile editor form
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # TextAreaField is a multi-line box in which the user can enter text. To validate this field is used Length, which will make sure that 
    # the text entered is between 0 and 140 characters, which is the space I have allocated for the corresponding field in the database.
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username


    # Check if the username entered in the form does already exists in the database, but with one exception - if the user leaves the original 
    # username untouched, then the validation should allow it, since that username is already assigned to that user.
    # validate_username() is an overloaded constructor that accepts the original username as an argument
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

# Form where the only thing the user needs to do is click on "Follow" or "Unfollow", without submitting any data            
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

# Listing submission form.
class PostForm(FlaskForm):
    post_title = TextAreaField('Title', validators=[
        DataRequired(), Length(min=1, max=50)])
    description = TextAreaField('Description', validators=[
        DataRequired(), Length(min=1, max=200)])
    price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')