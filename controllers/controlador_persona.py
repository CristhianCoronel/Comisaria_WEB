from models.Persona import Persona
from bd import bd

def obtener_personas():
    return Persona.query.order_by(Persona.id_persona).all()

def obtener_persona_por_id(id_persona):
    return Persona.query.get(id_persona)

def obtener_persona_por_dni(dni_persona):
    try:
        persona = Persona.query.filter_by(dni=dni_persona).first()
        return persona
    except Exception as e:
        print("Error al buscar persona:", e)
        return None

def insertar_persona(dni, nombres, ape_paterno, ape_materno, estado_civil, ocupacion, fecha_nacimiento=None, telefono=None, direccion=None, ubigeo=None):
    nueva = Persona(dni=dni, nombres=nombres, ape_paterno=ape_paterno, ape_materno=ape_materno, estado_civil=estado_civil, ocupacion=ocupacion,
                    fecha_nacimiento=fecha_nacimiento, telefono=telefono, direccion=direccion, ubigeo=ubigeo)
    if nueva:
        bd.session.add(nueva)
        bd.session.commit()
        return True
    return False

def actualizar_persona(id_persona, dni, nombres, ape_paterno, ape_materno, estado_civil, ocupacion, fecha_nacimiento=None, telefono=None, direccion=None, ubigeo=None):
    persona = Persona.query.get(id_persona)
    if persona:
        persona.dni = dni
        persona.nombres = nombres
        persona.ape_paterno = ape_paterno
        persona.ape_materno = ape_materno
        persona.estado_civil = estado_civil
        persona.ocupacion = ocupacion
        persona.fecha_nacimiento = fecha_nacimiento
        persona.telefono = telefono
        persona.direccion = direccion
        persona.ubigeo = ubigeo
        bd.session.commit()
        return True
    return False

def eliminar_persona(id_persona):
    persona = Persona.query.get(id_persona)
    if persona:
        bd.session.delete(persona)
        bd.session.commit()
        return True
    return False

def obtener_persona_nombre_dni(nombre=None, dni=None):
    base_query = Persona.query

    if not nombre and not dni:
        return base_query.order_by(Persona.id_persona).all()

    query_nombre = base_query
    if nombre:
        query_nombre = query_nombre.filter(Persona.nombres.ilike(f"%{nombre}%"))
    res_nombre = query_nombre.all()

    query_dni = base_query
    if dni:
        query_dni = query_dni.filter(Persona.dni.ilike(f"%{dni}%"))
    res_dni = query_dni.all()

    # --- Decidir qué filtro tiene más resultados ---
    len_nombre = len(res_nombre)
    len_dni = len(res_dni)

    if nombre and not dni:
        return res_nombre

    if dni and not nombre:
        return res_dni

    # Caso: ambos existen → comparar tamaños
    if len_nombre >= len_dni:
        final_query = Persona.query.filter(
            Persona.nombres.ilike(f"%{nombre}%")
        ).filter(
            Persona.dni.ilike(f"%{dni}%")
        )
    else:
        final_query = Persona.query.filter(
            Persona.dni.ilike(f"%{dni}%")
        ).filter(
            Persona.nombres.ilike(f"%{nombre}%")
        )

    return final_query.order_by(Persona.id_persona).all()

def duplicado_dni(dni):
    persona = Persona.query.filter_by(dni=dni).first()
    if persona:
        return True
    return False
