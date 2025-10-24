# controllers/controlador_ubigeo.py
from models.Ubigeo import Ubigeo
from bd import bd

def obtener_ubigeos():
    """Devuelve todos los ubigeos registrados."""
    return Ubigeo.query.all()

def obtener_ubigeo_por_id(id_ubigeo):
    """Devuelve un ubigeo específico por su ID."""
    return Ubigeo.query.get(id_ubigeo)

def insertar_ubigeo(codigo, id_distrito):
    """Inserta un nuevo ubigeo en la base de datos."""
    nuevo = Ubigeo(
        codigo=codigo,
        id_distrito=id_distrito
    )
    bd.session.add(nuevo)
    bd.session.commit()

def modificar_ubigeo(id_ubigeo, codigo, id_distrito):
    """Actualiza un ubigeo existente."""
    ubigeo = Ubigeo.query.get(id_ubigeo)
    if ubigeo:
        ubigeo.codigo = codigo
        ubigeo.id_distrito = id_distrito
        bd.session.commit()
        return True
    return False

def eliminar_ubigeo(id_ubigeo):
    """Elimina un ubigeo de la base de datos."""
    ubigeo = Ubigeo.query.get(id_ubigeo)
    if ubigeo:
        bd.session.delete(ubigeo)
        bd.session.commit()
        return True
    return False
