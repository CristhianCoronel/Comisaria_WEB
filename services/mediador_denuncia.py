import os
from datetime import date
from flask import current_app
from bd import bd
from models.Models import (
    Denuncia, D_Delito_Patrimonio, D_Violencia_Domestica, D_Extorsion,
    Detalle_Bienes, Bienes, Detalle_Sospechoso,
    Arma, Tipo_Arma, Evidencia,
    Persona, Tipo_Documento, Distrito,
    Estado_Denuncia, Seguimiento_Denuncia
)

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

def registrar_denuncia_mediada(data, files, id_usuario):
    """
    data  = request.form
    files = request.files
    id_usuario = usuario en sesión
    """
    try:
        with bd.session.begin():  

            # --------------------------------------------------------
            # 1. Buscar o registrar denunciante
            # --------------------------------------------------------
            documento = data.get("dni")
            denunciante = Persona.query.filter_by(documento=documento).first()

            if not denunciante:
                denunciante = Persona(
                    id_tipo_documento=1,                    # DNI
                    documento=documento,
                    nombre=data.get("nombre"),
                    ape_paterno=data.get("ape_paterno"),
                    ape_materno=data.get("ape_materno"),
                    id_distrito=data.get("id_distrito"),
                    fecha_nacimiento=data.get("fecha_nac"),
                    direccion=data.get("direccion"),
                    estado_civil=data.get("estado_civil"),
                    ocupacion=data.get("ocupacion"),
                    telefono=data.get("telefono"),
                    correo=data.get("correo")
                )
                bd.session.add(denunciante)
                bd.session.flush()  # obtiene id

            # --------------------------------------------------------
            # 2. Registrar DENUNCIA
            # --------------------------------------------------------
            nueva = Denuncia(
                fecha_incidente=data.get("fecha_incidente"),
                hora_incidente=data.get("hora_incidente"),
                lugar_hechos=data.get("lugar_incidente"),
                direccion=data.get("direccion_incidente"),
                descripcion=data.get("descripcion_incidente"),
                id_denunciante=denunciante.id_persona,
                id_denunciado=None,
                id_tipo_denuncia=data.get("id_tipo_denuncia"),
                id_estado_denuncia=1   # 1 = NUEVO / REGISTRADO
            )
            bd.session.add(nueva)
            bd.session.flush()

            id_denuncia = nueva.id_denuncia

            # --------------------------------------------------------
            # 3. Datos específicos según tipo de denuncia
            # --------------------------------------------------------
            tipo = int(data.get("id_tipo_denuncia"))

            if tipo == 1:  # Patrimonio
                delito = D_Delito_Patrimonio(
                    id_denuncia=id_denuncia,
                    tipo_delito=data.get("tipo_delito"),
                    monto_estimado=data.get("monto_estimado")
                )
                bd.session.add(delito)

            elif tipo == 2:  # Violencia
                violencia = D_Violencia_Domestica(
                    id_denuncia=id_denuncia,
                    tipo=data.get("tipo_violencia"),
                    parentesco=data.get("parentesco")
                )
                bd.session.add(violencia)

            elif tipo == 3:  # Extorsión
                ext = D_Extorsion(
                    id_denuncia=id_denuncia,
                    alias_extorsion=data.get("alias_extorsion"),
                    cantidad=data.get("cantidad")
                )
                bd.session.add(ext)

            # --------------------------------------------------------
            # 4. Registrar bienes (múltiples)
            # --------------------------------------------------------
            bienes_ids = data.getlist("id_bien[]")
            marcas = data.getlist("marca[]")
            modelos = data.getlist("modelo[]")
            unidades = data.getlist("unidades_bienes[]")
            valores = data.getlist("valor_estimado[]")
            descripciones_bien = data.getlist("descripcion_bien[]")

            for i in range(len(bienes_ids)):
                detalle = Detalle_Bienes(
                    id_bien=bienes_ids[i],
                    marca=marcas[i],
                    modelo=modelos[i],
                    unidades=unidades[i],
                    valor_estimado=valores[i],
                    descripcion=descripciones_bien[i],
                    id_denuncia=id_denuncia
                )
                bd.session.add(detalle)

            # --------------------------------------------------------
            # 5. Registrar sospechosos (múltiples)
            # --------------------------------------------------------
            dni_s = data.getlist("s_dni[]")
            nombres_s = data.getlist("s_nombres[]")
            descr_s = data.getlist("s_descripcion[]")
            rol_s = data.getlist("s_rol[]")

            for i in range(len(dni_s)):
                sosp = Detalle_Sospechoso(
                    id_denuncia=id_denuncia,
                    dni=dni_s[i],
                    nombres=nombres_s[i],
                    descripcion=descr_s[i],
                    rol_participacion=rol_s[i]
                )
                bd.session.add(sosp)

            # --------------------------------------------------------
            # 6. Registrar armas (múltiples)
            # --------------------------------------------------------
            tipo_armas = data.getlist("id_tipo_arma[]")
            desc_armas = data.getlist("descripcion_arma[]")
            cant_armas = data.getlist("unidades_armas[]")

            for i in range(len(tipo_armas)):
                arma = Arma(
                    id_denuncia=id_denuncia,
                    id_tipo_arma=tipo_armas[i],
                    descripcion=desc_armas[i],
                    cantidad=cant_armas[i]
                )
                bd.session.add(arma)

            # --------------------------------------------------------
            # 7. Registrar evidencias (múltiples archivos)
            # --------------------------------------------------------
            evidencia_archivos = files.getlist("evidencias[]")
            titulos = data.getlist("titulo_evidencia[]")
            descripcion_e = data.getlist("descripcion_evidencia[]")

            carpeta_evi = os.path.join(current_app.root_path, "static/evidencias")

            if not os.path.exists(carpeta_evi):
                os.makedirs(carpeta_evi)

            for i, archivo in enumerate(evidencia_archivos):
                if archivo and archivo.filename != "":
                    nombre_archivo = f"{id_denuncia}_{archivo.filename}"
                    ruta_guardada = os.path.join(carpeta_evi, nombre_archivo)
                    archivo.save(ruta_guardada)

                    evidencia = Evidencia(
                        titulo=titulos[i],
                        descripcion=descripcion_e[i],
                        ruta=f"/static/evidencias/{nombre_archivo}",
                        id_denuncia=id_denuncia
                    )
                    bd.session.add(evidencia)

            # --------------------------------------------------------
            # 8. Registrar seguimiento
            # --------------------------------------------------------
            seg = Seguimiento_Denuncia(
                id_usuario=id_usuario,
                id_denuncia=id_denuncia,
                fecha=date.today(),
                accion="CREAR - REGISTRAR"
            )
            bd.session.add(seg)

        return id_denuncia

    except Exception as e:
        bd.session.rollback()
        raise e






