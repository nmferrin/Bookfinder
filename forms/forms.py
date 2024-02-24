from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SubmitField, StringField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from models.models import User

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class RegisterForm(FlaskForm):
    username = StringField('Username',
            validators=[DataRequired(), Length(min=3, max=32)])
    email = StringField('Email',
            validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
            validators=[DataRequired(), Length(min=8, max=64)])
    confirm = PasswordField('Verify password',
            validators=[DataRequired(), EqualTo('password',
            message='Passwords must match')])
    

class ReadingListForm(FlaskForm):
    """Form for creating a new reading list."""
    name = StringField('List Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create Reading List')


class NewBookForReadingListForm(FlaskForm):
    """Form for adding a book to an existing reading list."""
    book_id = SelectField('Select Book', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Book to List')

class EditReadingListForm(FlaskForm):
    '''Form for editing an existing reading list.'''
    reading_list_id = HiddenField('Reading List ID')  # Optional, use if you need to pass the list ID
    name = StringField('List Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Update Reading List')

    