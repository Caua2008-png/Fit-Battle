import os

from flask import current_app, jsonify, request
from flask_login import current_user, login_required

from services.postagem_service import PostagemService


class PostagemController:
    @staticmethod
    @login_required
    def criar():
        texto = request.form.get("texto")
        arquivo_foto = request.files.get("foto")
        pasta_upload = os.path.join(current_app.static_folder, "uploads")
        try:
            PostagemService.cadastrar(current_user, texto, arquivo_foto, pasta_upload)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        return jsonify({"mensagem": "Postagem publicada!"}), 201

    @staticmethod
    @login_required
    def excluir(postagem_id):
        try:
            PostagemService.excluir(current_user, postagem_id)
        except PermissionError as erro:
            return jsonify({"erro": str(erro)}), 403
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 404
        return jsonify({"mensagem": "Postagem excluída."})
