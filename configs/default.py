from flask import Flask
from flask_jwt_extended import JWTManager
import os
import pandas as pd

# Diretório onde os arquivos serão salvos
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


salt = str(os.getenv('SALT')).encode()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JWT_SECRET_KEY'] = str(os.getenv('JWT_SECRET'))
jwt = JWTManager(app)
