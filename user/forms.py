from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.widgets import TextArea
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError
from user.models import User
import re


class BaseUserForm(Form):
    '''
    BaseUserForm class
    '''
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    email = EmailField('Email Address', [
        validators.DataRequired(),
        validators.Email()
    ])
    username = StringField('Username', [
        validators.required(),
        validators.length(min=4, max=25)
    ])
    bio = StringField('Bio',
                      widget=TextArea(),
                      validators=[validators.length(max=160)]
                      )


class RegisterForm(BaseUserForm):
    '''
    RegisterForm which extends BaseUserForm Class
    '''
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password Must Match'),
        validators.length(min=4, max=80)
    ])
    confirm = PasswordField('Repeat Password')

    def validate_username(form, field):
        if User.objects.filter(username=field.data).first():
            raise ValidationError("Username Already Exists")
        if not re.match('^[a-zA-Z0-9_-]{4,25}$', field.data):
            raise ValidationError('Invalid Username')

    def validate_email(form, field):
        if User.objects.filter(email=field.data).first():
            raise ValidationError("Email Already Exists")



class LoginForm(Form):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.length(min=4, max=25)
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.length(min=4, max=80)
    ])

class EditForm(BaseUserForm):
    pass
