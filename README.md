## Comandos para rodar o app web atraves de um ambiente virtual:


### Iniciar ambiente virtual
```
py -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
```

### Instalar bibliotecas
```
py -m pip install --upgrade pip
pip install flask
pip install ipython
pip install flask-wtf
pip install werkzeug
pip install flask-login
pip install flask-sqlalchemy flask-migrate
```
### Rodar
```
set FLASK_APP=bloguvv.py
$env:FLASK_DEBUG = 1
flask run
```
### Inicio BD
```
pip install flask-sqlalchemy flask-migrate
flask db init
```
Segurança:
```
pip install werkzeug
pip install flask-login

```