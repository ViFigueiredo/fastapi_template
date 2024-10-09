from configs.default import app
from configs.db import get_db_connection
from routes.auth import teachers
from flask_jwt_extended import jwt_required
from flask import jsonify, request, Blueprint
from datetime import datetime, timezone

roles_bp = Blueprint('roles', __name__)
cursor = get_db_connection().cursor()


@app.route('/config/roles/<int:role_id>', methods=['DELETE'])
# @jwt_required()
# @teachers()
def delete_role(role_id):
    try:
        cursor.execute("SELECT 1 FROM [role] WHERE id = ?", role_id)

        if cursor.fetchone() is None:
            return jsonify({'message': 'Não existe.'}), 400

        cursor.execute(f"DELETE FROM [role] WHERE id = ?", role_id)
        cursor.commit()
        return jsonify({'message': 'Deletado com sucesso.'}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/roles/<int:role_id>', methods=['PUT'])
# @jwt_required()
# @teachers()
def update_role(role_id):
    try:
        data = request.get_json()
        new_name = data.get('name')
        new_value = data.get('value')
        now = datetime.now(timezone.utc)

        cursor.execute("SELECT 1 FROM [role] WHERE id = ?", role_id)

        if cursor.fetchone() is None:
            return jsonify({'message': 'Não existe.'}), 400

        if new_name:
            cursor.execute(
                "UPDATE [role] SET name = ? WHERE id = ?",
                (new_name, role_id)
            )

        if new_value:
            cursor.execute(
                "UPDATE [role] SET value = ? WHERE id = ?",
                (new_value, role_id)
            )

        cursor.execute(
            "UPDATE [role] SET updated_at = ? WHERE id = ?",
            (now, role_id)
        )

        cursor.commit()
        return jsonify({'message': 'Atualizado com sucesso.'}), 200

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/roles/<int:role_id>', methods=['GET'])
# @jwt_required()
# @teachers()
def get_role(role_id):
    try:
        cursor.execute(f"SELECT * FROM [role] WHERE id = ?", (role_id))
        row = cursor.fetchone()

        if row is None:
            return jsonify({'message': 'Não encontrado.'}), 404

        role = {
            'id': row.id,
            'name': row.name,
            'value': row.value,
            'created_at': row.created_at,
            'updated_at': row.updated_at
        }

        return jsonify(role)

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/roles', methods=['GET'])
# @jwt_required()
# @teachers()
def get_roles():
    try:
        cursor.execute("SELECT * FROM [role]")
        roles = []

        for row in cursor:
            roles.append({
                'id': row.id,
                'name': row.name,
                'value': row.value,
                'created_at': row.created_at,
                'updated_at': row.updated_at

            })

        return jsonify(roles)

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/roles', methods=['POST'])
# @jwt_required()
# @teachers()
def add_role():
    try:
        data = request.get_json()
        name = data.get('name')
        value = data.get('value')
        now = datetime.now(timezone.utc)
        messages = []

        cursor.execute("SELECT 1 FROM [role] WHERE name = ?", (name))
        if cursor.fetchone():
            messages.append('Já cadastrado.')

        if len(name) > 50:
            messages.append('Nome maior que 50 caracteres.')

        if len(messages) > 0:
            return jsonify({'message': messages}), 400

        cursor.execute(
            "INSERT INTO [role] (name, value, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (name, value, now, now)
        )

        cursor.commit()
        return jsonify({'message': 'Adicionado com sucesso.'}), 200

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500
