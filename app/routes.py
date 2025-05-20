from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify, session
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

    # Apenas para o próprio usuário, adiciona as viagens da sessão
    if current_user == user:
        user.viagens_agendadas = session.get('viagens_agendadas', [])
    else:
        user.viagens_agendadas = []

    return render_template('user.html', user=user)

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
        flash('Mudanças salvas com sucesso.')
        return redirect(url_for('user', username=current_user.nome))
    elif request.method=='GET':
        form.username.data=current_user.nome
        form.email.data=current_user.email
    return render_template('edit_profile.html',title='EditProfile',
                            form=form)

@app.route('/agendar', methods=['POST'])
@login_required
def agendar_viagem():
    dados = request.get_json()

    if not dados:
        return jsonify({'error': 'Dados ausentes'}), 400

    viagem = {
        'origem': dados.get('origem'),
        'destino': dados.get('destino'),
        'data': dados.get('data'),
        'preco': dados.get('preco'),
        'ida': dados.get('ida'),
        'volta': dados.get('volta')
    }

    # Inicializa a lista se ainda não existir
    if 'viagens_agendadas' not in session:
        session['viagens_agendadas'] = []

    # Adiciona a viagem à sessão
    viagens = session['viagens_agendadas']
    viagens.append(viagem)
    session['viagens_agendadas'] = viagens

    return jsonify({'success': True})

@app.route('/remover_viagem', methods=['POST'])
@login_required
def remover_viagem():
    dados = request.get_json()
    try:
        index = int(dados.get('index'))
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Índice inválido"}), 400

    if "viagens_agendadas" in session and 0 <= index < len(session["viagens_agendadas"]):
        session["viagens_agendadas"].pop(index)
        session.modified = True
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Índice fora do intervalo"}), 400

@app.route('/api/users')
def api_users():
    users = Cliente.query.all()  
    user_list = [
        {"id": u.id, "nome": u.nome, "email": u.email}
        for u in users
    ]
    return jsonify(user_list)
