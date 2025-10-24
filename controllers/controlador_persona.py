from models.Persona import Persona
from bd import bd

def obtener_personas():
    return Persona.query.order_by(Persona.id_persona).all()

def obtener_persona_por_id(id_persona):
    return Persona.query.get(id_persona)

def insertar_persona(dni, nombres, apellidos, fecha_nacimiento=None, telefono=None, direccion=None):
    nueva = Persona(dni=dni, nombres=nombres, apellidos=apellidos,
                    fecha_nacimiento=fecha_nacimiento, telefono=telefono, direccion=direccion)
    bd.session.add(nueva)
    bd.session.commit()

def actualizar_persona(id_persona, dni, nombres, apellidos, fecha_nacimiento=None, telefono=None, direccion=None):
    persona = Persona.query.get(id_persona)
    if persona:
        persona.dni = dni
        persona.nombres = nombres
        persona.apellidos = apellidos
        persona.fecha_nacimiento = fecha_nacimiento
        persona.telefono = telefono
        persona.direccion = direccion
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
    query = Persona.query
    if nombre:
        query = query.filter(Persona.nombres.ilike(f"%{nombre}%"))
    if dni:
        query = query.filter(Persona.dni.ilike(f"%{dni}%"))
    return query.order_by(Persona.id_persona).all()
