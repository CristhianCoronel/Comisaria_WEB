from bd import bd

class Area(bd.Model):
    __tablename__ = 'area'

    id_area = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(100), nullable=False)
    descripcion = bd.Column(bd.String(150))