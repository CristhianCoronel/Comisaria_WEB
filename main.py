from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, session, flash
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from bd import bd
from functools import wraps

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
    departamentos = controlador_departamento.obtener_departamentos()
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

    
    return render_template('login.html', departamentos=departamentos)


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
    return render_template('persona.html', personas=personas)

@app.route('/api/personas', methods=['POST'])
@login_required
def api_guardar_persona():
    try:
        data = request.get_json()

        dni = data.get("dni")
        nombres = data.get("nombres")
        apellidos = data.get("apellidos")
        fecha_nacimiento = data.get("fecha_nacimiento")
        telefono = data.get("telefono")
        direccion = data.get("direccion")
        ubigeo = data.get("ubigeo")

        # --- Validaciones ---
        if not dni or not nombres or not apellidos:
            return jsonify({
                "status": 0,
                "data": None,
                "message": "Faltan campos obligatorios."
            }), 400

        # --- Insertar la nueva persona ---
        controlador_persona.insertar_persona(
            dni, nombres, apellidos, fecha_nacimiento, telefono, direccion, ubigeo
        )

        persona = controlador_persona.obtener_ultima_persona()

        if not persona:
            return jsonify({
                "status": 0,
                "data": None,
                "message": "No se pudo obtener la persona recién registrada."
            }), 404

        persona_json = {
            "id_persona": persona.id_persona,
            "dni": persona.dni,
            "nombres": persona.nombres,
            "apellidos": persona.apellidos,
            "fecha_nacimiento": persona.fecha_nacimiento.strftime("%Y-%m-%d") if persona.fecha_nacimiento else None,
            "telefono": persona.telefono,
            "direccion": persona.direccion,
            "ubigeo": persona.ubigeo
        }

        return jsonify({
            "status": 1,
            "data": persona_json,
            "message": "Persona registrada correctamente."
        }), 201

    except Exception as e:
        print("Error en /api/personas:", e)
        return jsonify({
            "status": 0,
            "data": None,
            "message": f"Error interno del servidor: {str(e)}"
        }), 500


@app.route('/guardar_ciudadano')
@login_required
def guardar_persona():
    dni = request.form["dni"]
    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    fecha_nacimiento = request.form.get("fecha_nacimiento") or None  # puede venir vacío
    telefono = request.form.get("telefono") or None
    direccion = request.form.get("direccion") or None
    ubigeo = request.form.get("ubigeo") or None

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

@app.route("/api/personas/buscar", methods=["POST"])
@login_required
def api_buscar_persona():
    try:
        nombre = request.json.get("b_nombre", "")
        dni = request.json.get("b_dni", "")
        lista = controlador_persona.obtener_persona_nombre_dni(nombre, dni)

        personas_json = [
            {
                "id_persona": p.id_persona,
                "dni": p.dni,
                "nombres": p.nombres,
                "apellidos": p.apellidos,
                "fecha_nacimiento": p.fecha_nacimiento.strftime("%Y-%m-%d") if p.fecha_nacimiento else None,
                "telefono": p.telefono,
                "direccion": p.direccion,
                "ubigeo": p.ubigeo,
            }
            for p in lista
        ]

        return jsonify({
            "status": 1,
            "data": personas_json,
            "message": "Resultados obtenidos correctamente"
        })
    except Exception as e:
        print("Error:", e)
        return jsonify({
            "status": -1,
            "data": [],
            "message": f"Error al listar personas: {str(e)}"
        }), 500

@app.route('/persona/<int:id_persona>/json', methods=['GET'])
@login_required
def persona_por_id_json(id_persona):
    """Devuelve los datos de una persona en formato JSON dado su id."""
    try:
        persona = controlador_persona.obtener_persona_por_id(id_persona)
        if not persona:
            return jsonify({"status": 0, "data": None, "message": "Persona no encontrada"}), 404

        return jsonify({
            "status": 1,
            "data": {
                "id_persona": persona.id_persona,
                "dni": persona.dni,
                "nombres": persona.nombres,
                "apellidos": persona.apellidos,
                "fecha_nacimiento": persona.fecha_nacimiento,
                "telefono": persona.telefono,
                "direccion": persona.direccion
            }
        })
    except Exception as e:
        return jsonify({"status": -1, "data": None, "message": str(e)}), 500


@app.route("/historial")
@login_required
def ver_historial():
    return redirect('ciudadanos')


############# FIN PERSONA ###############

#############  AREA  ######################

@app.route('/area', methods=['GET'])
@login_required
def area():
    areas = controlador_area.obtener_areas()
    return render_template('area.html', areas=areas)

