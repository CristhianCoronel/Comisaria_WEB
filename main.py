from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from controllers import controlador_evidencia
from controllers import controlador_departamento
from models import Ubigeo

import os, json

app = Flask(__name__)

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


@app.route('/denuncia')
def denuncia():
    return render_template('denuncia.html')


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



if __name__ == '__main__':
    app.run(debug=True, port=5000)
