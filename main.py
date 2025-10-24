from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_bcrypt import Bcrypt
from bd import bd
from controllers import controlador_evidencia
from controllers import controlador_departamento
from controllers import controlador_persona
from models import Ubigeo, Persona, Evidencia

import os, json

app = Flask(__name__)
bcrypt = Bcrypt(app)

##  postgresql, usuario, contraseña, host, puerto, nombre_db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:usat_2025@localhost:5432/bd_comisaria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
bd.init_app(app)

# Crear tablas si no existen
with app.app_context():
    bd.create_all()




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
        usuario = request.form['usuario']
        id_oficial = request.form['id_oficial']
        contrasena = request.form['contrasena']

        # Validación temporal (demo)
        if contrasena == "policia123":
            return redirect(url_for('index'))
        else:
            flash("Credenciales incorrectas. Intente nuevamente.")
            return redirect(url_for('login'))

    return render_template('login.html')

###########################################


############### PERSONA #################

@app.route('/ciudadanos')
def persona():
    personas = controlador_persona.obtener_personas()
    return render_template('persona.html', personas = personas)

@app.route('/agregar_ciudadano')
def formulario_agregar_persona():
    return render_template('agregar_persona.html')

@app.route('/guardar_ciudadano')
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
def formulario_editar_persona(id):
    persona = controlador_persona.obtener_persona_por_id(id)
    return render_template("editar_persona.html", persona=persona)


@app.route("/actualizar_persona", methods=["POST"])
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
def listar_persona():
    return redirect('ciudadanos')

@app.route("/historial")
def ver_historial():
    return redirect('ciudadanos')


############# FIN PERSONA ###############


############# DENUNCIA ####################

@app.route('/denuncia')
def denuncia():
    return render_template('denuncia.html')



######### FIN DENUNCIA #################



if __name__ == '__main__':
    app.run(debug=True, port=5000)
