from configs.default import app
from configs.db import get_db_connection
from routes.auth import teachers
from flask_jwt_extended import jwt_required
from flask import jsonify, request, Blueprint
from datetime import datetime, timezone

produtos_bp = Blueprint('produtos', __name__)
cursor = get_db_connection().cursor()


@app.route('/crm/produtos/<int:produto_id>', methods=['DELETE'])
# @jwt_required()
# @teachers()
def delete_produto(produto_id):
    try:
        cursor.execute("SELECT 1 FROM [produtos] WHERE id = ?", produto_id)

        if cursor.fetchone() is None:
            return jsonify({'message': 'Não existe.'}), 400

        cursor.execute(f"DELETE FROM [produtos] WHERE id = ?", produto_id)
        cursor.commit()
        return jsonify({'message': 'Deletado com sucesso.'}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/crm/produtos/<int:produto_id>', methods=['PUT'])
# @jwt_required()
# @teachers()
def update_produto(produto_id):
    try:
        data = request.get_json()
        new_name = data.get('name')
        new_preco = data.get('preco')
        new_operation_id = data.get('operacao_id')
        now = datetime.now(timezone.utc)

        cursor.execute("SELECT 1 FROM [produtos] WHERE id = ?", produto_id)

        if cursor.fetchone() is None:
            return jsonify({'message': 'Não existe.'}), 400

        if new_name:
            cursor.execute(
                "UPDATE [produtos] SET name = ? WHERE id = ?",
                (new_name, produto_id)
            )

        if new_preco:
            cursor.execute(
                "UPDATE [produtos] SET preco = ? WHERE id = ?",
                (new_preco, produto_id)
            )

        if new_operation_id:
            cursor.execute(
                "UPDATE [produtos] SET operacao_id = ? WHERE id = ?",
                (new_operation_id, produto_id)
            )

        cursor.execute(
            "UPDATE [produtos] SET updated_at = ? WHERE id = ?",
            (now, produto_id)
        )

        cursor.commit()
        return jsonify({'message': 'Atualizado com sucesso.'}), 200

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/crm/produtos/<int:produto_id>', methods=['GET'])
# @jwt_required()
# @teachers()
def get_produto(produto_id):
    try:
        cursor.execute("SELECT * FROM [produtos] WHERE id = ?", (produto_id))
        row = cursor.fetchone()

        if row is None:
            return jsonify({'message': 'Não encontrado.'}), 404

        produto = {
            'id': row.id,
            'name': row.name,
            'preco': row.preco,
            'operacao_id': row.operacao_id,
            'created_at': row.created_at,
            'updated_at': row.updated_at,
            'created_at': row.created_at,
            'updated_at': row.updated_at

        }

        return jsonify(produto)

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/crm/produtos', methods=['GET'])
# @jwt_required()
# @teachers()
def get_produtos():
    try:
        cursor.execute("SELECT * FROM [produtos]")
        crmProdutos = []

        for row in cursor:
            crmProdutos.append({
                "id": row.id,
                "name": row.name,
                "preco": row.preco,
                "operacao_id": row.operacao_id,
                'created_at': row.created_at,
                'updated_at': row.updated_at

            })

        return jsonify(crmProdutos)
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/crm/produtos', methods=['POST'])
# @jwt_required()
# @teachers()
def add_produto():
    try:
        data = request.get_json()
        name = data.get('name')
        preco = data.get('preco')
        operacao_id = data.get('operacao_id')
        now = datetime.now(timezone.utc)

        cursor.execute(
            "INSERT INTO [produtos] (name, preco, operacao_id, created_at, updated_at) VALUES (?,?,?,?,?)",
            (name, preco, operacao_id, now, now)
        )

        cursor.commit()

        return jsonify({'message': 'Adicionado com sucesso.'}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500
