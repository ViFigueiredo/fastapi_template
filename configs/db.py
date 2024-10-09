from dotenv import load_dotenv
import pyodbc
import os

load_dotenv()  # Carregar variáveis de ambiente

# Configuração da conexão
conn_str = (
    'DRIVER={' + os.getenv('DB_DRIVER') + '};'
    'SERVER=' + os.getenv('DB_SERVER') + ';'
    'DATABASE=' + os.getenv('DB_NAME') + ';'
    'UID=' + os.getenv('DB_USER') + ';'
    'PWD=' + os.getenv('DB_PASSWORD') + ';'
    'Encrypt=no'
)

def get_db_connection():
    try:
        conn = pyodbc.connect(conn_str, timeout=10)
        return conn
    except pyodbc.InterfaceError as ie:
        raise Exception(f"Erro de interface: {ie}")
    except pyodbc.DatabaseError as de:
        raise Exception(f"Erro de banco de dados: {de}")
    except Exception as e:
        raise Exception(f"Erro desconhecido: {e}")
