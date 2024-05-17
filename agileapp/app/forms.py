from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,Length
import sqlalchemy as sa
from app import db
from app.models import User
import re

def checkNames(form,field):
    if not re.match("^[a-zA-Z ]*$",field.data):
        raise ValidationError("Invalid characters. Use only characters and whitespaces.")
    
def checkPassword(form,field):
    if not re.search("[!@#$%^&*(),.?:}{\"|<>]",field.data):
        raise ValidationError("Password should contain atleast one special character")
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(),checkNames])
    lastname = StringField('Last Name', validators=[DataRequired(),checkNames])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=30),checkPassword])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Email already registered. Please use a different email address.')

class AddItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    photos = FileField('Photos', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Allowed format: jpg, jpeg, png')])
    tags = StringField('Tags', validators=[DataRequired()])
    submit = SubmitField('Publish')