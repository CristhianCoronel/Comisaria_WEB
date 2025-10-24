from bd import bd

class Rol(bd.Model):
    __tablename__ = 'rol'

    id_rol = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(50), nullable=False)
    descripcion = bd.Column(bd.String(150))
    id_area = bd.Column(bd.Integer, bd.ForeignKey('area.id_area'))

    area = bd.relationship('Area', backref='roles')