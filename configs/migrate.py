from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.exc import OperationalError
from urllib.parse import quote_plus
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

connection_str = (
    f"Driver={os.getenv('DB_DRIVER')};"
    f"Server={os.getenv('DB_SERVER')};"
    f"Database={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    f"Encrypt=no"
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc:///?odbc_connect={
    quote_plus(connection_str)}'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


def get_current_time():
    return datetime.now(timezone.utc) - timedelta(hours=3)


class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf_cnpj = db.Column(db.String(128), unique=True)
    razao_social = db.Column(db.String(128), unique=True)
    cep = db.Column(db.String(128))
    logradouro = db.Column(db.String(128))
    numero = db.Column(db.String(128))
    complemento = db.Column(db.String(128))
    bairro = db.Column(db.String(128))
    uf = db.Column(db.String(128))
    cidade = db.Column(db.String(128))
    tel_corporativo = db.Column(db.String(128), unique=True)
    tel_financeiro = db.Column(db.String(128), unique=True)
    tel_outro = db.Column(db.String(128), unique=True)
    email_corporativo = db.Column(db.String(128), unique=True)
    email_financeiro = db.Column(db.String(128), unique=True)
    email_outro = db.Column(db.String(128), unique=True)
    created_at = db.Column(
        db.DateTime, default=get_current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=get_current_time,
                           onupdate=get_current_time, nullable=False)


class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    preco = db.Column(db.Integer)

    operacao_id = db.Column(db.Integer, db.ForeignKey('operacoes.id'))
    operacao = db.relationship('Operacoes', backref='produtos')

    created_at = db.Column(
        db.DateTime, default=get_current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=get_current_time,
                           onupdate=get_current_time, nullable=False)


class AvisosSys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    content = db.Column(db.String(500))
    created_at = db.Column(
        db.DateTime, default=get_current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=get_current_time,
                           onupdate=get_current_time, nullable=False)


class RefreshTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    refresh_token = db.Column(db.String(1000), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(
        db.DateTime, default=get_current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=get_current_time,
                           onupdate=get_current_time, nullable=False)


class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    code = db.Column(db.String(5), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(
        db.DateTime, default=get_current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=get_current_time,
                           onupdate=get_current_time, nullable=False)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(5), nullable=False)
    users = db.relationship('User', backref='role', lazy=True)
    created_at = db.Column(
        db.DateTime, default=get_current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=get_current_time,
                           onupdate=get_current_time, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, ForeignKey('role.id'), nullable=False)
    created_at = db.Column(
        db.DateTime, default=get_current_time, nullable=False)
    updated_at = db.Column(db.DateTime, default=get_current_time,
                           onupdate=get_current_time, nullable=False)
