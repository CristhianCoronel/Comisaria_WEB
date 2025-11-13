# routes_persona.py
from flask import render_template, request, jsonify, redirect, url_for, flash, Response
from main import app, login_required  # usamos el mismo app y el mismo decorador
import json
from controllers import controlador_persona

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
        ape_paterno = data.get("ape_paterno")
        ape_materno = data.get("ape_materno")
        fecha_nacimiento = data.get("fecha_nacimiento")
        telefono = data.get("telefono")
        direccion = data.get("direccion")
        ubigeo = data.get("ubigeo")

        # --- Validaciones ---
        if not dni or not nombres or not ape_paterno:
            return jsonify({
                "status": 0,
                "data": None,
                "message": "Faltan campos obligatorios."
            }), 400

        # --- Insertar la nueva persona ---
        controlador_persona.insertar_persona(
            dni, nombres, ape_paterno, ape_materno, fecha_nacimiento, telefono, direccion, ubigeo
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
            "ape_paterno": persona.ape_paterno,
            "ape_materno": persona.ape_materno,
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
    ape_paterno = request.form["ape_paterno"]
    ape_materno = request.form["ape_materno"]
    fecha_nacimiento = request.form.get("fecha_nacimiento") or None  # puede venir vacío
    telefono = request.form.get("telefono") or None
    direccion = request.form.get("direccion") or None
    ubigeo = request.form.get("ubigeo") or None

    controlador_persona.insertar_persona(dni, nombres, ape_paterno, ape_materno, fecha_nacimiento, telefono, direccion)
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

        data = ({
            "status": 1,
            "data": {
                "id_persona": persona.id_persona,
                "dni": persona.dni,
                "nombres": persona.nombres,
                "ape_paterno": persona.ape_paterno,
                "ape_materno": persona.ape_materno,
                "fecha_nacimiento": persona.fecha_nacimiento,
                "telefono": persona.telefono,
                "direccion": persona.direccion
            }
        })
        return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json; charset=utf-8')
    except Exception as e:
        return jsonify({"status": -1, "data": None, "message": str(e)}), 500
    
@app.route('/persona_dni/<string:dni>/json', methods=['GET'])
@login_required
def persona_por_dni_json(dni):
    """Devuelve los datos de una persona en formato JSON dado su id."""
    print("API llamada para DNI:", repr(dni))
    try:
        persona = controlador_persona.obtener_persona_por_dni(dni)
        if not persona:
            return jsonify({"status": 0, "data": None, "message": "Persona no encontrada"}), 404
        return jsonify({
            "status": 1,
            "data": {
                "id_persona": persona.id_persona,
                "dni": persona.dni,
                "nombres": persona.nombres,
                "ape_paterno": persona.ape_paterno,
                "ape_materno": persona.ape_materno,
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