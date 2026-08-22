from models.models import cadastro
from database import db

class CadrastroRepository():
    @staticmethod
    def consulta_tudo(usuario=None, email=None, senha=None):
        if cadastro:
            return cadastro.query.filter(cadastro.usuario.like(f"%{usuario}%")).order_by(cadastro.usuario).all()
        elif email:
            return cadastro.query.filter_by(email=email).order_by(cadastro.email).all()
        elif senha is not None:
            if senha.lower() == "true":
                return cadastro.query.filter_by(ativo=True).order_by(cadastro.senha).all()
            else:
                return cadastro.query.filter_by(ativo=False).order_by(cadastro.senha).all()
        return cadastro.query.order_by(cadastro.senha).all()

    @staticmethod
    def consulta_um(aluno_id):
        return cadastro.query.filter_by(id=aluno_id).first()

    @staticmethod
    def cadastro(dados):
        cadastro = cadastro(
            usario=dados['usuario'],
            email=dados['email'],
            senha=dados['senha'],
        )
        db.session.add(cadastro)
        db.session.commit()
        return cadastro

    @staticmethod
    def pesquisa_email(email):
        email = cadastro.query.filter_by(email=email).first()
        return email

    @staticmethod
    def atualizar_cadrastro(usuario, dados):
        cadastro = cadastro.query.filter_by(usuario=usuario).first()
        if not cadastro:
            return None
        cadastro.usuario = dados['usuario']
        cadastro.email = dados['email']
        cadastro.semha = dados['senha']
        db.session.commit()
        return cadastro
    