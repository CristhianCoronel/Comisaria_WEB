from bd import bd

class Denuncia(bd.Model):
    __tablename__ = 'denuncia'

    id_denuncia = bd.Column(bd.Integer, primary_key=True)
    fecha_registro = bd.Column(bd.DateTime, default=bd.func.current_timestamp())
    fecha_acto = bd.Column(bd.Date)
    lugar_hechos = bd.Column(bd.String(200), nullable=False)
    descripcion = bd.Column(bd.Text, nullable=False)
    estado = bd.Column(bd.String(1), default='P')
    id_denunciante = bd.Column(bd.Integer, bd.ForeignKey('persona.id_persona'), nullable=False)
    id_denunciado = bd.Column(bd.Integer, bd.ForeignKey('persona.id_persona'))
    id_usuario = bd.Column(bd.Integer, bd.ForeignKey('usuario.id_usuario'), nullable=False)
    id_tipo_denuncia = bd.Column(bd.Integer, bd.ForeignKey('tipo_denuncia.id_tipo'), nullable=False)
    ubigeo = bd.Column(bd.String(5), bd.ForeignKey('ubigeo.codigo'))

    denunciante = bd.relationship('Persona', foreign_keys=[id_denunciante], backref='denuncias_hechas')
    denunciado = bd.relationship('Persona', foreign_keys=[id_denunciado], backref='denuncias_recibidas')
    usuario = bd.relationship('Usuario', backref='denuncias')
    tipo_denuncia = bd.relationship('TipoDenuncia', backref='denuncias')
    ubigeo_rel = bd.relationship('Ubigeo', backref='denuncias')