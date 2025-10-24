# controllers/controlador_comisaria.py
from models.Comisaria import Comisaria
from bd import bd

def obtener_comisarias():
    """Devuelve todas las comisarías registradas."""
    return Comisaria.query.all()

def obtener_comisaria_por_id(id_comisaria):
    """Devuelve una comisaría específica por su ID."""
    return Comisaria.query.get(id_comisaria)

def insertar_comisaria(nombre, direccion, ubigeo, telefono):
    """Inserta una nueva comisaría en la base de datos."""
    nueva = Comisaria(
        nombre=nombre,
        direccion=direccion,
        ubigeo=ubigeo,
        telefono=telefono
    )
    bd.session.add(nueva)
    bd.session.commit()

def modificar_comisaria(id_comisaria, nombre, direccion, ubigeo, telefono):
    """Actualiza una comisaría existente."""
    comisaria = Comisaria.query.get(id_comisaria)
    if comisaria:
        comisaria.nombre = nombre
        comisaria.direccion = direccion
        comisaria.ubigeo = ubigeo
        comisaria.telefono = telefono
        bd.session.commit()
        return True
    return False

def eliminar_comisaria(id_comisaria):
    """Elimina una comisaría de la base de datos."""
    comisaria = Comisaria.query.get(id_comisaria)
    if comisaria:
        bd.session.delete(comisaria)
        bd.session.commit()
        return True
    return False
