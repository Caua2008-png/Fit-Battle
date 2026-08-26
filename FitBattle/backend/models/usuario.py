from datetime import datetime, timezone

from flask_login import UserMixin

from database import db


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)

    nome = db.Column(db.String(120), nullable=False)
    handle = db.Column(db.String(80), nullable=False)
    localizacao = db.Column(db.String(120), default="")
    bio = db.Column(db.Text, default="")
    avatar = db.Column(db.String(255), nullable=True)

    peso = db.Column(db.Float, nullable=True)
    altura = db.Column(db.Float, nullable=True)
    idade = db.Column(db.Integer, nullable=True)

    xp = db.Column(db.Integer, default=0, nullable=False)
    streak = db.Column(db.Integer, default=0, nullable=False)
    ultimo_treino_em = db.Column(db.Date, nullable=True)

    unit_lb = db.Column(db.Boolean, default=False, nullable=False)
    notif = db.Column(db.Boolean, default=True, nullable=False)
    public_ranking = db.Column(db.Boolean, default=True, nullable=False)

    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    treinos = db.relationship("Treino", backref="autor", cascade="all, delete-orphan")
    postagens = db.relationship("Postagem", backref="autor", cascade="all, delete-orphan")
