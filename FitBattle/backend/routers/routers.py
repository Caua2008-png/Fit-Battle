from flask import Blueprint, jsonify

from controllers.feed_controller import FeedController
from controllers.postagem_controller import PostagemController
from controllers.treino_controller import TreinoController
from controllers.usuario_controller import UsuarioController

Fitbattle_bp = Blueprint("fitbattle", __name__, url_prefix="/api")

# Autenticação
Fitbattle_bp.add_url_rule("/cadastro", endpoint="cadastro", view_func=UsuarioController.cadastrar, methods=["POST"])
Fitbattle_bp.add_url_rule("/login", endpoint="login", view_func=UsuarioController.login, methods=["POST"])
Fitbattle_bp.add_url_rule("/logout", endpoint="logout", view_func=UsuarioController.logout, methods=["POST"])
Fitbattle_bp.add_url_rule("/sessao", endpoint="sessao", view_func=UsuarioController.sessao, methods=["GET"])

# Perfil
Fitbattle_bp.add_url_rule("/perfil", endpoint="ver_perfil", view_func=UsuarioController.perfil, methods=["GET"])
Fitbattle_bp.add_url_rule(
    "/perfil", endpoint="atualizar_perfil", view_func=UsuarioController.atualizar_perfil, methods=["PUT"]
)
Fitbattle_bp.add_url_rule(
    "/perfil/avatar", endpoint="enviar_avatar", view_func=UsuarioController.enviar_avatar, methods=["POST"]
)
Fitbattle_bp.add_url_rule(
    "/perfil/configuracoes",
    endpoint="atualizar_configuracoes",
    view_func=UsuarioController.atualizar_configuracoes,
    methods=["PUT"],
)

# Ranking
Fitbattle_bp.add_url_rule("/ranking", endpoint="ranking", view_func=UsuarioController.ranking, methods=["GET"])

# Feed / treinos / postagens
Fitbattle_bp.add_url_rule("/feed", endpoint="feed", view_func=FeedController.listar, methods=["GET"])
Fitbattle_bp.add_url_rule(
    "/treinos", endpoint="criar_treino", view_func=TreinoController.criar, methods=["POST"]
)
Fitbattle_bp.add_url_rule(
    "/postagens", endpoint="criar_postagem", view_func=PostagemController.criar, methods=["POST"]
)


@Fitbattle_bp.route("/cards/<string:tipo>/<int:item_id>", methods=["DELETE"])
def excluir_card(tipo, item_id):
    if tipo == "treino":
        return TreinoController.excluir(item_id)
    if tipo == "postagem":
        return PostagemController.excluir(item_id)
    return jsonify({"erro": "Tipo de card inválido."}), 400
