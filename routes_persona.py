# routes_persona.py
from flask import render_template, request, session, jsonify, redirect, url_for, flash, Response, flash
from main import app, login_required  # usamos el mismo app y el mismo decorador
import json
from controllers import controlador_persona, controlador_usuario, controlador_comisaria, controlador_rol, controlador_rango
from services.reniec_service import consultar_dni_faciliza
from models.Models import Persona, Usuario
from main import FACILIZA_TOKEN, FACILIZA_URL
import requests

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

@app.route('/perfil')
@login_required
def perfil():
    dni_usuario = session.get('dni')
    usuario = controlador_usuario.obtener_usuario_por_dni(dni_usuario)
    print("DEBUG usuario:", usuario)
    print("DEBUG comisaria:", usuario.comisaria if usuario else None)
    return render_template('perfil.html', usuario=usuario)


@app.route('/ciudadanos')
@login_required
def persona():
    personas = controlador_persona.obtener_personas()
    tipos_documentos = controlador_persona.obtener_tipos_documentos()
    return render_template('persona.html', personas=personas, tipos_documentos=tipos_documentos)


@app.route('/ciudadano/registrar', methods=["POST"])
@login_required
def guardar_persona():
    try:
        dni = request.form["dni"]
        if controlador_persona.duplicado_dni(dni):
            flash("DNI Duplicado. No es posible el registro", "success")
            return redirect("/ciudadanos")
        
        nombres = request.form["nombres"]
        ape_paterno = request.form["ape_paterno"]
        ape_materno = request.form["ape_materno"]
        estado_civil = request.form["estado_civil"]
        ocupacion = request.form["ocupacion"]
        fecha_nacimiento = request.form.get("fecha_nacimiento") or None
        telefono = request.form.get("telefono") or None
        direccion = request.form.get("direccion") or None
        ubigeo = request.form.get("ubigeo") or None

        if controlador_persona.insertar_persona(
            dni, nombres, ape_paterno, ape_materno, estado_civil, ocupacion,
            fecha_nacimiento, telefono, direccion, ubigeo
        ):
            flash("Persona registrada correctamente.", "success")
            return redirect("/ciudadanos")
        flash("Error al registrar.", "danger")
        return redirect("/ciudadanos")
    except Exception as e:
        flash(f"Error al registrar persona: {str(e)}", "danger")
        return redirect("/ciudadanos")
    

@app.route("/ciudadano/actualizar", methods=["POST"])
@login_required
def actualizar_persona():
    try:
        id_persona = request.form["id_persona"]
        dni = request.form["dni"]
        nombres = request.form["nombres"]
        ape_paterno = request.form["ape_paterno"]
        ape_materno = request.form["ape_materno"]
        estado_civil = request.form["estado_civil"]
        ocupacion = request.form["ocupacion"]
        fecha_nacimiento = request.form.get("fecha_nacimiento") or None
        telefono = request.form.get("telefono") or None
        direccion = request.form.get("direccion") or None
        ubigeo = request.form.get("ubigeo") or None

        if controlador_persona.actualizar_persona(id_persona,
            dni, nombres, ape_paterno, ape_materno, estado_civil, ocupacion,
            fecha_nacimiento, telefono, direccion, ubigeo):

            flash("Persona actualizada correctamente.", "success")
            return redirect("/ciudadanos")
        
        flash("Error al actualizar.", "danger")
        return redirect("/ciudadanos")

    except Exception as e:
        flash(f"Error al actualizar persona: {str(e)}", "danger")
        return redirect("/ciudadanos")


@app.route("/ciudadano/buscar/<string:nombre>/<string:dni>", methods=["GET"])
@login_required
def buscar_persona(nombre,dni):
    try:
        if (nombre == "_" and dni == "_"):
            return redirect('/ciudadanos')
        
        lista = controlador_persona.obtener_persona_nombre_dni(nombre, dni)
        return render_template('persona.html', personas=lista)
        
    except Exception as e:
        flash(f"Error al filtrar las personas: {str(e)}", "danger")
        return redirect("/ciudadanos")

