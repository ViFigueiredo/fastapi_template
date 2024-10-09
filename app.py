from configs.default import app
from flask_cors import CORS
from routes.users import users_bp
from routes.roles import roles_bp
from routes.auth import auth_bp
from routes.news import avisos_bp
from routes.relatorios import relatorios_bp
from routes.clientes import clientes_bp
from routes.produtos import produtos_bp

# Habilita o CORS
CORS(app, origins=[
    "http://127.0.0.1:5173",
    "http://localhost:5173",
])

# Configuração de cabeçalhos de segurança
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['X_CONTENT_TYPE_OPTIONS'] = 'nosniff'
app.config['X_FRAME_OPTIONS'] = 'SAMEORIGIN'
app.config['STRICT_TRANSPORT_SECURITY'] = 'max-age=31536000; includeSubDomains'

app.register_blueprint(users_bp)
app.register_blueprint(roles_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(avisos_bp)
app.register_blueprint(relatorios_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(produtos_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
