from bd import bd

class Rango(bd.Model):
    __tablename__ = 'rango'

    id_rango = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(50), nullable=False)
    descripcion = bd.Column(bd.String(150))