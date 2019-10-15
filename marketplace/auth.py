from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db


# create a blueprint
bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if(form.validate_on_submit()):
        user_name = form.username.data
        password = form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        # if there is no user with matching username
        if u1 is None:
            error = 'Incorrect User Name'
            # if there is an incorrect username
        elif not check_password_hash(u1.password_hash, password):
            error = 'Incorrect Password'
        if error is None:
            print('no errors')
            # log in the user
            login_user(u1)

            return redirect(url_for('main.index'))
        else:
            print(error)
            flash(error)
    return render_template('user.html', form=form, heading='Login')


@bp.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print('Registration form Submitted')
        # retrieve Username, Pwd & Email
        uname = form.username.data
        pwd = form.password.data
        email = form.email.data
        pwd_hash = generate_password_hash(pwd)

        # query db to check if there are any existing users already registered with that username
        user_exists = User.query.filter_by(name=uname).first()

        if user_exists:
            register_error = "User \"{}\" already exists, please try another username" .format(
                uname)
            flash(register_error)
            return redirect(url_for('auth.register'))

        # create a new db user

        new_user = User(name=uname, password_hash=pwd_hash, emailid=email)
        db.session.add(new_user)
        db.session.commit()
        print('COMMITED TO DB')

        # redirect

        return redirect(url_for('auth.login'))

    return render_template('user.html', form=form, heading='Register')
