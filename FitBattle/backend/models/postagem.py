from datetime import datetime, timezone

from database import db


class Postagem(db.Model):
    __tablename__ = "postagem"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    texto = db.Column(db.Text, nullable=False)
    foto = db.Column(db.String(255), nullable=True)

    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
