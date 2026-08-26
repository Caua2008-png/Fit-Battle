from database import db
from models.usuario import Usuario


class UsuarioRepository:
    @staticmethod
    def buscar_por_id(usuario_id):
        return Usuario.query.get(usuario_id)

    @staticmethod
    def buscar_por_usuario(usuario):
        return Usuario.query.filter_by(usuario=usuario).first()

    @staticmethod
    def buscar_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def buscar_por_usuario_ou_email(identificador):
        return Usuario.query.filter(
            (Usuario.usuario == identificador) | (Usuario.email == identificador)
        ).first()

    @staticmethod
    def listar_ranking():
        return Usuario.query.order_by(Usuario.xp.desc()).all()

    @staticmethod
    def salvar(usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def atualizar():
        db.session.commit()
