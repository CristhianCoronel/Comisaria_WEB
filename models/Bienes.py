from bd import bd

class Categoria_Bienes(bd.Model):
    __tablename__ = 'categoria_bienes'

    id_categoria = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(100), nullable=False)
    descripcion = bd.Column(bd.Text)

class Detalle_Bienes(bd.Model):
    __tablename__ = 'detalle_bienes'

    id_detalle = bd.Column(bd.Integer, primary_key=True)
    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia'), nullable=False)
    id_categoria = bd.Column(bd.Integer, bd.ForeignKey('categoria_bienes.id_categoria'), nullable=False)
    nombre = bd.Column(bd.String(200), nullable=False)
    monto_asciende = bd.Column(bd.Numeric(12,2))
    descripcion = bd.Column(bd.Text)
    tipo_bien = bd.Column(bd.String(50))

    denuncia = bd.relationship('Denuncia', backref='detalles_bienes')
    categoria = bd.relationship('Categoria_Bienes', backref='detalles_bienes')