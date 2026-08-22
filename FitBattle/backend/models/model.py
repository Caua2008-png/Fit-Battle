from database import db
from datetime import datetime

class Registro(db.Model):
    __tablename__ = 'registro'
    usuario = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(8), unique=True, nullable=False)
    