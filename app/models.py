from decimal import Decimal
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from hashlib import md5

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped['Post']=so.relationship(back_populates='author')
    about_me:so.Mapped[Optional[str]]=so.mapped_column(sa.String(140))
    last_seen:so.Mapped[Optional[datetime]]=so.mapped_column(
        default=lambda:datetime.now(timezone.utc))

    def  __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates="posts")

    def __repr__(self):
        return "<Post{}>".format(self.body)


class Motorista(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    cnh: so.Mapped[str] = so.mapped_column(sa.String(9), index=True, unique=True)
    cpf: so.Mapped[str] = so.mapped_column(sa.String(11), index=True, unique=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    veiculos: so.WriteOnlyMapped["Veiculo"] = so.relationship(
        back_populates="motorista"
    )
    telefones: so.WriteOnlyMapped["Telefone"] = so.relationship(
        back_populates="motorista"
    )
    viagens: so.WriteOnlyMapped["Viagem"] = so.relationship(
        back_populates="motorista"
    )


class Veiculo(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    placa: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    modelo: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    marca: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    capacidade: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    # ForeignKey motorista
    motorista_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Motorista.id), index=True
    )
    motorista: so.Mapped[Motorista] = so.relationship(back_populates="veiculos")


class Cliente(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    cpf: so.Mapped[str] = so.mapped_column(sa.String(11), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    telefones: so.WriteOnlyMapped["Telefone"] = so.relationship(
        back_populates="cliente"
    )
    endereco: so.WriteOnlyMapped["Endereco"] = so.relationship(
        back_populates="cliente", 
    )
    viagens: so.WriteOnlyMapped["Viagem"] = so.relationship(
        back_populates="cliente"
    )


class Telefone(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    telefone: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    # ForeignKey motorista
    motorista_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Motorista.id), index=True
    )
    motorista: so.Mapped[Motorista] = so.relationship(back_populates="telefones")
    # ForeignKey cliente
    cliente_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Cliente.id), index=True)
    cliente: so.Mapped[Cliente] = so.relationship(back_populates="telefones")

class Instituicao(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    cnpj: so.Mapped[str] = so.mapped_column(sa.String(14), index=True, unique=True)
    endereco: so.WriteOnlyMapped["Endereco"] = so.relationship(
        back_populates="instituicao", 
    )
    viagens: so.WriteOnlyMapped["Viagem"] = so.relationship(
        back_populates="instituicao"
    )
    
class Endereco(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    cep: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    rua: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    numero: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    bairro: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    cidade: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    uf: so.Mapped[str] = so.mapped_column(sa.String(2), index=True)
    complemento: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    # ForeignKey cliente
    cliente_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Cliente.id),
        index=True, 
        unique=True  # Garante que um cliente tenha no máximo 1 endereço
    ) 
    cliente: so.Mapped[Cliente] = so.relationship(back_populates="endereco")
    # ForeignKey instituição
    instituicao_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Instituicao.id),
        index=True, 
        unique=True  # Garante que uma instituicao tenha no máximo 1 endereço
	)
    instituicao: so.Mapped[Instituicao] = so.relationship(back_populates="endereco")
    

# classe Motorista_Instituicao não será implementada por enquanto
# se houver necessidade, implementamos

class Viagem(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    valor_corrida: so.Mapped[Decimal] = so.mapped_column(sa.Numeric(10, 2)) # até 99999999.99
    data_hora_inicio: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True))
    data_hora_fim: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True))
    # ForeignKey motorista
    motorista_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Motorista.id), 
        index=True
    )
    motorista: so.Mapped[Motorista] = so.relationship(back_populates="viagens")
    # ForeignKey cliente
    cliente_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Cliente.id),
        index=True 
    ) 
    cliente: so.Mapped[Cliente] = so.relationship(back_populates="viagens")
    # ForeignKey instituicao
    instituicao_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Instituicao.id),
        index=True 
    )
    instituicao: so.Mapped[Instituicao] = so.relationship(back_populates="viagens")