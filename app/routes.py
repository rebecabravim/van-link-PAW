from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm , RegistrationForm, EditProfileForm
from urllib.parse import urlsplit
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app.models import Cliente
from datetime import datetime, timezone

@app.route('/')
@app.route('/index')
@login_required
def index():
    user={'username':'Wanderson'}
    posts=[
        {
            'author':{'username': 'Joao'},
            'body': 'Belo dia em Vila Velha!'
        },
        {
           'author': {'username': 'Maria'},
           'body': 'Bora para o cinema hoje?'
        },
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return  redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(Cliente).where(Cliente.nome == form.username.data)) 
        if user is None or not user.check_password(form.password.data):
            flash('Senha ou Nome inválidos')
            return  redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'SignIn', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Cliente(nome=form.username.data, cpf=form.cpf.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Parabéns, agora você é um usuário registrado!')
        return redirect(url_for('login', success=True))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(Cliente).where(Cliente.nome == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

# cria banco ao subir o servidor web, necessário apenas uma vez
# @app.before_request
# def ensure_tables_exist():
#     db.create_all()

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile',methods=['GET', 'POST'])
@login_required
def edit_profile():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.nome=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method=='GET':
        form.username.data=current_user.nome
        form.email.data=current_user.email
    return render_template('edit_profile.html',title='EditProfile',
                            form=form)


@app.route('/api/users')
def api_users():
    users = Cliente.query.all()  
    user_list = [
        {"id": u.id, "nome": u.nome, "email": u.email}
        for u in users
    ]
    return jsonify(user_list)
