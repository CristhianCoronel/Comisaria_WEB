from bd import bd

# ---------------------------
# TABLAS PRINCIPALES
# ---------------------------

class Rango(bd.Model):
    __tablename__ = 'rango'  # Tabla original: Rango
    id_rango = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(30), nullable=False)

class Rol(bd.Model):
    __tablename__ = 'rol'  # Tabla original: Rol
    id_rol = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(30), nullable=False)

class Departamento(bd.Model):
    __tablename__ = 'departamento'  # Tabla original: Departamento
    id_departamento = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(30), nullable=False)

class Provincia(bd.Model):
    __tablename__ = 'provincia'  # Tabla original: Provincia
    id_provincia = bd.Column(bd.Integer, primary_key=True)
    id_departamento = bd.Column(bd.Integer, bd.ForeignKey('departamento.id_departamento'), nullable=False)
    nombre = bd.Column(bd.String(30), nullable=False)

    departamento = bd.relationship('Departamento', backref='provincias')

class Distrito(bd.Model):
    __tablename__ = 'distrito'  # Tabla original: Distrito
    id_distrito = bd.Column(bd.Integer, primary_key=True)
    id_provincia = bd.Column(bd.Integer, bd.ForeignKey('provincia.id_provincia'), nullable=False)
    nombre = bd.Column(bd.String(30), nullable=False)
    ubigeo = bd.Column(bd.String(5), nullable=False)

    provincia = bd.relationship('Provincia', backref='distritos')

class Comisaria(bd.Model):
    __tablename__ = 'comisaria'  # Tabla original: Comisaria
    id_comisaria = bd.Column(bd.Integer, primary_key=True)
    id_distrito = bd.Column(bd.Integer, bd.ForeignKey('distrito.id_distrito'), nullable=False)
    nombre = bd.Column(bd.String(30), nullable=False)
    telefono = bd.Column(bd.String(30), nullable=False)
    direccion = bd.Column(bd.String(50), nullable=False)

    distrito = bd.relationship('Distrito', backref='comisarias')

class Usuario(bd.Model):
    __tablename__ = 'usuario'  # Tabla original: Usuario
    id_usuario = bd.Column(bd.Integer, primary_key=True)
    dni = bd.Column(bd.String(8), nullable=False)
    nombres = bd.Column(bd.String(50), nullable=False)
    ape_paterno = bd.Column(bd.String(50), nullable=False)
    ape_materno = bd.Column(bd.String(50), nullable=False)
    estado = bd.Column(bd.String(1), nullable=False)  # A/I/R
    codigo_usuario = bd.Column(bd.String(50), nullable=False)
    clave = bd.Column(bd.String(100), nullable=False)
    id_comisaria = bd.Column(bd.Integer, bd.ForeignKey('comisaria.id_comisaria'), nullable=False)
    id_rango = bd.Column(bd.Integer, bd.ForeignKey('rango.id_rango'), nullable=False)
    id_rol = bd.Column(bd.Integer, bd.ForeignKey('rol.id_rol'), nullable=False)

    comisaria = bd.relationship('Comisaria', backref='usuarios')
    rango = bd.relationship('Rango', backref='usuarios')
    rol = bd.relationship('Rol', backref='usuarios')

class Tipo_Documento(bd.Model):
    __tablename__ = 'tipo_documento'  # Tabla original: Tipo_Documento
    id_tipo_documento = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(50), nullable=False)

