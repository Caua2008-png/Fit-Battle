from database import db
from models.treino import Treino


class TreinoRepository:
    @staticmethod
    def salvar(treino):
        db.session.add(treino)
        db.session.commit()
        return treino

    @staticmethod
    def buscar_por_id(treino_id):
        return Treino.query.get(treino_id)

    @staticmethod
    def excluir(treino):
        db.session.delete(treino)
        db.session.commit()

    @staticmethod
    def listar_todos():
        return Treino.query.all()
