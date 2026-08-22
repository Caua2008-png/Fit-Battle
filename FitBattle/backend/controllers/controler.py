from flask import jsonify, request
from services.services import RegistroServices

class FitbattleController():

    @staticmethod
    def valida_dados(dados):
        if not dados:
            return jsonify({"erro": "JSON inválido"}), 400
        if len(dados.get("usuario", "")) < 3:
            return jsonify({"erro": "Nome inválido"}), 400
        senha = dados.get("senha")
        if senha is None:
            return jsonify({"erro": "Senha e obrigatória"}), 400
        if senha < 8:
            return jsonify({"erro": "O mínimo de caracteres é 8 "}), 400
        if senha > 8:
            return jsonify({"erro": "Senha inválida"}), 400
        email = dados.get("email")
        if not email:
            return jsonify({"erro": "Email obrigatório"}), 400
        if "@" not in email:
            return jsonify({"erro": "Email inválido"}), 400

    @staticmethod
    def cadastrar():
        dados = request.json
        valida_dados = FitbattleController.valida_dados(dados)
        if valida_dados is not True:
            return valida_dados

        registro = RegistroServices.cadastra_registro(
            usuario=dados["usuario"],
            senha=dados["idade"],
            email=dados["email"],
        )

        return jsonify({
            "mensagem": "Registro concluido!",
        })