class Persona(bd.Model):
    __tablename__ = 'persona'  # Tabla original: Persona
    id_persona = bd.Column(bd.Integer, primary_key=True)
    id_tipo_documento = bd.Column(bd.Integer, bd.ForeignKey('tipo_documento.id_tipo_documento'), nullable=False)
    documento = bd.Column(bd.String(20), nullable=False)
    nombre = bd.Column(bd.String(50), nullable=False)
    ape_paterno = bd.Column(bd.String(50), nullable=False)
    ape_materno = bd.Column(bd.String(50), nullable=False)
    id_distrito = bd.Column(bd.Integer, bd.ForeignKey('distrito.id_distrito'), nullable=False)
    fecha_nacimiento = bd.Column(bd.Date, nullable=False)
    direccion = bd.Column(bd.String(50), nullable=False)
    estado_civil = bd.Column(bd.String(30), nullable=False)
    ocupacion = bd.Column(bd.String(30), default='Sin ocupación')
    telefono = bd.Column(bd.String(30))
    correo = bd.Column(bd.String(50))

    tipo_documento = bd.relationship('Tipo_Documento', backref='personas')
    distrito = bd.relationship('Distrito', backref='personas')

class Tipo_Denuncia(bd.Model):
    __tablename__ = 'tipo_denuncia'  # Tabla original: Tipo_Denuncia
    id_tipo_denuncia = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(30), nullable=False)

class Estado_Denuncia(bd.Model):
    __tablename__ = 'estado_denuncia'  # Tabla original: Estado_Denuncia
    id_estado_denuncia = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(30), nullable=False)

class Denuncia(bd.Model):
    __tablename__ = 'denuncia'  # Tabla original: Denuncia
    id_denuncia = bd.Column(bd.Integer, primary_key=True)
    fecha_registro = bd.Column(bd.Date, default=bd.func.current_date())
    hora_registro = bd.Column(bd.Time, default=bd.func.current_time())
    fecha_incidente = bd.Column(bd.Date, nullable=False)
    hora_incidente = bd.Column(bd.Time)
    lugar_hechos = bd.Column(bd.String(50), nullable=False)
    direccion = bd.Column(bd.String(50), nullable=False)
    descripcion = bd.Column(bd.Text, nullable=False)
    id_denunciante = bd.Column(bd.Integer, bd.ForeignKey('persona.id_persona'), nullable=False)
    id_denunciado = bd.Column(bd.Integer, bd.ForeignKey('persona.id_persona'))
    id_tipo_denuncia = bd.Column(bd.Integer, bd.ForeignKey('tipo_denuncia.id_tipo_denuncia'), nullable=False)
    id_estado_denuncia = bd.Column(bd.Integer, bd.ForeignKey('estado_denuncia.id_estado_denuncia'), nullable=False)

    denunciante = bd.relationship('Persona', foreign_keys=[id_denunciante], backref='denuncias_realizadas')
    denunciado = bd.relationship('Persona', foreign_keys=[id_denunciado], backref='denuncias_recibidas')
    tipo_denuncia = bd.relationship('Tipo_Denuncia', backref='denuncias')
    estado_denuncia = bd.relationship('Estado_Denuncia', backref='denuncias')

# ---------------------------
# TIPOS DE DENUNCIA
# ---------------------------

class D_Delito_Patrimonio(bd.Model):
    __tablename__ = 'd_delito_patrimonio'
    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia', ondelete='CASCADE'), primary_key=True)
    tipo_delito = bd.Column(bd.String(30), nullable=False)
    monto_estimado = bd.Column(bd.Numeric(9,2))

    denuncia = bd.relationship('Denuncia', backref='delito_patrimonio', uselist=False)

class D_Violencia_Domestica(bd.Model):
    __tablename__ = 'd_violencia_domestica'
    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia', ondelete='CASCADE'), primary_key=True)
    tipo = bd.Column(bd.String(30), nullable=False)
    parentesco = bd.Column(bd.String(30), nullable=False)

    denuncia = bd.relationship('Denuncia', backref='violencia_domestica', uselist=False)

class D_Extorsion(bd.Model):
    __tablename__ = 'd_extorsion'
    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia', ondelete='CASCADE'), primary_key=True)
    alias_extorsion = bd.Column(bd.String(30))
    cantidad = bd.Column(bd.Integer, nullable=False)

    denuncia = bd.relationship('Denuncia', backref='extorsion', uselist=False)

