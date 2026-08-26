from flask import jsonify, request
from flask_login import current_user, login_required

from services.treino_service import TreinoService


class TreinoController:
    @staticmethod
    @login_required
    def criar():
        dados = request.get_json(silent=True)
        if not dados:
            return jsonify({"erro": "JSON inválido"}), 400
        try:
            TreinoService.cadastrar(current_user, dados)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        return jsonify({"mensagem": "Treino publicado!"}), 201

    @staticmethod
    @login_required
    def excluir(treino_id):
        try:
            TreinoService.excluir(current_user, treino_id)
        except PermissionError as erro:
            return jsonify({"erro": str(erro)}), 403
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404
        return jsonify({"mensagem": "Treino excluído."})
