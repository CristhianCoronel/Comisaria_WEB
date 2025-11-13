# services/mediador_denuncia.py

from datetime import datetime
from bd import bd
from models.Persona import Persona
from models.Denuncia import Denuncia
from models.Evidencia import Evidencia

def _normalizar_nombres(nombre_completo: str):
    partes = nombre_completo.strip().split()
    if len(partes) >= 3:
        # Ej: ORLIN WILLIAM ISHUIZA VILCHERREZ -> muy variable
        # Tomamos lo último como ape_materno, lo penúltimo ape_paterno
        ape_materno = partes[-1]
        ape_paterno = partes[-2]
        nombres = " ".join(partes[:-2])
    elif len(partes) == 2:
        nombres = partes[0]
        ape_paterno = partes[1]
        ape_materno = "NO ESPECIFICADO"
    else:
        nombres = nombre_completo
        ape_paterno = "NO ESPECIFICADO"
        ape_materno = "NO ESPECIFICADO"

    return nombres, ape_paterno, ape_materno


def registrar_denuncia_mediada(form, files, usuario_actual):
    # ---------- 1. DATOS DEL DENUNCIANTE ----------
    dni = form["dni"].strip()
    nombre_completo = form["nombres"].strip()
    telefono = form.get("telefono") or None
    estado_civil = form.get("estado_civil") or "SOLTERO"
    direccion_denunciante = form.get("direccion_denunciante") or None

    # Buscamos si ya existe la persona
    persona = Persona.query.filter_by(dni=dni).first()

    if not persona:
        # Intentamos separar nombres y apellidos de 'nombre_completo'
        nombres, ape_paterno, ape_materno = _normalizar_nombres(nombre_completo)

        persona = Persona(
            dni=dni,
            nombres=nombres,
            ape_paterno=ape_paterno,
            ape_materno=ape_materno,
            estado_civil=estado_civil,
            ocupacion="NO ESPECIFICADA",  # campo NOT NULL en la BD
            telefono=telefono,
            direccion=direccion_denunciante,
            ubigeo=None
        )
        bd.session.add(persona)
        bd.session.flush()  # para tener persona.id_persona
    else:
        # Actualizamos algunos campos si se enviaron
        if telefono:
            persona.telefono = telefono
        if direccion_denunciante:
            persona.direccion = direccion_denunciante
        if estado_civil:
            persona.estado_civil = estado_civil

    # ---------- 2. DETALLES DE LA DENUNCIA ----------
    id_tipo_denuncia = int(form["id_tipo_denuncia"])
    fecha_hechos_str = form["fecha_hechos"]
    hora_hechos_str = form["hora_hechos"]
    direccion_hechos = form["direccion_hechos"].strip()
    descripcion_hechos = form["descripcion_hechos"].strip()
    modalidad = form.get("modalidad") or None
    condicion = form.get("condicion") or None

    # Convertimos fecha (DATE)
    fecha_acto = datetime.strptime(fecha_hechos_str, "%Y-%m-%d").date()

    # Construimos una descripción extendida con datos extra
    descripcion = descripcion_hechos
    extras = []
    if hora_hechos_str:
        extras.append(f"Hora de los hechos: {hora_hechos_str}.")
    if modalidad:
        extras.append(f"Modalidad de denuncia: {modalidad}.")
    if condicion:
        extras.append(f"Condición de la denuncia: {condicion}.")
    if extras:
        descripcion += "\n\n" + " ".join(extras)

    # ---------- 3. CREAR DENUNCIA ----------
    denuncia = Denuncia(
        fecha_acto=fecha_acto,
        lugar_hechos=direccion_hechos,
        descripcion=descripcion,
        estado="P",                            # Pendiente
        id_denunciante=persona.id_persona,
        id_denunciado=None,                    # por ahora no lo usamos
        id_usuario=usuario_actual.id_usuario,  # efectivo que registra
        id_tipo_denuncia=id_tipo_denuncia,
        ubigeo=None
    )

    bd.session.add(denuncia)
    bd.session.flush()  # necesitamos denuncia.id_denuncia para evidencias

    # ---------- 4. EVIDENCIAS ----------
    tipos_ev = form.getlist("evidencia_tipo[]")
    descs_ev = form.getlist("evidencia_descripcion[]")
    archivos_ev = files.getlist("evidencia_archivo[]")

    for tipo_ev, desc_ev, archivo_ev in zip(tipos_ev, descs_ev, archivos_ev):
        if not archivo_ev or not archivo_ev.filename:
            continue

        # Aquí podrías guardar el archivo en disco y usar esa ruta
        ruta_archivo = f"/uploads/{archivo_ev.filename}"

        evidencia = Evidencia(
            id_denuncia=denuncia.id_denuncia,
            tipo=tipo_ev,
            descripcion=desc_ev or None,
            url_archivo=ruta_archivo
        )
        bd.session.add(evidencia)
        # Si quisieras guardar realmente el archivo, aquí va el save()

    # devolvemos la denuncia por si la quieres usar
    return denuncia
