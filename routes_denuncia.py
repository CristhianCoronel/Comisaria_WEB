from main import app, login_required
from flask import render_template, request, jsonify, redirect, url_for, flash
from controllers import controlador_denuncia, controlador_persona
from models.Tipo_Denuncia import Tipo_Denuncia
from models.Denuncia import Denuncia


@app.route('/denuncia')
@login_required
def denuncia():
    denuncias = controlador_denuncia.obtener_denuncias()
    tipos_denuncias = Tipo_Denuncia.query.all()
    return render_template('denuncia.html', denuncias = denuncias, tipos_denuncias = tipos_denuncias)

@app.route('/registrar_denuncia')
@login_required
def registrar_denuncia():
    tipos_denuncias = Tipo_Denuncia.query.all()
    
    return render_template('registrar_denuncia.html', tipos_denuncias = tipos_denuncias)

@app.route('/guardar_denuncia', methods=['POST'])
@login_required
def guardar_denuncia():
    ## Datos denuncia
    dni_denunciante =  request.form['dni_denunciante']
    desnunciante = controlador_persona.obtener_persona_por_dni(dni_denunciante)
    id_persona_denunciante = desnunciante.id_persona if desnunciante else None
    id_tipo_denuncia = request.form['tipo_denuncia']
    descripcion = request.form['descripcion']
    fecha_hechos = request.form['fecha_hechos']
    hora_hechos = request.form['hora_hechos']
    direccion_hechos = request.form['direccion_hechos']
    
    ## Datos tipo denuncia
    
    ## Datos sospechoso
    
    ## Datos bienes
    
    ## Datos evidencia
    
    ## Procesar  toda la información
    

    datos = request.form.to_dict()
    
    controlador_denuncia.insertar_denuncia(datos)
    flash("Denuncia registrada correctamente.", "success")
    return redirect(url_for('denuncia'))
