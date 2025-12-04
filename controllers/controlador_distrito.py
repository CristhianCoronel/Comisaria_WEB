# controllers/controlador_distrito.py
from models.Models import Distrito
from bd import bd

def obtener_distritos():
    """Devuelve todos los distritos registrados."""
    return Distrito.query.all()

def obtener_distrito_por_id(id_distrito):
    """Devuelve un distrito específico por su ID."""
    return Distrito.query.get(id_distrito)

def insertar_distrito(nombre, id_provincia, ubigeo):
    """Inserta un nuevo distrito en la base de datos."""
    nuevo = Distrito(
        nombre=nombre,
        id_provincia=id_provincia,
        ubigeo=ubigeo
    )
    bd.session.add(nuevo)
    bd.session.commit()

def modificar_distrito(id_distrito, nombre, id_provincia, ubigeo):
    """Actualiza un distrito existente."""
    distrito = Distrito.query.get(id_distrito)
    if distrito:
        distrito.nombre = nombre
        distrito.id_provincia = id_provincia
        distrito.ubigeo = ubigeo
        bd.session.commit()
        return True
    return False

# def eliminar_distrito(id_distrito):
#     """Elimina un distrito de la base de datos."""
#     distrito = Distrito.query.get(id_distrito)
#     if distrito:
#         bd.session.delete(distrito)
#         bd.session.commit()
#         return True
#     return False

def obtener_ubigeo(id_distrito):
    distrito = Distrito.query.get(id_distrito)
    if distrito:
        return distrito.ubigeo
    return None

def obtener_distrito(ubigeo):
    distrito = Distrito.query.filter_by(ubigeo=ubigeo).first()
    if distrito:
        return distrito.id_distrito
    return None
