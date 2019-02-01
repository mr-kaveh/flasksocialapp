from flask import Blueprint, render_template, request, redirect, session, url_for, abort
from forms import BaseUserForm, RegisterForm, EditForm
import bcrypt

from user.models import User
from user.forms import RegisterForm, LoginForm

# Creating user_app Blueprint
user_app = Blueprint('user_app', __name__)


@user_app.route('/register', methods=['Get', 'POST'])
def register():
    '''
    Registration
    :return: resgister.html Template
    '''
    form = RegisterForm() # RegisterForm Class Instantiating
    if form.validate_on_submit():
        salt = bcrypt.gensalt() # Generating Salt
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt) # Generating Hashed Password
        # Instantiating The User Model Class
        # These are Database Fields which are
        # defined in the user.models
        user = User(
            username=form.username.data,
            password=hashed_password,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.save() # Saves the record to mongodb
        return 'User Registered'
    return render_template('user/register.html', form=form)


@user_app.route('/login', methods=['Get', 'POST'])
def login():
    '''
    Login
    :return:
    '''
    form = LoginForm() # LoginForm Class Instantiating
    error = None
    # if there is a 'next' argument in request
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next')
    if form.validate_on_submit():
        # Instantiating User Class and Querying the Database
        user = User.objects.filter(username=form.username.data).first()
        if user:
            # Checking the input password with the one in the Database
            # All The Passwords must be encoded to UTF-8
            if bcrypt.hashpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
                session['username'] = form.username.data # Session Variable
                # Processing next
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return 'User Logged in'
            else:
                user = None
        if not user:
            error = 'Incorrect Credentials'

    return render_template('user/login.html', form=form, error=error)

@user_app.route('/logout', methods=['Get', 'POST'])
def logout():
    session.pop('username')
    return redirect(url_for(user_app.login))

@user_app.route('/<username>', methods=['Get', 'POST'])
def profile(username):
    edit_profile = False
    user = User.objects.filter(username=username).first()
    if session.get('username') and user.username == session.get('username'):
        edit_profile = True
    if user:
        return render_template('user/profile.html', user=user, edit_profile=edit_profile)
    else:
        abort(404)


@user_app.route('/edit', methods=['Get', 'POST'])
def edit():
    error = None
    message = None
    user = User.objects.filter(username=session.get('username')).first()
    if user:
        form = EditForm(obj=user)
        if form.validate_on_submit():
            if user.username != form.username.data:
                if User.objects.filter(username=form.username.data.lower()).first:
                    error = 'Username Already Existes'
                else:
                    session['username'] = form.username.data.lower()
                    form.username.data = form.username.data.lower()
        if user.email != form.email.data:
            if User.objects.filter(email=form.email.data.lower()).first():
                error = 'Email Already Exists'
            else:
                form.email.data = form.email.data.lower()
        if not error:
                form.populate_obj(user)
                user.save()
                message = 'Profile Updated'
        return render_template('user/edit.html', form=form, error=error, message=message)
    if not user:
        abort(404)