# # services/mediador_denuncia.py

# from datetime import datetime
# from bd import bd
# from models.Models import Persona
# from models.Denuncia import Denuncia
# from models.Evidencia import Evidencia

# def _normalizar_nombres(nombre_completo: str):
#     partes = nombre_completo.strip().split()
#     if len(partes) >= 3:
#         # Ej: ORLIN WILLIAM ISHUIZA VILCHERREZ -> muy variable
#         # Tomamos lo último como ape_materno, lo penúltimo ape_paterno
#         ape_materno = partes[-1]
#         ape_paterno = partes[-2]
#         nombres = " ".join(partes[:-2])
#     elif len(partes) == 2:
#         nombres = partes[0]
#         ape_paterno = partes[1]
#         ape_materno = "NO ESPECIFICADO"
#     else:
#         nombres = nombre_completo
#         ape_paterno = "NO ESPECIFICADO"
#         ape_materno = "NO ESPECIFICADO"

#     return nombres, ape_paterno, ape_materno


# def registrar_denuncia_mediada(form, files, usuario_actual):
#     # ---------- 1. DATOS DEL DENUNCIANTE ----------
#     dni = form["dni"].strip()
#     nombre_completo = form["nombres"].strip()
#     telefono = form.get("telefono") or None
#     estado_civil = form.get("estado_civil") or "SOLTERO"
#     direccion_denunciante = form.get("direccion_denunciante") or None

