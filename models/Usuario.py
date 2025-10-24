from bd import bd

class Usuario(bd.Model):
    __tablename__ = 'usuario'

    id_usuario = bd.Column(bd.Integer, primary_key=True)
    dni = bd.Column(bd.String(15), nullable=False, unique=True)
    nombres = bd.Column(bd.String(100), nullable=False)
    ape_paterno = bd.Column(bd.String(100), nullable=False)
    ape_materno = bd.Column(bd.String(100), nullable=False)
    codigo_usuario = bd.Column(bd.String(100))
    estado = bd.Column(bd.String(1), default='A')
    id_comisaria = bd.Column(bd.Integer, bd.ForeignKey('comisaria.id_comisaria'))
    id_rango = bd.Column(bd.Integer, bd.ForeignKey('rango.id_rango'))
    id_rol = bd.Column(bd.Integer, bd.ForeignKey('rol.id_rol'))
    tipo_usuario = bd.Column(bd.String(1))

    comisaria = bd.relationship('Comisaria', backref='usuarios')
    rango = bd.relationship('Rango', backref='usuarios')
    rol = bd.relationship('Rol', backref='usuarios')