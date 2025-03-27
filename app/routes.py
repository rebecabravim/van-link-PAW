# app/routes.py

from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from urllib.parse import urlsplit
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app.models import User

@app.route('/')
@app.route('/index')
def index(): 
    user = {'username': 'Carnaval'}
    posts = [
        {
            'author': {'username': 'Joao'},
            'body': 'Belo dia em Vila Velha!'
        },
        {
            'author': {'username': 'Maria'},
            'body': 'Bora pra folia!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts = posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
