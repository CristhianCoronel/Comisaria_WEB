from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,Response 
from controllers import controlador_evidencia
from controllers import controlador_departamento
from models import Ubigeo

import os, json

app = Flask(__name__)

#---RUTAS FIJAS---#


@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/')
@app.route('/index')
def index():
    departamentos = list()
    departamentos = controlador_departamento.obtener_departamentos()
    return render_template('index.html', departamentos = departamentos)




# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8000, debug=True)

if __name__ ==  '__main__':
    app.run(debug=5000)