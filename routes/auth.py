from configs.default import app, salt
from configs.db import get_db_connection
from configs.smtp import enviar_email
from functools import wraps
from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from jwt.exceptions import ExpiredSignatureError
from datetime import datetime, timedelta, timezone
import hashlib
import binascii
import random
import jwt
import secrets
import os

auth_bp = Blueprint('auth', __name__)
cursor = get_db_connection().cursor()
access_expires_in_seconds = 28800
refresh_expires_in_seconds = datetime.now() + timedelta(seconds=24*60*60)


@app.errorhandler(ExpiredSignatureError)
def handle_expired_token(e):
    return jsonify({"message": "Sessão expirada."}), 401


def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            cursor.execute(
                "SELECT * FROM [user] WHERE email = ?", (current_user))
            user = cursor.fetchone()
            if user.role not in roles:
                return jsonify({"msg": "Permission denied."}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def teachers():
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            email = get_jwt_identity()
            expire_datetime = datetime.now(
                timezone.utc) + timedelta(seconds=access_expires_in_seconds)

            if expire_datetime > datetime.now(timezone.utc):
                return f(*args, **kwargs)
            else:
                return jsonify({"message": "Token expirado"}), 401
        return decorator
    return wrapper


def generate_access_token(email):
    expires_in_access = timedelta(seconds=access_expires_in_seconds)
    access_token = create_access_token(
        identity=email, expires_delta=expires_in_access)
    return access_token


def generate_refresh_token():
    payload = {"refresh_token": secrets.token_urlsafe(
        32), "exp": refresh_expires_in_seconds}
    refresh_token = jwt.encode(payload, str(
        os.getenv('JWT_SECRET')), algorithm="HS256")
    return refresh_token


def gerar_otp():
    return str(random.randint(1000, 9999))  # Gera um número de 4 dígitos


@app.route('/auth/otp', methods=['POST'])
def send_otp():
    try:
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400

        data = request.get_json()
        email = data.get('email')
        now = datetime.now(timezone.utc)
        active = False
        messages = []

        if not email:
            messages.append('E-mail inválido.')

        cursor.execute("SELECT * FROM [user] WHERE email = ?", (email))
        user = cursor.fetchone()

        if user is None:
            messages.append('Usuário não cadastrado.')

        if len(messages) > 0:
            return jsonify({"status": False, "message": messages}), 200

        otp = gerar_otp()
        enviar_email(email, otp)

        cursor.execute(
            "INSERT INTO [otp] (user_id, code, active, created_at, updated_at) VALUES (?,?,?,?,?)", (
                user.id, otp, active, now, now)
        )
        cursor.commit()

        return jsonify({"status": True, "message": "Enviado com sucesso."}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/auth/otp/confirm', methods=['POST'])
def confirm_otp():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')
        messages = []

        if not email:
            messages.append('E-mail inválido.')

        cursor.execute("SELECT * FROM [user] WHERE email = ?", (email))
        user = cursor.fetchone()

        if user is None:
            messages.append('Usuário não cadastrado.')

        else:
            cursor.execute("SELECT * FROM [otp] WHERE code = ?", (otp))
            otp_code = cursor.fetchone()

            if otp_code is None:
                messages.append('Código inválido.')

            else:
                if otp_code.active is True:
                    messages.append('Código já utilizado.')

            if len(messages) > 0:
                return jsonify({"status": False, "message": messages}), 200

            cursor.execute("UPDATE [otp] SET active = ? WHERE id = ?", (True, otp_code.id)
                           ).commit()

            return jsonify({"status": True, "message": "Salvo com sucesso."}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/auth/otp/reset', methods=['PUT'])
def reset_password():
    try:
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        errors = []

        if not email:
            errors.append('E-mail inválido.')

        cursor.execute("SELECT * FROM [user] WHERE email = ?", (email))
        user = cursor.fetchone()

        if user is None:
            errors.append('Usuário não cadastrado.')

        else:
            if len(errors) > 0:
                return jsonify({"status": False, "message": errors}), 200

            # Gera o hash da nova senha fornecida usando scrypt e trunca para 128 caracteres
            new_password_hash = hashlib.scrypt(password.encode(
            ), salt=salt, n=16384, r=8, p=1, maxmem=0, dklen=64)
            new_password_hash = binascii.hexlify(
                new_password_hash).decode()[:128]

            cursor.execute(
                "UPDATE [user] SET password = ? WHERE id = ?", (
                    new_password_hash, user.id)
            ).commit()

            return jsonify({"status": True, "message": "Salvo com sucesso."}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        messages = []

        if not email:
            messages.append('E-mail inválido.')
        if not password:
            messages.append('Senha inválida.')

        cursor.execute(f"SELECT * FROM [user] WHERE email = ?", (email))
        user = cursor.fetchone()

        if user is None:
            messages.append('Usuário não cadastrado.')
        else:
            if hasattr(user, 'id'):
                userData = {
                    "id": user.id,
                    "username": user.name,
                    "email": user.email,
                    "role_id": user.role_id,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at
                }
            else:
                messages.append('Atributo "id" não encontrado no usuário.')

        if hasattr(user, 'password'):
            password_hash = hashlib.scrypt(
                password.encode(), salt=salt, n=16384, r=8, p=1, maxmem=0, dklen=64)
            password_hash = binascii.hexlify(password_hash).decode()[:128]

            if user.password != password_hash:
                messages.append('Senha incorreta.')

        access_token = str(generate_access_token(email))

        if len(messages) > 0:
            return jsonify({"status": False, "message": messages}), 200
        return jsonify({"status": True, "access_token": access_token, "user": userData, "userID": user.id}), 200

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/refresh', methods=['PUT'])
def refresh_token():
    try:
        email = request.json.get('email')
        refresh_token = request.json.get('refresh_token')
        cursor.execute("SELECT * FROM [user] WHERE email = ?", (email))
        user = cursor.fetchone()

        access_token = str(generate_access_token(email))
        refresh_token = str(generate_refresh_token())

        if user is not None:
            cursor.execute(
                "UPDATE [user] SET refresh_token = ? WHERE email = ?", (
                    refresh_token, email)
            )

            cursor.commit()

        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500
