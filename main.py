from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, session, flash
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from bd import bd
from functools import wraps
from controllers import controlador_evidencia
from controllers import controlador_departamento
from controllers import controlador_persona

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:usat_2025@localhost:5432/bd_comisaria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'clave_para_flash'
app.config['JWT_SECRET_KEY'] = 'clave_super_secreta_para_jwt'

# Inicializar la base de datos
bd.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


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
def index():
    departamentos = list()
    # departamentos = controlador_departamento.obtener_departamentos()
    return render_template('index.html', departamentos=departamentos)


########## CONTROL DE SESION  ##########

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dni = request.form['usuario']
        contrasena = request.form['contrasena']

        usuario = Usuario.query.filter_by(dni=dni, estado='A').first()

        if usuario and bcrypt.check_password_hash(usuario.codigo_usuario, contrasena):
            token = create_access_token(identity=usuario.dni)
            
            session['token'] = token
            
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('index')) 
        else:
            flash("Credenciales incorrectas o usuario inactivo.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('token', None)
    flash("Has cerrado sesión.", "success")
    return redirect(url_for('login'))

###########################################


############### PERSONA #################

@app.route('/ciudadanos')
@login_required
def persona():
    personas = controlador_persona.obtener_personas()
    return render_template('persona.html', personas = personas)

@app.route('/agregar_ciudadano')
@login_required
def formulario_agregar_persona():
    return render_template('agregar_persona.html')

@app.route('/guardar_ciudadano')
@login_required
def guardar_persona():
    dni = request.form["dni"]
    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    fecha_nacimiento = request.form.get("fecha_nacimiento") or None  # puede venir vacío
    telefono = request.form.get("telefono") or None
    direccion = request.form.get("direccion") or None

    controlador_persona.insertar_persona(dni, nombres, apellidos, fecha_nacimiento, telefono, direccion)
    return redirect("/personas")
    
@app.route("/editar_ciudadano/<int:id>")
@login_required
def formulario_editar_persona(id):
    persona = controlador_persona.obtener_persona_por_id(id)
    return render_template("editar_persona.html", persona=persona)


@app.route("/actualizar_persona", methods=["POST"])
@login_required
def actualizar_persona():
    id_persona = request.form["id_persona"]
    dni = request.form["dni"]
    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    fecha_nacimiento = request.form.get("fecha_nacimiento") or None
    telefono = request.form.get("telefono") or None
    direccion = request.form.get("direccion") or None

    controlador_persona.actualizar_persona(dni, nombres, apellidos, fecha_nacimiento, telefono, direccion, id_persona)
    return redirect("/personas")

@app.route("/listar_persona")
@login_required
def listar_persona():
    return redirect('ciudadanos')

@app.route("/historial")
@login_required
def ver_historial():
    return redirect('ciudadanos')


############# FIN PERSONA ###############


############# DENUNCIA ####################

@app.route('/denuncia')
@login_required
def denuncia():
    return render_template('denuncia.html')



######### FIN DENUNCIA #################



if __name__ == '__main__':
    app.run(debug=True, port=5000)
