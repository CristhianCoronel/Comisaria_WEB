from main import app, login_required
from flask import render_template, request, jsonify, redirect, url_for, flash, session, current_app
from controllers import controlador_denuncia, controlador_persona, controlador_tipo_denuncia
from models.Models import (
    Tipo_Denuncia, Denuncia, Persona, Usuario,
    Evidencia, Comisaria
)
from bd import bd
from datetime import datetime
from main import app, login_required
from services.transaction_manager import transaccion
from services.mediador_denuncia import registrar_denuncia_mediada

import os

@app.route("/denuncia")
@login_required
def denuncia():
    denuncias = Denuncia.query.order_by(Denuncia.fecha_registro.desc()).all()
    tipos_denuncias = controlador_tipo_denuncia.obtener_tipos_denuncia()        ## Tipo_Denuncia.query.all()
    return render_template("denuncia.html", denuncias=denuncias, tipos_denuncias=tipos_denuncias)

@app.route('/registrar_denuncia', methods=['GET'])
@login_required
def registrar_denuncia():
    tipos_denuncias = controlador_tipo_denuncia.obtener_tipos_denuncia()
    return render_template('registrar_denuncia.html', tipos_denuncias=tipos_denuncias)


@app.route("/guardar_denuncia", methods=["POST"])
@login_required
def guardar_denuncia():
    try:
        # Usuario logueado (efectivo que registra)
        usuario_actual = Usuario.query.filter_by(dni=session.get("dni")).first()
        if not usuario_actual:
            flash("No se pudo identificar al usuario de la sesión.", "danger")
            return redirect(url_for("registrar_denuncia"))

        # Usamos nuestro 'monitor de transacciones'
        with transaccion("registrar_denuncia"):
            denuncia = registrar_denuncia_mediada(request.form, request.files, usuario_actual.id_usuario)

        flash("Denuncia registrada correctamente.", "success")
        return redirect(url_for("denuncia"))

    except Exception as e:
        # Ya se hizo rollback dentro de transaccion()
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