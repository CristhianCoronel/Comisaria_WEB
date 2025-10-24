# controllers/controlador_rol.py
from models.Rol import Rol
from bd import bd

def obtener_roles():
    """Devuelve todos los roles registrados."""
    return Rol.query.all()

def obtener_rol_por_id(id_rol):
    """Devuelve un rol específico por su ID."""
    return Rol.query.get(id_rol)

def insertar_rol(nombre, descripcion, id_area):
    """Inserta un nuevo rol en la base de datos."""
    nuevo = Rol(
        nombre=nombre,
        descripcion=descripcion,
        id_area=id_area
    )
    bd.session.add(nuevo)
    bd.session.commit()

def modificar_rol(id_rol, nombre, descripcion, id_area):
    """Actualiza un rol existente."""
    rol = Rol.query.get(id_rol)
    if rol:
        rol.nombre = nombre
        rol.descripcion = descripcion
        rol.id_area = id_area
        bd.session.commit()
        return True
    return False

def eliminar_rol(id_rol):
    """Elimina un rol de la base de datos."""
    rol = Rol.query.get(id_rol)
    if rol:
        bd.session.delete(rol)
        bd.session.commit()
        return True
    return False
