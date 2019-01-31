from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError
from user.models import User
import re


class RegisterForm(Form):
    '''
    Registration Form Elements.
    '''
    first_name = StringField('First Name', [validators.Required()])
    last_name = StringField('Last Name', [validators.Required()])
    email = EmailField('Email Address', [
        validators.Required(),
        validators.Email()
    ])
    username = StringField('Username', [
        validators.Required(),
        validators.length(min=4, max=25)
    ])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Password Must Match'),
        validators.length(min=4, max=80)
    ])
    confirm = PasswordField('Repeat Password')

    def validate_username(form, field):
        if User.objects.filter(username=field.data).first():
            raise ValidationError("Username Already Exists")

    def validate_email(form, field):
        if User.objects.filter(email=field.data).first():
            raise ValidationError("Email Already Exists")
        if not re.match('^[a-zA-Z0-9_-]{4,25}$', field.data):
            raise ValidationError('Invalid Username')


class LoginForm(Form):
    username = StringField('Username', [
        validators.Required(),
        validators.length(min=4, max=25)
    ])
    password = PasswordField('Password', [
        validators.Required(),
        validators.length(min=4, max=80)
    ])