from configs.default import app
from configs.db import get_db_connection
from routes.auth import teachers
from flask_jwt_extended import jwt_required
from flask import jsonify, request, Blueprint
from datetime import datetime, timezone
import re

clientes_bp = Blueprint('clientes', __name__)
cursor = get_db_connection().cursor()


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


@app.route('/crm/clientes/<int:cliente_id>', methods=['DELETE'])
# @jwt_required()
# @teachers()
def delete_cliente(cliente_id):
    try:
        cursor.execute("SELECT 1 FROM [clientes] WHERE id = ?", (cliente_id))

        if cursor.fetchone() is None:
            return jsonify({'message': 'Não existe.'}), 400

        cursor.execute(f"DELETE FROM [clientes] WHERE id = ?", (cliente_id))
        cursor.commit()
        return jsonify({'message': 'Deletado com sucesso.'}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/crm/clientes/<int:cliente_id>', methods=['PUT'])
# @jwt_required()
# @teachers()
def update_cliente(cliente_id):
    try:
        data = request.get_json()
        new_cpf_cnpj = data.get('cpf_cnpj')
        new_razao_social = data.get('razao_social')
        new_cep = data.get('cep')
        new_logradouro = data.get('logradouro')
        new_numero = data.get('numero')
        new_complemento = data.get('complemento')
        new_bairro = data.get('bairro')
        new_uf = data.get('uf')
        new_cidade = data.get('cidade')
        new_tel_corporativo = data.get('tel_corporativo')
        new_tel_financeiro = data.get('tel_financeiro')
        new_tel_outro = data.get('tel_outro')
        new_email_corporativo = data.get('email_corporativo')
        new_email_financeiro = data.get('email_financeiro')
        new_email_outro = data.get('email_outro')
        now = datetime.now(timezone.utc)
        messages = []

        # Verifica se o email é válido
        if not is_valid_email(new_email_corporativo):
            messages.append('E-mail "corporativo" inválido.')

        if not is_valid_email(new_email_financeiro):
            messages.append('E-mail "financeiro" inválido.')

        if not is_valid_email(new_email_outro):
            messages.append('E-mail "outro" inválido.')


        if new_cpf_cnpj:
            cursor.execute(
                "UPDATE [clientes] SET cpf_cnpj = ? WHERE id = ?", (new_cpf_cnpj, cliente_id))

        if new_razao_social:
            cursor.execute(
                "UPDATE [clientes] SET razao_social = ? WHERE id = ?", (new_razao_social, cliente_id))

        if new_cep:
            cursor.execute(
                "UPDATE [clientes] SET cep = ? WHERE id = ?", (new_cep, cliente_id))

        if new_logradouro:
            cursor.execute(
                "UPDATE [clientes] SET logradouro = ? WHERE id = ?", (new_logradouro, cliente_id))

        if new_numero:
            cursor.execute(
                "UPDATE [clientes] SET numero = ? WHERE id = ?", (new_numero, cliente_id))

        if new_complemento:
            cursor.execute(
                "UPDATE [clientes] SET complemento = ? WHERE id = ?", (new_complemento, cliente_id))

        if new_bairro:
            cursor.execute(
                "UPDATE [clientes] SET bairro = ? WHERE id = ?", (new_bairro, cliente_id))

        if new_uf:
            cursor.execute(
                "UPDATE [clientes] SET uf = ? WHERE id = ?", (new_uf, cliente_id))

        if new_cidade:
            cursor.execute(
                "UPDATE [clientes] SET cidade = ? WHERE id = ?", (new_cidade, cliente_id))

        if new_tel_corporativo:
            cursor.execute(
                "UPDATE [clientes] SET tel_corporativo = ? WHERE id = ?", (new_tel_corporativo, cliente_id))

        if new_tel_financeiro:
            cursor.execute(
                "UPDATE [clientes] SET tel_financeiro = ? WHERE id = ?", (new_tel_financeiro, cliente_id))

        if new_tel_outro:
            cursor.execute(
                "UPDATE [clientes] SET tel_outro = ? WHERE id = ?", (new_tel_outro, cliente_id))

        if new_email_corporativo:
            cursor.execute(
                "UPDATE [clientes] SET email_corporativo = ? WHERE id = ?", (new_email_corporativo, cliente_id))

        if new_email_financeiro:
            cursor.execute(
                "UPDATE [clientes] SET email_financeiro = ? WHERE id = ?", (new_email_financeiro, cliente_id))

        if new_email_outro:
            cursor.execute(
                "UPDATE [clientes] SET email_outro = ? WHERE id = ?", (new_email_outro, cliente_id))

        cursor.execute(
            "UPDATE [clientes] SET updated_at = ? WHERE id = ?", (now, cliente_id))

        cursor.commit()

        return jsonify({'message': 'Atualizado com sucesso.'}), 200
    except Exception as e:
        cursor.rollback()
        return "Erro ao realizar a requisição: {e}"


@app.route('/crm/clientes/<int:cliente_id>', methods=['GET'])
# @jwt_required()
# @teachers()
def get_cliente(cliente_id):
    try:
        cursor.execute(f"SELECT * FROM [clientes] WHERE id = ?", (cliente_id))
        row = cursor.fetchone()

        if row is None:
            return jsonify({'message': 'Não encontrado.'}), 404

        cliente = {
            "id": row.id,
            "cpf_cnpj": row.cpf_cnpj,
            "razao_social": row.razao_social,
            "cep": row.cep,
            "logradouro": row.logradouro,
            "numero": row.numero,
            "complemento": row.complemento,
            "bairro": row.bairro,
            "u": row.uf,
            "cidade": row.cidade,
            "tel_corporativo": row.tel_corporativo,
            "tel_financeiro": row.tel_financeiro,
            "tel_outro": row.tel_outro,
            "email_corporativo": row.email_corporativo,
            "email_financeiro": row.email_financeiro,
            "email_outro": row.email_outro
        }

        return jsonify(cliente)

    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/crm/clientes', methods=['GET'])
# @jwt_required()
# @teachers()
def get_clientes():
    try:
        cursor.execute("SELECT * FROM [clientes]")
        clientes = []

        for row in cursor:
            clientes.append({
                "id": row.id,
                "cpf_cnpj": row.cpf_cnpj,
                "razao_social": row.razao_social,
                "cep": row.cep,
                "logradouro": row.logradouro,
                "numero": row.numero,
                "complemento": row.complemento,
                "bairro": row.bairro,
                "u": row.uf,
                "cidade": row.cidade,
                "tel_corporativo": row.tel_corporativo,
                "tel_financeiro": row.tel_financeiro,
                "tel_outro": row.tel_outro,
                "email_corporativo": row.email_corporativo,
                "email_financeiro": row.email_financeiro,
                "email_outro": row.email_outro
            })

        return jsonify(clientes)
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/crm/clientes', methods=['POST'])
# @jwt_required()
# @teachers()
def add_clientes():
    try:
        data = request.get_json()
        cpf_cnpj = data.get('cpf_cnpj')
        razao_social = data.get('razao_social')
        cep = data.get('cep')
        logradouro = data.get('logradouro')
        numero = data.get('numero')
        complemento = data.get('complemento')
        bairro = data.get('bairro')
        uf = data.get('uf')
        cidade = data.get('cidade')
        tel_corporativo = data.get('tel_corporativo')
        tel_financeiro = data.get('tel_financeiro')
        tel_outro = data.get('tel_outro')
        email_corporativo = data.get('email_corporativo')
        email_financeiro = data.get('email_financeiro')
        email_outro = data.get('email_outro')
        now = datetime.now(timezone.utc)
        messages = []

        # Verifique se o cpf_cnpj já existe
        cursor.execute(
            "SELECT COUNT(*) FROM clientes WHERE cpf_cnpj = ?", (cpf_cnpj,))
        count = cursor.fetchone()[0]
        if count > 0:
            messages.append('CPF/CNPJ já existe na base de dados.')

        # Verifique se o razao_social já existe
        cursor.execute(
            "SELECT COUNT(*) FROM clientes WHERE razao_social = ?", (razao_social,))

        count = cursor.fetchone()[0]

        if count > 0:
            messages.append('Razão Social já existe na base de dados.')

        # Verifique se o tel_corporativo já existe
        cursor.execute(
            "SELECT COUNT(*) FROM clientes WHERE tel_corporativo = ?", (tel_corporativo,))

        count = cursor.fetchone()[0]

        if count > 0:
            messages.append('Telefone corporativo já existe na base de dados.')

        # Verifique se o tel_financeiro já existe
        cursor.execute(
            "SELECT COUNT(*) FROM clientes WHERE tel_financeiro = ?", (tel_financeiro,))

        count = cursor.fetchone()[0]

        if count > 0:
            messages.append('Telefone financeiro já existe na base de dados.')

        # Verifique se o tel_outro já existe
        cursor.execute(
            "SELECT COUNT(*) FROM clientes WHERE tel_outro = ?", (tel_outro,))

        count = cursor.fetchone()[0]

        if count > 0:
            messages.append('Telefone já existe na base de dados.')

        # Verifica se o email é válido
        if not is_valid_email(email_corporativo):
            messages.append('E-mail "corporativo" inválido.')

        if not is_valid_email(email_financeiro):
            messages.append('E-mail "financeiro" inválido.')

        if not is_valid_email(email_outro):
            messages.append('E-mail "outro" inválido.')


        # Verifique se o email_corporativo já existe
        cursor.execute(
            "SELECT COUNT(*) FROM clientes WHERE email_corporativo = ?", (email_corporativo,))

        count = cursor.fetchone()[0]

        if count > 0:
            messages.append('E-mail corporativo já existe na base de dados.')

        # Verifique se o email_financeiro já existe
        cursor.execute(
            "SELECT COUNT(*) FROM clientes WHERE email_financeiro = ?", (email_financeiro,))

        count = cursor.fetchone()[0]

        if count > 0:
            messages.append('E-mail financeiro já existe na base de dados.')

        # Verifique se o email_outro já existe
        cursor.execute(
            "SELECT COUNT(*) FROM clientes WHERE email_outro = ?", (email_outro,))

        count = cursor.fetchone()[0]

        if count > 0:
            messages.append('E-mail já existe na base de dados.')

        if len(messages) > 0:
            return jsonify({'message': messages}), 400

        cursor.execute(
            "INSERT INTO [clientes] (cpf_cnpj, razao_social, cep, logradouro, numero, complemento, bairro, uf, cidade, tel_corporativo, tel_financeiro, tel_outro, email_corporativo, email_financeiro, email_outro, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (cpf_cnpj, razao_social, cep, logradouro, numero, complemento, bairro, uf, cidade,
             tel_corporativo, tel_financeiro, tel_outro, email_corporativo, email_financeiro, email_outro, now, now)
        )

        cursor.commit()

        return jsonify({'message': 'Adicionado com sucesso.'}), 200
    except Exception as e:
        cursor.rollback()
        return jsonify({'message': str(e)}), 500
