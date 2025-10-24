from bd import bd

class Departamento(bd.Model):
    __tablename__ = 'departamento'

    id_departamento = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(100), nullable=False)


class Provincia(bd.Model):
    __tablename__ = 'provincia'

    id_provincia = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(100), nullable=False)
    id_departamento = bd.Column(bd.Integer, bd.ForeignKey('departamento.id_departamento'), nullable=False)

    departamento = bd.relationship('Departamento', backref='provincias')


class Distrito(bd.Model):
    __tablename__ = 'distrito'

    id_distrito = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(100), nullable=False)
    id_provincia = bd.Column(bd.Integer, bd.ForeignKey('provincia.id_provincia'), nullable=False)

    provincia = bd.relationship('Provincia', backref='distritos')


class Ubigeo(bd.Model):
    __tablename__ = 'ubigeo'

    id_ubigeo = bd.Column(bd.Integer, primary_key=True)
    codigo = bd.Column(bd.String(5), unique=True, nullable=False)
    id_distrito = bd.Column(bd.Integer, bd.ForeignKey('distrito.id_distrito'), nullable=False)

    distrito = bd.relationship('Distrito', backref='ubigeos')