@app.route('/persona/<int:id_persona>/json', methods=['GET'])
@login_required
def persona_por_id_json(id_persona):
    try:
        persona = controlador_persona.obtener_persona_por_id(id_persona)
        if not persona:
            return jsonify({"status": 0, "data": None, "message": "Persona no encontrada"}), 404
        
        if persona.fecha_nacimiento: 
            fecha_nac = persona.fecha_nacimiento.strftime("%Y-%m-%d")
        else:
            fecha_nac = None
            print(fecha_nac)
        
        data = ({
            "status": 1,
            "data": {
                "id_persona": persona.id_persona,
                "dni": persona.dni,
                "nombres": persona.nombres,
                "ape_paterno": persona.ape_paterno,
                "ape_materno": persona.ape_materno,
                "fecha_nacimiento": fecha_nac,
                "telefono": persona.telefono,
                "direccion": persona.direccion,
                "ubigeo": persona.ubigeo,
                "ocupacion" : persona.ocupacion,
                "estado_civil" :persona.estado_civil
            },
            "message": "Persona encontrada"
        })
        return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json; charset=utf-8')
    except Exception as e:
        return jsonify({"status": -1, "data": None, "message": str(e)}), 500
    
@app.route('/persona_dni/<string:dni>/json', methods=['GET'])
@login_required
def persona_por_dni_json(dni):
    try:
        # 1) Buscar primero en tu BD local
        persona = controlador_persona.obtener_persona_por_documento(1,dni)
    
        if persona:
            
            return jsonify({
                "status": 1,
                "data": {
                    # Datos básicos (DNI se mapea a 'documento' y Nombre a 'nombre' de la tabla)
                    "dni": persona.documento,
                    "nombres": persona.nombre,
                    "ape_paterno": persona.ape_paterno,
                    "ape_materno": persona.ape_materno,
                    
                    # Nuevos campos requeridos
                    "fecha_nacimiento": (
                        str(persona.fecha_nacimiento)
                        if persona.fecha_nacimiento else None
                    ),
                    "estado_civil": persona.estado_civil,
                    "ocupacion": persona.ocupacion,
                    
                    # Campos de Contacto y Dirección
                    "telefono": persona.telefono,
                    "correo": persona.correo,
                    "direccion": persona.direccion,
                },
                "source": "db",
            })
        
        # 2) Si no existe en la BD, consultamos FACILIZA
        if not FACILIZA_TOKEN or not FACILIZA_URL:
            print("API del estado no configurado")
            return jsonify({
                "status": 0,
                "data": None,
                "message": "FACILIZA_TOKEN o FACILIZA_URL no configurados",
            }), 500
        print("Ok, si está configurado")
        # Asegurarnos de que no se dupliquen las barras
        url = f"{FACILIZA_URL.rstrip('/')}/{dni}"
        
        print("URL consultada:", f"{FACILIZA_URL}/{dni}")
        print("Token usado (primeros 10 chars):", (FACILIZA_TOKEN or "")[:10])

        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {FACILIZA_TOKEN}"},
            timeout=5,
        )
        print("Llegamos hasta aquí")
        if resp.status_code != 200:
            return jsonify({
                "status": 0,
                "data": None,
                "message": f"Error al consultar FACILIZA (HTTP {resp.status_code})",
            }), 400
        print("Pasamos el otro error")
        body = resp.json()

        if not body.get("success"):
            return jsonify({
                "status": 0,
                "data": None,
                "message": body.get("message", "DNI no encontrado en FACILIZA"),
            }), 404
        print("Encontramos el dni")
        info = body.get("data", {})

        # Normalizamos lo que devuelve FACILIZA para tu front
        data = {
            "dni": info.get("numero"),
            "nombres": info.get("nombres", ""),
            "ape_paterno": info.get("apellido_paterno", ""),
            "ape_materno": info.get("apellido_materno", ""),
            "direccion": info.get("direccion_completa", ""),
        }
        print("Data registrada")
        return jsonify({
            "status": 1,
            "data": data,
            "source": "faciliza",
        })

    except Exception as e:
        print("Error en persona_por_dni_json:", e)
        return jsonify({
            "status": 0,
            "data": None,
            "message": "Error interno en el servidor",
        }), 500

###########################
###########################


@app.route("/personal")
@login_required
def usuario():
    usuarios = controlador_usuario.obtener_usuarios()
    roles = controlador_rol.obtener_roles()
    rangos = controlador_rango.obtener_rangos()
    comisarias = controlador_comisaria.obtener_comisarias()    
    return render_template("usuario.html", usuarios=usuarios, roles=roles, rangos=rangos, comisarias=comisarias)

