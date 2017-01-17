from flask import Blueprint, request, render_template, \
                  flash, g, redirect, url_for
from flask_login import login_user, logout_user, current_user

from app import db, flask_bcrypt
from app.auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    user = User(
        request.form['name'],
        flask_bcrypt.generate_password_hash(request.form['password']),
        request.form['email']
    )
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    email = request.form['email']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(email=email).first()
    if registered_user and flask_bcrypt.check_password_hash(
            registered_user.password, password):
        login_user(registered_user, remember=remember_me)
        flash('Logged in successfully')
        return redirect(request.args.get('next') or url_for('index'))

    flash('Email or Password is invalid', 'error')
    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@auth.before_request
def before_request():
    g.user = current_user
