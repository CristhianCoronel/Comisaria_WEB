# controllers/controlador_departamento.py
from models.Ubigeo import Departamento
from bd import bd

def obtener_departamentos():
    """Devuelve todos los departamentos registrados."""
    return Departamento.query.all()

def obtener_departamento_por_id(id_departamento):
    """Devuelve un departamento específico por su ID."""
    return Departamento.query.get(id_departamento)

def insertar_departamento(nombre):
    """Inserta un nuevo departamento en la base de datos."""
    nuevo = Departamento(nombre=nombre)
    bd.session.add(nuevo)
    bd.session.commit()

def modificar_departamento(id_departamento, nombre):
    """Actualiza un departamento existente."""
    departamento = Departamento.query.get(id_departamento)
    if departamento:
        departamento.nombre = nombre
        bd.session.commit()
        return True
    return False

def eliminar_departamento(id_departamento):
    """Elimina un departamento de la base de datos."""
    departamento = Departamento.query.get(id_departamento)
    if departamento:
        bd.session.delete(departamento)
        bd.session.commit()
        return True
    return False
