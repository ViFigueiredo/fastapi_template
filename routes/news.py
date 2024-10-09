from configs.default import app
from configs.db import get_db_connection
from routes.auth import teachers
from flask_jwt_extended import jwt_required
from flask import jsonify, request, Blueprint
from datetime import datetime, timezone

avisos_bp = Blueprint('avisos', __name__)
cursor = get_db_connection().cursor()


@app.route('/config/news/<int:aviso_id>', methods=['DELETE'])
# @jwt_required()
# @teachers()
def delete_aviso(aviso_id):
    try:
        cursor.execute("SELECT 1 FROM [avisos_sys] WHERE id = ?", aviso_id)

        if cursor.fetchone() is None:
            return jsonify({'message': 'Não existe.'}), 400

        cursor.execute(f"DELETE FROM [avisos_sys] WHERE id = ?", aviso_id)
        cursor.commit()
        return jsonify({'message': 'Deletado com sucesso.'}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/news/<int:aviso_id>', methods=['PUT'])
# @jwt_required()
# @teachers()
def update_aviso(aviso_id):
    try:
        data = request.get_json()
        new_name = data.get('name')
        new_content = data.get('content')
        now = datetime.now(timezone.utc)

        if new_name:
            cursor.execute(
                "UPDATE [avisos_sys] SET name = ? WHERE id = ?", (
                    new_name, aviso_id)
            )

        if new_content:
            cursor.execute(
                "UPDATE [avisos_sys] SET content = ? WHERE id = ?", (
                    new_content, aviso_id)
            )

        cursor.execute(
            "UPDATE [avisos_sys] SET updated_at = ? WHERE id = ?", (
                now, aviso_id)
        )

        cursor.commit()
        return jsonify({'message': 'Atualizado com sucesso.'}), 200

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/news/<int:aviso_id>', methods=['GET'])
# @jwt_required()
# @teachers()
def get_aviso(aviso_id):
    try:
        cursor.execute("SELECT * FROM [avisos_sys] WHERE id = ?", (aviso_id))
        row = cursor.fetchone()

        if row is None:
            return jsonify({'message': 'Não encontrado.'}), 404

        aviso = {
            'id': row.id,
            'name': row.name,
            'content': row.content,
            'created_at': row.created_at,
            'updated_at': row.updated_at
        }

        return jsonify(aviso)

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/news', methods=['GET'])
# @jwt_required()
# @teachers()
def get_avisos():
    try:
        cursor.execute("SELECT * FROM [avisos_sys]")
        avisos = []

        for row in cursor:
            avisos.append({
                'id': row.id,
                'name': row.name,
                'content': row.content,
                'created_at': row.created_at,
                'updated_at': row.updated_at
            })

        return jsonify(avisos)

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/config/news', methods=['POST'])
# @jwt_required()
# @teachers()
def add_aviso():
    try:
        data = request.get_json()
        name = data.get('name')
        content = data.get('content')
        now = datetime.now(timezone.utc)

        cursor.execute(
            "INSERT INTO [avisos_sys] (name, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (name, content, now, now)
        )

        cursor.commit()
        return jsonify({'message': 'Adicionado com sucesso.'}), 200

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500
