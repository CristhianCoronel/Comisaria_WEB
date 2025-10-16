from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,Response 
from controllers import controlador_evidencia
from models import Evidencia

import os, json

app = Flask(__name__)

#---RUTAS FIJAS---#

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')







# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8000, debug=True)

if __name__ ==  '__main__':
    app.run(debug=5000)