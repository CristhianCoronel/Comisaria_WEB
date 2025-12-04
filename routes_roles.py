from flask import render_template, request, jsonify, redirect, url_for, flash, Response
from main import app, login_required  # usamos el mismo app y el mismo decorador
import json
from controllers import controlador_rol

@app.route("/roles")
@login_required
def rol():
    roles = controlador_rol.obtener_roles()
    return render_template("rol.html", roles=roles)

@app.route("/guardar_rol", methods=["POST"])
@login_required
def guardar_rol():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    area = request.form["area"]
    controlador_rol.guardar_rol(nombre, descripcion, area)
    return redirect("/roles")

@app.route("/actualizar_rol", methods=["POST"])
@login_required
def actualizar_rol():
    id_rol = request.form["id_rol"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    area = request.form["area"]
    controlador_rol.modificar_rol(id_rol, nombre, descripcion, area)
    return redirect("/roles")

# @app.route("/eliminar_rol/<int:id_rol>", methods=["POST"])
# @login_required
# def eliminar_rol(id_rol):
#     controlador_rol.eliminar_rol(id_rol)
#     return redirect("/roles")