@app.route("/personal/registrar", methods=["POST"])
@login_required
def guardar_usuario():
    try:
        dni = request.form["dni"]
        if controlador_usuario.duplicado_dni(dni):
            flash("DNI Duplicado. No es posible el registro", "success")
            return redirect("/personal")
        
        codigo_usuario = request.form["codigo_usuario"]
        dni = request.form["dni"]
        nombres = request.form["nombres"]
        ape_paterno = request.form["ape_paterno"]
        ape_materno = request.form["ape_materno"]
        estado = request.form["estado"]
        id_rol = request.form["id_rol"]
        id_rango = request.form["id_rango"]
        id_comisaria = request.form["id_comisaria"]
        tipo_usuario = request.form["tipo_usuario"]
        
        hash_codigo = bcrypt.generate_password_hash(codigo_usuario).decode('utf-8')
        if controlador_usuario.insertar_usuario(
            dni, nombres, ape_paterno, ape_materno, hash_codigo, 
            estado, id_comisaria, id_rango, id_rol, tipo_usuario):
            flash("Personal registrado correctamente.", "success")
            return redirect("/personal")
        print("Retorno falso")
        flash("Error al registrar.", "danger")
        return redirect("/personal")
    except Exception as e:
        flash(f"Error al registrar personal: {str(e)}", "danger")
        return redirect("/personal")

@app.route("/personal/actualizar", methods=["POST"])
@login_required
def actualizar_usuario():
    try:
        id_usuario = request.form["id_usuario"]
        dni = request.form["dni"]
        nombres = request.form["nombres"]
        ape_paterno = request.form["ape_paterno"]
        ape_materno = request.form["ape_materno"]
        estado = request.form["estado"]
        id_rol = request.form["id_rol"]
        id_rango = request.form["id_rango"]
        id_comisaria = request.form["id_comisaria"]
        tipo_usuario = request.form["tipo_usuario"]
        # new_codigo = bcrypt.generate_password_hash(codigo_usuario).decode('utf-8')
        
        if controlador_usuario.modificar_usuario(id_usuario,
            dni, nombres, ape_paterno, ape_materno,
            estado, id_comisaria, id_rango, id_rol, tipo_usuario):
            flash("Personal actualizado correctamente.", "success")
            return redirect("/personal")
        flash("Error al actualizar.", "danger")
        return redirect("/personal")
    except Exception as e:
        flash(f"Error al actualizar personal: {str(e)}", "danger")
        return redirect("/personal")

@app.route("/personal/buscar/<string:nombre>/<string:dni>", methods=["GET"])
@login_required
def buscar_usuario(nombre,dni):
    try:
        if (nombre == "_" and dni == "_"):
            return redirect('/personal')
        
        lista = controlador_usuario.obtener_persona_nombre_dni(nombre, dni)
        
        roles = controlador_rol.obtener_roles()
        rangos = controlador_rango.obtener_rangos()
        comisarias = controlador_comisaria.obtener_comisarias() 
        return render_template('usuario.html', usuarios=lista, roles=roles, rangos=rangos, comisarias=comisarias)
        
    except Exception as e:
        flash(f"Error al filtrar las personas: {str(e)}", "danger")
        return redirect("/personal")


@app.route('/personal/<int:id_usuario>/json', methods=['GET'])
@login_required
def usuario_por_id_json(id_usuario):
    try:
        persona = controlador_usuario.obtener_usuario_por_id(id_usuario)
        if not persona:
            return jsonify({"status": 0, "data": None, "message": "Personal no encontrado"}), 404
        
        data = ({
            "status": 1,
            "data": {
                "id_usuario": persona.id_usuario,
                "dni": persona.dni,
                "codio_usuario": persona.codigo_usuario,
                "ape_paterno": persona.ape_paterno,
                "ape_materno": persona.ape_materno,
                "nombres": persona.nombres,
                "id_comisaria": persona.id_comisaria,
                "tipo_usuario": persona.tipo_usuario,
                "estado": persona.estado,
                "id_rango" : persona.id_rango,
                "id_rol" :persona.id_rol
            },
            "message": "Personal encontrado"
        })
        return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json; charset=utf-8')
    except Exception as e:
        return jsonify({"status": -1, "data": None, "message": str(e)}), 500


@app.route("/usuario/codigo/<int:id_usuario>", methods=["POST"])
@login_required
def actualizar_codigo_usuario(id_usuario):
    try:
        codigo_usuario = request.form.get("code")
        
        if not codigo_usuario or codigo_usuario.strip() == "":
            flash(f"Campo vacío. No se pudo cambiar el codigo", "danger")
            return redirect("/personal")
        
        new_codigo = bcrypt.generate_password_hash(codigo_usuario).decode('utf-8')
        estado = controlador_usuario.cambiar_codigo_usuario(id_usuario, new_codigo)


        if not estado:
            flash(f"Error al cambiar el código", "danger")
            return redirect("/personal")

        flash(f"Codigo cambiado correctamente", "success")
        return redirect("/personal")

    except Exception as e:
        flash(f"Error al cambiar el código {str(e)}", "danger")
        return redirect("/personal")



@app.route("/historial")
@login_required
def ver_historial():
    return redirect('ciudadanos')


############# FIN PERSONA ###############