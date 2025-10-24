# models/Persona.py
from bd import bd

class Persona(bd.Model):
    __tablename__ = 'persona'

    id_persona = bd.Column(bd.Integer, primary_key=True)
    dni = bd.Column(bd.String(15), nullable=False, unique=True)
    nombres = bd.Column(bd.String(100), nullable=False)
    apellidos = bd.Column(bd.String(100), nullable=False)
    fecha_nacimiento = bd.Column(bd.Date)
    telefono = bd.Column(bd.String(20))
    direccion = bd.Column(bd.String(150))
    ubigeo = bd.Column(bd.String(5), bd.ForeignKey('ubigeo.codigo'))

    ubigeo_rel = bd.relationship('Ubigeo', backref='personas')

