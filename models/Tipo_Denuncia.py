from bd import bd

class Tipo_Denuncia(bd.Model):
    __tablename__ = 'tipo_denuncia'

    id_tipo = bd.Column(bd.Integer, primary_key=True)
    tipo_denuncia = bd.Column(bd.String(50), nullable=False)
    descripcion = bd.Column(bd.String(150))
    id_area = bd.Column(bd.Integer, bd.ForeignKey('area.id_area'))

    area = bd.relationship('Area', backref='tipos_denuncia')


class D_Asalto(bd.Model):
    __tablename__ = 'd_asalto'

    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia'), primary_key=True)
    hubo_violencia = bd.Column(bd.Boolean)

    denuncia = bd.relationship('Denuncia', backref='asalto')


class D_Hurto(bd.Model):
    __tablename__ = 'd_hurto'

    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia'), primary_key=True)
    circunstancias = bd.Column(bd.String(200))

    denuncia = bd.relationship('Denuncia', backref='hurto')


class D_Violencia_Familiar(bd.Model):
    __tablename__ = 'd_violencia_familiar'

    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia'), primary_key=True)
    tipo_violencia = bd.Column(bd.String(50))
    relacion_agresor = bd.Column(bd.String(50))
    medidas_proteccion = bd.Column(bd.Boolean)

    denuncia = bd.relationship('Denuncia', backref='violencia_familiar')

