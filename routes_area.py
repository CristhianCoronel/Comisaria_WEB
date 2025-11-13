from main import app, login_required
from flask import render_template, request, jsonify, redirect, url_for, flash
from controllers import controlador_area


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

@app.route('/api/area/<int:id_area>/json', methods=['GET'])
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
