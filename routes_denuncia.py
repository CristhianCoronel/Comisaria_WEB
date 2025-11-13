from main import app, login_required
from flask import render_template, request, jsonify, redirect, url_for, flash, session, current_app
from controllers import controlador_denuncia, controlador_persona
from models.Tipo_Denuncia import Tipo_Denuncia
from models.Denuncia import Denuncia
from models.Persona import Persona
from models.Usuario import Usuario
from models.Evidencia import Evidencia
from bd import bd
from datetime import datetime
from main import app, login_required

import os

@app.route("/denuncia")
@login_required
def denuncia():
    denuncias = Denuncia.query.order_by(Denuncia.fecha_registro.desc()).all()
    tipos_denuncias = Tipo_Denuncia.query.all()
    return render_template("denuncia.html", denuncias=denuncias, tipos_denuncias=tipos_denuncias)

@app.route('/registrar_denuncia', methods=['GET'])
@login_required
def registrar_denuncia():
    tipos_denuncias = Tipo_Denuncia.query.order_by(Tipo_Denuncia.tipo_denuncia).all()
    return render_template('registrar_denuncia.html', tipos_denuncias=tipos_denuncias)


@app.route("/guardar_denuncia", methods=["POST"])
@login_required
def guardar_denuncia():
    try:
        # ---------- 1. DATOS DEL DENUNCIANTE ----------
        dni = request.form["dni"].strip()
        nombre_completo = request.form["nombres"].strip()  # solo para mostrar, pero en BD guardamos nombres por separado
        nombres = request.form.get("nombres").strip()      # si quieres, podrías guardar solo la parte nombres de RENIEC
        ape_paterno = request.form.get("ape_paterno") or ""
        ape_materno = request.form.get("ape_materno") or ""
        telefono = request.form.get("telefono") or None
        estado_civil = request.form.get("estado_civil") or "SOLTERO"
        direccion_denunciante = request.form.get("direccion_denunciante") or None
        correo = request.form.get("correo") or None  # si tienes columna correo en el modelo

        # Buscar persona por DNI
        persona = Persona.query.filter_by(dni=dni).first()

        if not persona:
            persona = Persona(
                dni=dni,
                nombres=nombres,            # 🔹 nombres tal como venga de RENIEC o del input
                ape_paterno=ape_paterno,    # 🔹 YA NO ES None
                ape_materno=ape_materno,    # 🔹 YA NO ES None
                telefono=telefono,
                direccion=direccion_denunciante,
                estado_civil=estado_civil,
                correo=correo,
                ubigeo=None,
            )
            bd.session.add(persona)
            bd.session.flush()
        else:
            persona.nombres = nombres
            if ape_paterno:
                persona.ape_paterno = ape_paterno
            if ape_materno:
                persona.ape_materno = ape_materno
            persona.telefono = telefono
            persona.direccion = direccion_denunciante
            persona.estado_civil = estado_civil
            persona.correo = correo

        # ---------- 2. DETALLES DE LA DENUNCIA ----------
        id_tipo_denuncia = int(request.form["id_tipo_denuncia"])
        fecha_hechos_str = request.form["fecha_hechos"]
        hora_hechos_str = request.form["hora_hechos"]
        direccion_hechos = request.form["direccion_hechos"].strip()
        descripcion_hechos = request.form["descripcion_hechos"].strip()
        modalidad = request.form.get("modalidad") or None
        condicion = request.form.get("condicion") or None

        # fecha_acto es DATE en el modelo
        fecha_acto = datetime.strptime(fecha_hechos_str, "%Y-%m-%d").date()

        # En el modelo no hay campo hora, modalidad ni condición → los metemos en la descripción
        descripcion = descripcion_hechos
        extras = []
        if hora_hechos_str:
            extras.append(f"Hora de los hechos: {hora_hechos_str}.")
        if modalidad:
            extras.append(f"Modalidad: {modalidad}.")
        if condicion:
            extras.append(f"Condición: {condicion}.")
        if extras:
            descripcion += "\n\n" + " ".join(extras)

        # ---------- 3. USUARIO QUE REGISTRA ----------
        usuario_actual = Usuario.query.filter_by(dni=session.get("dni")).first()
        if not usuario_actual:
            raise Exception("Usuario de sesión no encontrado para registrar la denuncia.")

        # ---------- 4. CREAR DENUNCIA (MAPPING CORRECTO) ----------
        denuncia = Denuncia(
            fecha_acto=fecha_acto,
            lugar_hechos=direccion_hechos,
            descripcion=descripcion,
            estado="P",                            # Pendiente
            id_denunciante=persona.id_persona,     # 🔹 AQUÍ VA id_denunciante
            id_denunciado=None,                    # Por ahora vacío
            id_usuario=usuario_actual.id_usuario,  # quién registró
            id_tipo_denuncia=id_tipo_denuncia,
            ubigeo=None,
        )

        bd.session.add(denuncia)
        bd.session.flush()  # para tener denuncia.id_denuncia

        # ---------- 5. EVIDENCIAS (si ya las tienes del form) ----------
        tipos_ev = request.form.getlist("evidencia_tipo[]")
        descs_ev = request.form.getlist("evidencia_descripcion[]")
        archivos_ev = request.files.getlist("evidencia_archivo[]")

        for tipo_ev, desc_ev, archivo_ev in zip(tipos_ev, descs_ev, archivos_ev):
            if not archivo_ev or not archivo_ev.filename:
                continue

            # Aquí podrías guardar el archivo en disco y almacenar la ruta
            evidencia = Evidencia(
                id_denuncia=denuncia.id_denuncia,
                tipo=tipo_ev,
                descripcion=desc_ev,
                nombre_archivo=archivo_ev.filename,
                ruta_archivo=f"/uploads/{archivo_ev.filename}",
            )
            bd.session.add(evidencia)

        # ---------- 6. GUARDAR EN BD ----------
        bd.session.commit()
        flash("Denuncia registrada correctamente.", "success")
        return redirect(url_for("denuncia"))

    except Exception as e:
        bd.session.rollback()
        current_app.logger.error(f"Error al registrar denuncia: {e}")
        flash("Ocurrió un error al registrar la denuncia.", "danger")
        return redirect(url_for("registrar_denuncia"))


