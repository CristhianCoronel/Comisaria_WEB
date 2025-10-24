# controllers/controlador_area.py
from models.Area import Area
from bd import bd

def obtener_areas():
    """Devuelve todas las áreas registradas."""
    return Area.query.all()

def obtener_area_por_id(id_area):
    """Devuelve un área específica por su ID."""
    return Area.query.get(id_area)

def insertar_area(nombre, descripcion):
    """Inserta una nueva área en la base de datos."""
    nueva = Area(
        nombre=nombre,
        descripcion=descripcion
    )
    bd.session.add(nueva)
    bd.session.commit()

def modificar_area(id_area, nombre, descripcion):
    """Actualiza un área existente."""
    area = Area.query.get(id_area)
    if area:
        area.nombre = nombre
        area.descripcion = descripcion
        bd.session.commit()
        return True
    return False

def eliminar_area(id_area):
    """Elimina un área de la base de datos."""
    area = Area.query.get(id_area)
    if area:
        bd.session.delete(area)
        bd.session.commit()
        return True
    return False
