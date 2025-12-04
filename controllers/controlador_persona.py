# controllers/controlador_persona.py
from models.Models import Persona, Tipo_Documento
from bd import bd

def obtener_personas():
    return Persona.query.all()

def obtener_persona_por_id(id_persona):
    return Persona.query.get(id_persona)

def obtener_persona_por_documento(tipo_documento_id, documento):
    return Persona.query.filter_by(
        id_tipo_documento=tipo_documento_id,
        documento=documento
    ).first()

def insertar_persona(id_tipo_documento, documento, nombre, ape_paterno, ape_materno,
                     id_distrito, fecha_nacimiento, direccion, estado_civil,
                     ocupacion='Sin ocupación', telefono=None, correo=None):
    try:
        nueva = Persona(
            id_tipo_documento=id_tipo_documento,
            documento=documento,
            nombre=nombre,
            ape_paterno=ape_paterno,
            ape_materno=ape_materno,
            id_distrito=id_distrito,
            fecha_nacimiento=fecha_nacimiento,
            direccion=direccion,
            estado_civil=estado_civil,
            ocupacion=ocupacion,
            telefono=telefono,
            correo=correo
        )
        bd.session.add(nueva)
        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al insertar persona:", e)
        return False

def modificar_persona(id_persona, id_tipo_documento=None, documento=None, nombre=None, 
                      ape_paterno=None, ape_materno=None, id_distrito=None,
                      fecha_nacimiento=None, direccion=None, estado_civil=None,
                      ocupacion=None, telefono=None, correo=None):
    try:
        persona = Persona.query.get(id_persona)
        if not persona:
            print("Persona no encontrada")
            return False

        if id_tipo_documento: persona.id_tipo_documento = id_tipo_documento
        if documento: persona.documento = documento
        if nombre: persona.nombre = nombre
        if ape_paterno: persona.ape_paterno = ape_paterno
        if ape_materno: persona.ape_materno = ape_materno
        if id_distrito: persona.id_distrito = id_distrito
        if fecha_nacimiento: persona.fecha_nacimiento = fecha_nacimiento
        if direccion: persona.direccion = direccion
        if estado_civil: persona.estado_civil = estado_civil
        if ocupacion: persona.ocupacion = ocupacion
        if telefono: persona.telefono = telefono
        if correo: persona.correo = correo

        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al modificar persona:", e)
        return False

# def eliminar_persona(id_persona):
#     try:
#         persona = Persona.query.get(id_persona)
#         if persona:
#             bd.session.delete(persona)
#             bd.session.commit()
#             return True
#         return False
#     except Exception as e:
#         bd.session.rollback()
#         print("Error al eliminar persona:", e)
#         return False

def obtener_personas_nombre_dni(nombre=None, dni=None):
    query_base = Persona.query

    if not nombre and not dni:
        return query_base.order_by(Persona.id_persona).all()

    query_nombre = query_base
    if nombre:
        query_nombre = query_nombre.filter(Persona.nombre.ilike(f"%{nombre}%"))

    query_dni = query_base
    if dni:
        query_dni = query_dni.filter(Persona.documento.ilike(f"%{dni}%"))

    count_nombre = query_nombre.count() if nombre else 0
    count_dni = query_dni.count() if dni else 0

    if count_nombre >= count_dni:
        query_final = query_nombre
        if dni:
            query_final = query_final.filter(Persona.documento.ilike(f"%{dni}%"))
    else:
        query_final = query_dni
        if nombre:
            query_final = query_final.filter(Persona.nombre.ilike(f"%{nombre}%"))

    return query_final.order_by(Persona.id_persona).all()

################################

## Controladores adicionales

###############################

def obtener_tipos_documentos():
    return Tipo_Documento.query.all()

