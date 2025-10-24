# controllers/controlador_provincia.py
from models.Ubigeo import Provincia
from bd import bd

def obtener_provincias():
    """Devuelve todas las provincias registradas."""
    return Provincia.query.all()

def obtener_provincia_por_id(id_provincia):
    """Devuelve una provincia específica por su ID."""
    return Provincia.query.get(id_provincia)

def insertar_provincia(nombre, id_departamento):
    """Inserta una nueva provincia en la base de datos."""
    nueva = Provincia(
        nombre=nombre,
        id_departamento=id_departamento
    )
    bd.session.add(nueva)
    bd.session.commit()

def modificar_provincia(id_provincia, nombre, id_departamento):
    """Actualiza una provincia existente."""
    provincia = Provincia.query.get(id_provincia)
    if provincia:
        provincia.nombre = nombre
        provincia.id_departamento = id_departamento
        bd.session.commit()
        return True
    return False

def eliminar_provincia(id_provincia):
    """Elimina una provincia de la base de datos."""
    provincia = Provincia.query.get(id_provincia)
    if provincia:
        bd.session.delete(provincia)
        bd.session.commit()
        return True
    return False
