from database import db
from models.postagem import Postagem


class PostagemRepository:
    @staticmethod
    def salvar(postagem):
        db.session.add(postagem)
        db.session.commit()
        return postagem

    @staticmethod
    def buscar_por_id(postagem_id):
        return Postagem.query.get(postagem_id)

    @staticmethod
    def excluir(postagem):
        db.session.delete(postagem)
        db.session.commit()

    @staticmethod
    def listar_todas():
        return Postagem.query.all()