@app.route('/agregar_area')
@login_required
def formulario_agregar_area():
    return render_template('denuncia.html')

@app.route('/guardar_area', methods=['POST'])
@login_required
def guardar_area():
    nombre = request.form['nombre']
    descripcion = request.form.get('descripcion', '')
    controlador_area.insertar_area(nombre,descripcion)
    return redirect(url_for('area'))

@app.route('/formulario_editar_area/<int:id_area>')
@login_required
def formulario_editar_area(id_area):
    area = controlador_area.obtener_area_por_id(id_area)
    return render_template('editar_area.html', area=area)

@app.route('/actualizar_area', methods=['POST'])
@login_required
def actualizar_area():
    id_area = request.form['id_area']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    controlador_area.modificar_area(id_area, nombre, descripcion)
    return redirect('area')

@app.route('/eliminar_area')
@login_required
def eliminar_area():
    id_area = request.form['id_area']
    controlador_area.eliminar_area(id_area)

@app.route('/buscar_area', methods=['POST'])
@login_required
def buscar_area():
    return render_template('denuncia.html')

@app.route('/area/<int:id_area>/json', methods=['GET'])
@login_required
def area_por_id_json(id_area):
    """Devuelve los datos de un área en formato JSON dado su id."""
    try:
        area = controlador_area.obtener_area_por_id(id_area)
        if not area:
            return jsonify({"status": 0, "data": None, "message": "Área no encontrada"}), 404

        return jsonify({
            "status": 1,
            "data": {
                "id_area": area.id_area,
                "nombre": area.nombre,
                "descripcion": area.descripcion
            }
        })
    except Exception as e:
        return jsonify({"status": -1, "data": None, "message": str(e)}), 500

######################################

############# COMISARÍA ##############

# Listar comisarías
@app.route('/comisaria', methods=['GET'])
@login_required
def comisaria():
    comisarias = controlador_comisaria.obtener_comisarias()
    return render_template('comisaria.html', comisarias=comisarias, ubigeos=controlador_ubigeo.obtener_ubigeos())

@app.route('/agregar_comisaria')
@login_required
def formulario_agregar_comisaria():
    return render_template('comisaria.html', comisaria=None, ubigeos=controlador_ubigeo.obtener_ubigeos())

@app.route('/guardar_comisaria', methods=['POST'])
@login_required
def guardar_comisaria():
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    ubigeo = request.form['ubigeo']
    controlador_comisaria.insertar_comisaria(nombre, direccion, ubigeo, telefono)
    return redirect(url_for('comisaria'))

@app.route('/formulario_editar_comisaria/<int:id_comisaria>')
@login_required
def formulario_editar_comisaria(id_comisaria):
    comisaria = controlador_comisaria.obtener_comisaria_por_id(id_comisaria)
    return render_template('comisaria.html', comisaria=comisaria, ubigeos=controlador_ubigeo.obtener_ubigeos())

@app.route('/actualizar_comisaria', methods=['POST'])
@login_required
def actualizar_comisaria():
    id_comisaria = request.form['id_comisaria']
    nombre = request.form['nombre']
    direccion = request.form.get('direccion', '')
    telefono = request.form.get('telefono', '')
    ubigeo = request.form.get('ubigeo', '')
    controlador_comisaria.modificar_comisaria(id_comisaria, nombre, direccion, ubigeo, telefono)
    return redirect(url_for('comisaria'))

@app.route('/eliminar_comisaria', methods=['POST'])
@login_required
def eliminar_comisaria():
    id_comisaria = request.form['id_comisaria']
    controlador_comisaria.eliminar_comisaria(id_comisaria)
    return redirect(url_for('comisaria'))

@app.route('/buscar_comisaria', methods=['POST'])
@login_required
def buscar_comisaria():
    nombre = request.form.get("b_nombre", "")
    direccion = request.form.get("b_direccion", "")
    lista = controlador_comisaria.obtener_comisaria_nombre_direccion(nombre, direccion)
    return jsonify({
        "status": 1,
        "data": [{"id_comisaria": c.id_comisaria, "nombre": c.nombre, "direccion": c.direccion, "telefono": c.telefono, "ubigeo": c.ubigeo} for c in lista],
        "message": "Comisarías encontradas"
    })


#######################################

############# DENUNCIA ####################

@app.route('/denuncia')
@login_required
def denuncia():
    return render_template('denuncia.html')



######### FIN DENUNCIA #################



if __name__ == '__main__':
    app.run(debug=True, port=5000)
