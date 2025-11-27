from main import app, login_required
from flask import render_template, request, jsonify, redirect, url_for, flash, Response
from controllers import controlador_comisaria, controlador_ubigeo
from models.Comisaria import Comisaria
import json

# Listar comisarías
@app.route('/comisarias', methods=['GET'])
@login_required
def comisaria():
    comisarias = controlador_comisaria.obtener_comisarias()
    return render_template('comisaria.html', comisarias=comisarias, ubigeos=controlador_ubigeo.obtener_ubigeos())

@app.route('/comisaria/registrar', methods=['POST'])
@login_required
def guardar_comisaria():
    try:
        nombre = request.form.get('nombre', '')
        direccion = request.form.get('direccion', '')
        telefono = request.form.get('telefono', '')
        ubigeo = request.form.get('ubigeo', '')
        if controlador_comisaria.insertar_comisaria(nombre, direccion, ubigeo, telefono):
            flash("Comisaria registrada correctamente.", "success")
            return redirect("/comisarias")
        flash("Error al registrar.", "danger")
        return redirect("/comisarias")
    except Exception as e:
        flash(f"Error al registrar comisaria: {str(e)}", "danger")
        return redirect("/comisarias")
        
@app.route('/comisaria/actualizar', methods=['POST'])
@login_required
def actualizar_comisaria():
    try:
        id_comisaria = request.form.get('id_comisaria', '')
        nombre = request.form.get('nombre', '')
        direccion = request.form.get('direccion', '')
        telefono = request.form.get('telefono', '')
        ubigeo = request.form.get('ubigeo', '')
        if controlador_comisaria.modificar_comisaria(id_comisaria, nombre, direccion, ubigeo, telefono):
            flash("Comisaria actualizada correctamente.", "success")
            return redirect("/comisarias")
        
        flash("Error al actualizar.", "danger")
        return redirect("/comisarias")

    except Exception as e:
        flash(f"Error al actualizar comisaria: {str(e)}", "danger")
        return redirect("/comisarias")


@app.route("/comisaria/buscar/<string:nombre>/<string:ubigeo>", methods=["GET"])
@login_required
def buscar_comisaria(nombre, ubigeo):
    try:
        if nombre == "_" and ubigeo == "_":
            return redirect('/comisarias')
        
        lista = controlador_comisaria.obtener_comisaria_nombre_ubigeo(nombre, ubigeo)
        ubigeos=controlador_ubigeo.obtener_ubigeos()
        
        return render_template('comisaria.html', comisarias=lista, ubigeos=ubigeos)
    
    except Exception as e:
        flash(f"Error al filtrar las comisarías: {str(e)}", "danger")
        return redirect("/comisarias")


@app.route('/comisaria/<int:id_comisaria>/json', methods=['GET'])
@login_required
def api_obtener_comisaria(id_comisaria):
    try:
        comisaria = controlador_comisaria.obtener_comisaria_por_id(id_comisaria)
        if not comisaria:
            return jsonify({"status": 0, "data": None, "message": "Persona no encontrada"}), 404
        
        data = ({
            "status": 1,
            "data": {
                "id_comisaria": comisaria.id_comisaria,
                "nombre": comisaria.nombre,
                "direccion": comisaria.direccion,
                "telefono": comisaria.telefono,
                "ubigeo": comisaria.ubigeo
            },
            "message": "Comisaría encontrada"
        })
        return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json; charset=utf-8')
    except Exception as e:
        return jsonify({"status": -1, "data": None, "message": str(e)}), 500