#     # Buscamos si ya existe la persona
#     persona = Persona.query.filter_by(dni=dni).first()

#     if not persona:
#         # Intentamos separar nombres y apellidos de 'nombre_completo'
#         nombres, ape_paterno, ape_materno = _normalizar_nombres(nombre_completo)

#         persona = Persona(
#             dni=dni,
#             nombres=nombres,
#             ape_paterno=ape_paterno,
#             ape_materno=ape_materno,
#             estado_civil=estado_civil,
#             ocupacion="NO ESPECIFICADA",  # campo NOT NULL en la BD
#             telefono=telefono,
#             direccion=direccion_denunciante,
#             ubigeo=None
#         )
#         bd.session.add(persona)
#         bd.session.flush()  # para tener persona.id_persona
#     else:
#         # Actualizamos algunos campos si se enviaron
#         if telefono:
#             persona.telefono = telefono
#         if direccion_denunciante:
#             persona.direccion = direccion_denunciante
#         if estado_civil:
#             persona.estado_civil = estado_civil

#     # ---------- 2. DETALLES DE LA DENUNCIA ----------
#     id_tipo_denuncia = int(form["id_tipo_denuncia"])
#     fecha_hechos_str = form["fecha_hechos"]
#     hora_hechos_str = form["hora_hechos"]
#     direccion_hechos = form["direccion_hechos"].strip()
#     descripcion_hechos = form["descripcion_hechos"].strip()
#     modalidad = form.get("modalidad") or None
#     condicion = form.get("condicion") or None

#     # Convertimos fecha (DATE)
#     fecha_acto = datetime.strptime(fecha_hechos_str, "%Y-%m-%d").date()

#     # Construimos una descripción extendida con datos extra
#     descripcion = descripcion_hechos
#     extras = []
#     if hora_hechos_str:
#         extras.append(f"Hora de los hechos: {hora_hechos_str}.")
#     if modalidad:
#         extras.append(f"Modalidad de denuncia: {modalidad}.")
#     if condicion:
#         extras.append(f"Condición de la denuncia: {condicion}.")
#     if extras:
#         descripcion += "\n\n" + " ".join(extras)

#     # ---------- 3. CREAR DENUNCIA ----------
#     denuncia = Denuncia(
#         fecha_acto=fecha_acto,
#         lugar_hechos=direccion_hechos,
#         descripcion=descripcion,
#         estado="P",                            # Pendiente
#         id_denunciante=persona.id_persona,
#         id_denunciado=None,                    # por ahora no lo usamos
#         id_usuario=usuario_actual.id_usuario,  # efectivo que registra
#         id_tipo_denuncia=id_tipo_denuncia,
#         ubigeo=None
#     )

#     bd.session.add(denuncia)
#     bd.session.flush()  # necesitamos denuncia.id_denuncia para evidencias

#     # ---------- 4. EVIDENCIAS ----------
#     tipos_ev = form.getlist("evidencia_tipo[]")
#     descs_ev = form.getlist("evidencia_descripcion[]")
#     archivos_ev = files.getlist("evidencia_archivo[]")

#     for tipo_ev, desc_ev, archivo_ev in zip(tipos_ev, descs_ev, archivos_ev):
#         if not archivo_ev or not archivo_ev.filename:
#             continue

#         # Aquí podrías guardar el archivo en disco y usar esa ruta
#         ruta_archivo = f"/uploads/{archivo_ev.filename}"

#         evidencia = Evidencia(
#             id_denuncia=denuncia.id_denuncia,
#             tipo=tipo_ev,
#             descripcion=desc_ev or None,
#             url_archivo=ruta_archivo
#         )
#         bd.session.add(evidencia)
#         # Si quisieras guardar realmente el archivo, aquí va el save()

#     # devolvemos la denuncia por si la quieres usar
#     return denuncia
