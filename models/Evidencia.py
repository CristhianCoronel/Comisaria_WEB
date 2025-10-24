# models/Evidencia.py
from bd import bd

class Evidencia(bd.Model):
    __tablename__ = 'evidencia'

    id_evidencia = bd.Column(bd.Integer, primary_key=True)
    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia'), nullable=False)
    tipo = bd.Column(bd.String(50))
    url_archivo = bd.Column(bd.String(200))
    descripcion = bd.Column(bd.Text)

    denuncia = bd.relationship('Denuncia', backref='evidencias')
