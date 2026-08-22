import re
from werkzeug.security import generate_password_hash


class CadastrarUsuarioService:
    def _init_(self, usuario_model_class_re):
        self.registro_model_class = re

    def executar(self, dados):
        
        usuario = dados.get("usuario")
        email = dados.get("email")
        senha = dados.get("senha")

        if not usuario or not email or not senha:
            raise ValueError("Todos os campos devem ser preenchidos.")

        if len(senha) < 8:
            raise ValueError("A senha deve ter no mínimo 8 caracteres.")

        padrao_email = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(padrao_email, email):
            raise ValueError("Informe um e-mail válido.")

        if self.usuario_model_class.query.filter_by(email=email).first():
            raise ValueError("E-mail já cadastrado no sistema.")

        if self.usuario_model_class.query.filter_by(usuario=usuario).first():
            raise ValueError("Nome de usuário já está em uso.")

        senha_hash = generate_password_hash(senha)

        novo_usuario = self.usuario_model_class(
            usuario=usuario,
            email=email,
            senha=senha_hash
        )

        return novo_usuario.salvar()