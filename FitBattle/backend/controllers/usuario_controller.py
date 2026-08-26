import os

from flask import current_app, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user

from repositories.postagem_repository import PostagemRepository
from repositories.treino_repository import TreinoRepository
from services.usuario_service import UsuarioService


class UsuarioController:
    @staticmethod
    def cadastrar():
        dados = request.get_json(silent=True)
        if not dados:
            return jsonify({"erro": "JSON inválido"}), 400
        try:
            usuario = UsuarioService.cadastrar(dados)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

        login_user(usuario)
        return jsonify({"mensagem": "Cadastro concluído!", "usuario": usuario.usuario}), 201

    @staticmethod
    def login():
        dados = request.get_json(silent=True)
        if not dados:
            return jsonify({"erro": "JSON inválido"}), 400
        try:
            usuario = UsuarioService.autenticar(dados.get("identificador"), dados.get("senha"))
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 401

        login_user(usuario, remember=True)
        return jsonify({"mensagem": "Login realizado!", "usuario": usuario.usuario})

    @staticmethod
    @login_required
    def logout():
        logout_user()
        return jsonify({"mensagem": "Sessão encerrada."})

    @staticmethod
    def sessao():
        if not current_user.is_authenticated:
            return jsonify({"autenticado": False}), 200
        return jsonify({"autenticado": True, "usuario": current_user.usuario})

    @staticmethod
    @login_required
    def perfil():
        total_treinos = len([t for t in TreinoRepository.listar_todos() if t.usuario_id == current_user.id])
        total_postagens = len([p for p in PostagemRepository.listar_todas() if p.usuario_id == current_user.id])
        posicao = UsuarioService.posicao_no_ranking(current_user)
        return jsonify(
            UsuarioService.montar_perfil(current_user, total_treinos, total_postagens, posicao)
        )

    @staticmethod
    @login_required
    def atualizar_perfil():
        dados = request.get_json(silent=True) or {}
        try:
            UsuarioService.atualizar_perfil(current_user, dados)
        except (TypeError, ValueError):
            return jsonify({"erro": "Dados de perfil inválidos."}), 400
        return jsonify({"mensagem": "Perfil atualizado."})

    @staticmethod
    @login_required
    def enviar_avatar():
        arquivo = request.files.get("avatar")
        if not arquivo:
            return jsonify({"erro": "Nenhum arquivo enviado."}), 400

        pasta_upload = os.path.join(current_app.static_folder, "uploads")
        try:
            UsuarioService.salvar_avatar(current_user, arquivo, pasta_upload)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        return jsonify({"mensagem": "Avatar atualizado.", "avatar": current_user.avatar})

    @staticmethod
    @login_required
    def atualizar_configuracoes():
        dados = request.get_json(silent=True) or {}
        UsuarioService.atualizar_configuracoes(current_user, dados)
        return jsonify({"mensagem": "Configurações atualizadas."})

    @staticmethod
    def ranking():
        return jsonify(UsuarioService.montar_ranking())
