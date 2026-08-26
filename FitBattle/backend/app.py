import os

from flask import Flask, jsonify, send_from_directory
from flask_login import LoginManager

from database import db
from routers.routers import Fitbattle_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "fitbattle.db")
app.config["SECRET_KEY"] = os.environ.get("FITBATTLE_SECRET_KEY", "chave-de-desenvolvimento-fitbattle")

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def carregar_usuario(usuario_id):
    from repositories.usuario_repository import UsuarioRepository

    return UsuarioRepository.buscar_por_id(int(usuario_id))


@login_manager.unauthorized_handler
def acesso_nao_autorizado():
    return jsonify({"erro": "Autenticação necessária."}), 401


app.register_blueprint(Fitbattle_bp)

with app.app_context():
    from models.postagem import Postagem  # noqa: F401
    from models.treino import Treino  # noqa: F401
    from models.usuario import Usuario  # noqa: F401

    db.create_all()


@app.route("/")
def pagina_landing():
    return send_from_directory(FRONTEND_DIR, "landing.html")


@app.route("/cadastro")
def pagina_cadastro():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/login")
def pagina_login():
    return send_from_directory(FRONTEND_DIR, "login.html")


@app.route("/app")
def pagina_app():
    return send_from_directory(FRONTEND_DIR, "app.html")


@app.route("/<path:caminho_arquivo>")
def arquivos_frontend(caminho_arquivo):
    return send_from_directory(FRONTEND_DIR, caminho_arquivo)


if __name__ == "__main__":
    app.run(debug=True)
