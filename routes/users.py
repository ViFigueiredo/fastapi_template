from configs.default import app, salt
from configs.db import get_db_connection
from routes.auth import teachers
from flask_jwt_extended import jwt_required
from flask import jsonify, request, Blueprint
from datetime import datetime, timezone
import hashlib
import binascii
import re

users_bp = Blueprint('users', __name__)
cursor = get_db_connection().cursor()


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


@app.route('/config/users/password-fresh', methods=['PUT'])
# @jwt_required()
# @teachers()
def password_clear():
    try:
        data = request.get_json()
        role_id = data.get('role_id')
        password_before_reset = 'password_null'

        password_after_reset = hashlib.scrypt(password_before_reset.encode(
        ), salt=salt, n=16384, r=8, p=1, maxmem=0, dklen=64)

        password_after_reset = binascii.hexlify(
            password_after_reset).decode()[:128]

        cursor.execute(
            "UPDATE [user] SET password = ? WHERE id = ?", (password_after_reset, role_id))
        cursor.commit()

        return jsonify({'msg': 'Senhas resetadas com sucesso.'}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/users/<int:user_id>', methods=['DELETE'])
# @jwt_required()
# @teachers()
def delete_user(user_id):
    try:
        cursor.execute("SELECT 1 FROM [user] WHERE id = ?", user_id)

        if cursor.fetchone() is None:
            return jsonify({'message': 'Não existe.'}), 400

        cursor.execute("DELETE FROM [user] WHERE id = ?", user_id)
        cursor.commit()
        return jsonify({'message': 'Deletado com sucesso.'}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/users/<int:user_id>', methods=['PUT'])
# @jwt_required()
# @teachers()
def update_user(user_id):
    try:
        data = request.get_json()
        new_name = data.get('name')
        new_email = data.get('email')
        new_password = data.get('password')
        new_role_id = data.get('role_id')
        now = datetime.now(timezone.utc)

        if new_password:
            # Gera o hash da nova senha fornecida usando scrypt e trunca para 128 caracteres
            new_password_hash = hashlib.scrypt(new_password.encode(
            ), salt=salt, n=16384, r=8, p=1, maxmem=0, dklen=64)
            new_password_hash = binascii.hexlify(
                new_password_hash).decode()[:128]

            cursor.execute(
                f"UPDATE [user] SET password = ?, updated_at = ? WHERE id = ?", (
                    new_password_hash, now, user_id)
            )

        if new_name:
            cursor.execute(
                f"UPDATE [user] SET name = ?, updated_at = ? WHERE id = ?", (
                    new_name, now, user_id)
            )

        if new_email:
            cursor.execute(
                f"UPDATE [user] SET email = ?, updated_at = ? WHERE id = ?", (
                    new_email, now, user_id)
            )

        if new_role_id:
            cursor.execute(
                "UPDATE [user] SET role_id = ?, updated_at = ? WHERE id = ?", (
                    new_role_id, now, user_id)
            )

        cursor.commit()

        return jsonify({'message': 'Atualizado com sucesso.'}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/users/<int:user_id>', methods=['GET'])
# @jwt_required()
# @teachers()
def get_user(user_id):
    try:
        cursor.execute("SELECT * FROM [user] WHERE id = ?", (user_id))
        row = cursor.fetchone()

        if row is None:
            return jsonify({'message': 'Não encontrado.'}), 404

        role = {
            'id': row.id,
            'name': row.name,
            'email': row.email,
            'role_id': row.role_id,
            'created_at': row.created_at,
            'updated_at': row.updated_at
        }

        return jsonify(role)

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/users', methods=['GET'])
# @jwt_required()
# @teachers()
def get_users():
    try:
        cursor.execute("SELECT * FROM [user]")
        users = []

        for row in cursor:
            users.append({
                'id': row.id,
                'name': row.name,
                'email': row.email,
                'role_id': row.role_id,
                'created_at': row.created_at,
                'updated_at': row.updated_at
            })

        return jsonify(users)
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/users', methods=['POST'])
# @jwt_required()
# @teachers()
def add_user():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        role_id = data.get('role_id')
        password = data.get('password')
        messages = []

        # Verifica se os campos obrigatórios estão presentes
        required_fields = ['name', 'email', 'password', 'role_id']
        for field in required_fields:
            if field not in data or not data[field]:
                messages.append(f'O campo {field} é obrigatório.')

        # Verifica o comprimento dos campos
        if len(name) > 128 or len(email) > 128 or len(password) > 128:
            messages.append(
                'O comprimento dos campos não pode exceder 128 caracteres.')

        # Verifica se o email é válido
        if not is_valid_email(email):
            messages.append('E-mail inválido.')

        # Verifica se o email já está cadastrado
        cursor.execute(
            "SELECT 1 FROM [user] WHERE email = ?", (email))
        if cursor.fetchone():
            messages.append('E-mail já cadastrado.')

        # Verifica se o nome já está cadastrado
        cursor.execute("SELECT 1 FROM [user] WHERE name = ?", (name))
        if cursor.fetchone():
            messages.append('Nome já cadastrado.')

        if len(messages) > 0:
            return jsonify({'message': messages})

        now = datetime.now(timezone.utc)
        password_hash = hashlib.scrypt(password.encode(
        ), salt=salt, n=16384, r=8, p=1, maxmem=0, dklen=64)
        password_hash = binascii.hexlify(password_hash).decode()[:128]
        password = password_hash

        cursor.execute(
            "INSERT INTO [user] (name, email, password, role_id, created_at, updated_at) VALUES (?,?,?,?,?,?)",
            (name, email,
             password, role_id, now, now)
        )
        cursor.commit()

        return jsonify({'message': 'Adicionado com sucesso.'}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500
