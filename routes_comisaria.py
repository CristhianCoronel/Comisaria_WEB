from main import app, login_required
from flask import render_template, request, jsonify, redirect, url_for, flash
from controllers import controlador_comisaria, controlador_ubigeo
from models.Comisaria import Comisaria

# Listar comisarías
@app.route('/comisaria', methods=['GET'])
@login_required
def comisaria():
    comisarias = controlador_comisaria.obtener_comisarias()
    return render_template('comisaria.html', comisarias=comisarias, ubigeos=controlador_ubigeo.obtener_ubigeos())

@app.route('/api/comisaria', methods=['POST'])
@login_required
def api_agregar_comisaria():
    try:
        nombre = request.args.get('nombre', '')
        direccion = request.args.get('direccion', '')
        telefono = request.args.get('telefono', '')
        ubigeo = request.args.get('ubigeo', '')
        controlador_comisaria.insertar_comisaria(nombre, direccion, ubigeo, telefono)
        return jsonify({
            "status": 1,
            "data": [],
            "message": "Comisaría agregada correctamente"
        })
    except Exception as e:
        return jsonify({
            "status": 0,
            "data": [],
            "message": f"Error al agregar comisaría: {str(e)}"
        })
        
@app.route('/api/comisaria/actualizar', methods=['POST'])
@login_required
def api_actualizar_comisaria():
    try:
        id_comisaria = request.args.get('id_comisaria', '')
        nombre = request.args.get('nombre', '')
        direccion = request.args.get('direccion', '')
        telefono = request.args.get('telefono', '')
        ubigeo = request.args.get('ubigeo', '')
        controlador_comisaria.modificar_comisaria(id_comisaria, nombre, direccion, ubigeo, telefono)
        return jsonify({
            "status": 1,
            "data": [],
            "message": "Comisaría actualizada correctamente"
        })
    except Exception as e:
        return jsonify({
            "status": 0,
            "data": [],
            "message": f"Error al actualizar comisaría: {str(e)}"
        })

@app.route('/api/comisaria/<int:id_comisaria>', methods=['GET'])
@login_required
def api_obtener_comisaria(id_comisaria):
    try:
        comisaria = controlador_comisaria.obtener_comisaria_por_id(id_comisaria)
        if comisaria:
            return jsonify({
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
        else:
            return jsonify({
                "status": 0,
                "data": [],
                "message": "Comisaría no encontrada"
            })
    except Exception as e:
        return jsonify({
            "status": 0,
            "data": [],
            "message": f"Error al obtener comisaría: {str(e)}"
        })

# @app.route('/agregar_comisaria')
# @login_required
# def formulario_agregar_comisaria():
#     return render_template('comisaria.html', comisaria=None, ubigeos=controlador_ubigeo.obtener_ubigeos())

# @app.route('/guardar_comisaria', methods=['POST'])
# @login_required
# def guardar_comisaria():
#     nombre = request.form['nombre']
#     direccion = request.form['direccion']
#     telefono = request.form['telefono']
#     ubigeo = request.form['ubigeo']
#     controlador_comisaria.insertar_comisaria(nombre, direccion, ubigeo, telefono)
#     return redirect(url_for('comisaria'))

# @app.route('/formulario_editar_comisaria/<int:id_comisaria>')
# @login_required
# def formulario_editar_comisaria(id_comisaria):
#     comisaria = controlador_comisaria.obtener_comisaria_por_id(id_comisaria)
#     return render_template('comisaria.html', comisaria=comisaria, ubigeos=controlador_ubigeo.obtener_ubigeos())

# @app.route('/actualizar_comisaria', methods=['POST'])
# @login_required
# def actualizar_comisaria():
#     id_comisaria = request.form['id_comisaria']
#     nombre = request.form['nombre']
#     direccion = request.form.get('direccion', '')
#     telefono = request.form.get('telefono', '')
#     ubigeo = request.form.get('ubigeo', '')
#     controlador_comisaria.modificar_comisaria(id_comisaria, nombre, direccion, ubigeo, telefono)
#     return redirect(url_for('comisaria'))

# @app.route('/eliminar_comisaria', methods=['POST'])
# @login_required
# def eliminar_comisaria():
#     id_comisaria = request.form['id_comisaria']
#     controlador_comisaria.eliminar_comisaria(id_comisaria)
#     return redirect(url_for('comisaria'))

# @app.route('/buscar_comisaria', methods=['POST'])
# @login_required
# def buscar_comisaria():
#     nombre = request.form.get("b_nombre", "")
#     direccion = request.form.get("b_direccion", "")
#     lista = controlador_comisaria.obtener_comisaria_nombre_direccion(nombre, direccion)
#     return jsonify({
#         "status": 1,
#         "data": [{"id_comisaria": c.id_comisaria, "nombre": c.nombre, "direccion": c.direccion, "telefono": c.telefono, "ubigeo": c.ubigeo} for c in lista],
#         "message": "Comisarías encontradas"
#     })