# ---------------------------
# BIENES
# ---------------------------

class Bienes(bd.Model):
    __tablename__ = 'bienes'
    id_bien = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(50), nullable=False)

class Detalle_Bienes(bd.Model):
    __tablename__ = 'detalle_bienes'
    id_detalle_bien = bd.Column(bd.Integer, primary_key=True)
    id_bien = bd.Column(bd.Integer, bd.ForeignKey('bienes.id_bien'), nullable=False)
    marca = bd.Column(bd.String(30))
    modelo = bd.Column(bd.String(30))
    unidades = bd.Column(bd.Integer, nullable=False)
    valor_estimado = bd.Column(bd.Numeric(9,2))
    descripcion = bd.Column(bd.String(100))
    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia', ondelete='CASCADE'), nullable=False)

    bien = bd.relationship('Bienes', backref='detalle_bienes')
    denuncia = bd.relationship('Denuncia', backref='detalle_bienes')

# ---------------------------
# SOSPECHOSOS
# ---------------------------

class Detalle_Sospechoso(bd.Model):
    __tablename__ = 'detalle_sospechoso'
    id_detalle_sospechoso = bd.Column(bd.Integer, primary_key=True)
    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia', ondelete='CASCADE'), nullable=False)
    dni = bd.Column(bd.String(20))
    nombres = bd.Column(bd.String(200))
    descripcion = bd.Column(bd.Text)
    rol_participacion = bd.Column(bd.String(100))

    denuncia = bd.relationship('Denuncia', backref='detalle_sospechoso')

# ---------------------------
# ARMAS
# ---------------------------

class Tipo_Arma(bd.Model):
    __tablename__ = 'tipo_arma'
    id_tipo_arma = bd.Column(bd.Integer, primary_key=True)
    nombre = bd.Column(bd.String(50), nullable=False)

class Arma(bd.Model):
    __tablename__ = 'arma'
    id_arma = bd.Column(bd.Integer, primary_key=True)
    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia', ondelete='CASCADE'), nullable=False)
    id_tipo_arma = bd.Column(bd.Integer, bd.ForeignKey('tipo_arma.id_tipo_arma'), nullable=False)
    descripcion = bd.Column(bd.String(100))
    cantidad = bd.Column(bd.Integer, default=1)

    denuncia = bd.relationship('Denuncia', backref='arma')
    tipo_arma = bd.relationship('Tipo_Arma', backref='arma')

# ---------------------------
# EVIDENCIA
# ---------------------------

class Evidencia(bd.Model):
    __tablename__ = 'evidencia'
    id_evidencia = bd.Column(bd.Integer, primary_key=True)
    titulo = bd.Column(bd.String(50), nullable=False)
    descripcion = bd.Column(bd.String(200))
    ruta = bd.Column(bd.Text, nullable=False)
    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia', ondelete='CASCADE'), nullable=False)

    denuncia = bd.relationship('Denuncia', backref='evidencia')

# ---------------------------
# SEGUIMIENTO
# ---------------------------

class Seguimiento_Denuncia(bd.Model):
    __tablename__ = 'seguimiento_denuncia'
    id_seguimiento = bd.Column(bd.Integer, primary_key=True)
    id_usuario = bd.Column(bd.Integer, bd.ForeignKey('usuario.id_usuario', ondelete='CASCADE'), nullable=False)
    id_denuncia = bd.Column(bd.Integer, bd.ForeignKey('denuncia.id_denuncia', ondelete='CASCADE'), nullable=False)
    fecha = bd.Column(bd.Date, nullable=False)
    accion = bd.Column(bd.String(50), nullable=False)

    usuario = bd.relationship('Usuario', backref='seguimiento_denuncia')
    denuncia = bd.relationship('Denuncia', backref='seguimiento_denuncia')
    