from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, session, flash
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from bd import bd
from functools import wraps
from dotenv import load_dotenv

from controllers import controlador_departamento
from controllers import controlador_provincia
from controllers import controlador_distrito
from controllers import controlador_ubigeo
from controllers import controlador_comisaria
from controllers import controlador_area
from controllers import controlador_rango
from controllers import controlador_rol
from controllers import controlador_persona
from controllers import controlador_usuario
from controllers import controlador_categoria_bienes
from controllers import controlador_tipo_denuncia
from controllers import controlador_denuncia
from controllers import controlador_d_hurto
from controllers import controlador_d_asalto
from controllers import controlador_d_violencia_familiar
from controllers import controlador_detalles_bienes
from controllers import controlador_evidencia

from models.Ubigeo import Departamento, Provincia, Distrito, Ubigeo
from models.Comisaria import Comisaria
from models.Area import Area
from models.Rango import Rango
from models.Rol import Rol
from models.Persona import Persona
from models.Usuario import Usuario
from models.Bienes import Categoria_Bienes
from models.Tipo_Denuncia import Tipo_Denuncia
from models.Denuncia import Denuncia
from models.Tipo_Denuncia import D_Hurto
from models.Tipo_Denuncia import D_Asalto
from models.Tipo_Denuncia import D_Violencia_Familiar
from models.Bienes import Detalle_Bienes
from models.Evidencia import Evidencia

import os, json

app = Flask(__name__)

##  postgresql, usuario, contraseña, host, puerto, nombre_db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bd_comisaria_user:HmGlVBo5J21P0ojPxCrO24tMZ2gxxc68@dpg-d3tu8n6uk2gs73df7b50-a.oregon-postgres.render.com:5432/bd_comisaria'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:WgtzsruCmjT7dmlB8Hjxim4xqv8uXpnG@dpg-d3v50s3e5dus73a4ogu0-a.oregon-postgres.render.com/bd_comisaria_008i'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.secret_key = os.environ.get('FLASK_SECRET_KEY')
# app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.secret_key = "clave_local_flask"
app.config['JWT_SECRET_KEY'] = "clave_local_jwt"

# Inicializar la base de datos
bd.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ACTIVO TOKEN PARA LA API DE LA RENIEC

load_dotenv()

FACILIZA_TOKEN = os.getenv("FACILIZA_TOKEN")
FACILIZA_URL = os.getenv("FACILIZA_URL", "https://api.factiliza.com/v1/dni/info")

# Crear tablas si no existen
with app.app_context():
    bd.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('token')  # Busca el token JWT en sesión
        if not token:
            flash("Debes iniciar sesión primero.", "warning")
            return redirect(url_for('login'))  # Redirige al login si no hay token
        return f(*args, **kwargs)
    return decorated_function

# --- RUTAS FIJAS --- #

@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/index')
@login_required
def index():
    # 1) Total de ciudadanos (todas las personas registradas)
    total_ciudadanos = Persona.query.count()

    # 2) Denuncias activas (por ejemplo estados P = pendiente, A = activa)
    denuncias_activas = Denuncia.query.filter(
        Denuncia.estado.in_(["P", "A"])
    ).count()

    # 3) Personal activo (usuarios con estado 'A')
    personal_activo = Usuario.query.filter_by(estado="A").count()

    # 4) Total de comisarías registradas
    total_comisarias = Comisaria.query.count()

    # 5) Actividad reciente: últimas 5 denuncias registradas
    actividad_reciente = (
        Denuncia.query
        .order_by(Denuncia.fecha_registro.desc())
        .limit(5)
        .all()
    )

    # 6) Denuncias pendientes (estado 'P') + nombre del tipo de denuncia
    pendientes_raw = (
        bd.session.query(Denuncia, Tipo_Denuncia)
        .join(Tipo_Denuncia, Denuncia.id_tipo_denuncia == Tipo_Denuncia.id_tipo)
        .filter(Denuncia.estado == "P")
        .order_by(Denuncia.fecha_registro.desc())
        .limit(5)
        .all()
    )

    # Transformar a una lista simple de diccionarios para el template
    denuncias_pendientes = []
    for denuncia, tipo in pendientes_raw:
        denuncias_pendientes.append({
            "id": denuncia.id_denuncia,
            "codigo": f"DEN-{denuncia.id_denuncia:06d}",
            "tipo": tipo.tipo_denuncia,
            "fecha": denuncia.fecha_registro,  # por si luego quieres mostrarla
            # si quieres más adelante, aquí puedes calcular prioridad según tipo
            "prioridad": "Alta"
        })

    return render_template(
        "index.html",
        total_ciudadanos=total_ciudadanos,
        denuncias_activas=denuncias_activas,
        personal_activo=personal_activo,
        total_comisarias=total_comisarias,
        actividad_reciente=actividad_reciente,
        denuncias_pendientes=denuncias_pendientes
    )



########## CONTROL DE SESION  ##########

@app.route('/login', methods=['GET', 'POST'])
def login():
    departamentos = controlador_departamento.obtener_departamentos()
    if request.method == 'POST':
        dni = request.form['usuario']
        contrasena = request.form['contrasena']
        usuario = Usuario.query.filter_by(dni=dni, estado='A').first()
        
        if usuario and bcrypt.check_password_hash(usuario.codigo_usuario, contrasena):
            token = create_access_token(identity=usuario.dni)
            
            session['token'] = token
            session['dni'] = usuario.dni
            session['usuario'] = f"{usuario.ape_paterno} {usuario.ape_materno[0]}. {usuario.nombres}"
            session['tipo'] = usuario.tipo_usuario
            comisaria = Comisaria.query.filter_by(id_comisaria=usuario.id_comisaria).first()
            rango = Rango.query.filter_by(id_rango=usuario.id_rango).first()
            session['comisaria'] = comisaria.nombre
            session['rango'] = rango.nombre
            
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('index')) 
        else:
            flash("Credenciales incorrectas o usuario inactivo.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html', departamentos=departamentos)


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    flash("Has cerrado sesión.", "success")
    return redirect(url_for('login'))


# Importar rutas que están separadas en otros archivos
from routes_persona import *
from routes_area import *
from routes_comisaria import *
from routes_denuncia import *


if __name__ == '__main__':
    app.run(debug=True, port=5000)

