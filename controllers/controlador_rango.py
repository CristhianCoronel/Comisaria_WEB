# controllers/controlador_rango.py
from models.Rango import Rango
from bd import bd

def obtener_rangos():
    """Devuelve todos los rangos registrados."""
    return Rango.query.all()

def obtener_rango_por_id(id_rango):
    """Devuelve un rango específico por su ID."""
    return Rango.query.get(id_rango)

def insertar_rango(nombre, descripcion):
    """Inserta un nuevo rango en la base de datos."""
    nuevo = Rango(
        nombre=nombre,
        descripcion=descripcion
    )
    bd.session.add(nuevo)
    bd.session.commit()

def modificar_rango(id_rango, nombre, descripcion):
    """Actualiza un rango existente."""
    rango = Rango.query.get(id_rango)
    if rango:
        rango.nombre = nombre
        rango.descripcion = descripcion
        bd.session.commit()
        return True
    return False

def eliminar_rango(id_rango):
    """Elimina un rango de la base de datos."""
    rango = Rango.query.get(id_rango)
    if rango:
        bd.session.delete(rango)
        bd.session.commit()
        return True
    return False
