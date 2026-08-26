from datetime import datetime, timezone

from database import db

CATEGORIAS_TREINO = ("musculacao", "cardio", "yoga", "outro")


class Treino(db.Model):
    __tablename__ = "treino"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    categoria = db.Column(db.String(20), nullable=False)
    titulo = db.Column(db.String(80), nullable=False)
    grupo = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.Text, nullable=False)

    duracao_min = db.Column(db.Float, nullable=False)
    metrica2_valor = db.Column(db.Float, nullable=False)
    metrica2_unidade = db.Column(db.String(20), nullable=False)
    metrica2_rotulo = db.Column(db.String(40), nullable=False)
    metrica3_valor = db.Column(db.Float, nullable=False)
    metrica3_unidade = db.Column(db.String(20), nullable=False)
    metrica3_rotulo = db.Column(db.String(40), nullable=False)

    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
