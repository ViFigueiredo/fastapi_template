from configs.default import app
from configs.db import get_db_connection
from routes.auth import role_required, teachers
from flask_jwt_extended import jwt_required
from flask import jsonify, request, Blueprint
from datetime import datetime, timezone

relatorios_bp = Blueprint('relatorios', __name__)
cursor = get_db_connection().cursor()


@app.route('/config/relatorios/<int:relatorios_id>', methods=['DELETE'])
# @jwt_required()
# @teachers()
def delete_relatorio(relatorios_id):
    try:
        cursor.execute(f"DELETE FROM [relatorios] WHERE id = {relatorios_id}")
        cursor.commit()
        return jsonify({'message': 'Deletado com sucesso.'}), 200
    
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/relatorios/<int:relatorio_id>', methods=['PUT'])
# @jwt_required()
# @teachers()
def update_relatorio(relatorio_id):
    try:
        data = request.get_json()
        new_name = data.get('name')
        new_user_id = data.get('user_id')
        new_url = data.get('url')
        now = datetime.now(timezone.utc)

        if new_name:
            cursor.execute(
                "UPDATE [relatorios] SET name = ? WHERE id = ?", (
                    new_name, relatorio_id)
            )

        if new_user_id:
            cursor.execute(
                "UPDATE [relatorios] SET user_id = ? WHERE id = ?", (
                    new_user_id, relatorio_id)
            )

        if new_url:
            cursor.execute(
                "UPDATE [relatorios] SET url = ? WHERE id = ?", (
                    new_url, relatorio_id)
            )

        cursor.execute(
            "UPDATE [relatorios] SET updated_at = ? WHERE id = ?", (
                now, relatorio_id)
        )

        cursor.commit()
        return jsonify({'message': 'Atualizado com sucesso.'}), 200

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/relatorios/<int:relatorio_id>', methods=['GET'])
# @jwt_required()
# @teachers()
def get_relatorio(relatorio_id):
    try:
        cursor.execute(
            f"SELECT * FROM [relatorios] WHERE id = ?", (relatorio_id))
        row = cursor.fetchone()

        if row is None:
            return jsonify({'message': 'Não encontrado.'}), 404

        relatorio = {
            'id': row.id,
            'name': row.name,
            'user_id': row.user_id,
            'url': row.url,
            'created_at': row.created_at,
            'updated_at': row.updated_at
        }

        return jsonify(relatorio)

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/relatorios', methods=['GET'])
# @jwt_required()
# @teachers()
def get_relatorios():
    try:
        cursor.execute("SELECT * FROM [relatorios]")
        relatorios = []

        for row in cursor:
            relatorios.append({
                'id': row.id,
                'name': row.name,
                'user_id': row.user_id,
                'url': row.url,
                'created_at': row.created_at,
                'updated_at': row.updated_at
            })

        return jsonify(relatorios)

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/relatorios', methods=['POST'])
# @jwt_required()
# @teachers()
def add_relatorio():
    try:
        data = request.get_json()
        name = data.get('name')
        user_id = data.get('user_id')
        url = data.get('url')
        now = datetime.now(timezone.utc)

        cursor.execute(
            "INSERT INTO [relatorios] (name, user_id, url, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (name, user_id, url, now, now)
        )

        cursor.commit()
        return jsonify({'message': 'Adicionado com sucesso.'}), 200

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500
