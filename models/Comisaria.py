from bd import bd

class Comisaria(bd.Model):
    __tablename__ = 'comisaria'

    id_comisaria = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(100), nullable=False)
    direccion = bd.Column(bd.String(200))
    ubigeo = bd.Column(bd.String(5), bd.ForeignKey('ubigeo.codigo'))
    telefono = bd.Column(bd.String(20))

    ubigeo_rel = bd.relationship('Ubigeo', backref='comisarias')