from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import sqlalchemy as sa
from app import db
from app.models import Cliente

class LoginForm(FlaskForm):
    username = StringField('Nome', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Logar')

class RegistrationForm(FlaskForm):
    username = StringField('Nome',validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(),Length(11, 11)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Senha',validators=[DataRequired()])
    password2 = PasswordField('Repetir Senha', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self,username):
        user = db.session.scalar(sa.select(Cliente).where(
            Cliente.nome==username.data))
        if user is not None:
            raise ValidationError('Pleaseuseadifferentusername.')
    
    def validate_email(self,email):
        user = db.session.scalar(sa.select(Cliente).where(
            Cliente.email==email.data))
        if user is not None:
            raise ValidationError('Pleaseuseadifferentemailaddress.')
        
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    # about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