@app.route('/denuncia/<int:id>/editar')
@login_required
def editar_denuncia(id):
    """
    Ruta temporal para evitar el BuildError.
    Más adelante aquí cargaremos el formulario para editar la denuncia.
    """
    flash("La edición de denuncias aún no está implementada.", "info")
    return redirect(url_for('denuncia'))

@app.route("/denuncia/<int:id>/ver")
@login_required
def ver_denuncia(id):
    # 1) Obtenemos la denuncia
    denuncia = Denuncia.query.get_or_404(id)

    # 2) Denunciante (gracias a la relación ya definida en el modelo)
    denunciante = denuncia.denunciante

    # 3) Usuario que registró la denuncia
    usuario = denuncia.usuario  # por la relationship en el modelo Denuncia

    # 4) Comisaría (según cómo tengas el modelo Usuario)
    comisaria = None
    try:
        # si hay relación usuario.comisaria la usamos
        comisaria = usuario.comisaria
    except Exception:
        # si no, buscamos por id_comisaria
        if hasattr(usuario, "id_comisaria") and usuario.id_comisaria:
            comisaria = Comisaria.query.get(usuario.id_comisaria)

    # 5) Evidencias asociadas
    evidencias = Evidencia.query.filter_by(id_denuncia=denuncia.id_denuncia).all()

    return render_template(
        "denuncia_detalle.html",
        denuncia=denuncia,
        denunciante=denunciante,
        usuario=usuario,
        comisaria=comisaria,
        evidencias=evidencias
    )