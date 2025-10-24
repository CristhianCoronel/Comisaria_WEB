# controllers/controlador_tipo_denuncia.py
from models.Tipo_Denuncia import Tipo_Denuncia
from bd import bd

def obtener_tipos_denuncia():
    """Devuelve todos los tipos de denuncia registrados."""
    return Tipo_Denuncia.query.all()

def obtener_tipo_denuncia_por_id(id_tipo):
    """Devuelve un tipo de denuncia específico por su ID."""
    return Tipo_Denuncia.query.get(id_tipo)

def insertar_tipo_denuncia(tipo_denuncia, descripcion, id_area):
    """Inserta un nuevo tipo de denuncia en la base de datos."""
    nuevo = Tipo_Denuncia(
        tipo_denuncia=tipo_denuncia,
        descripcion=descripcion,
        id_area=id_area
    )
    bd.session.add(nuevo)
    bd.session.commit()

def modificar_tipo_denuncia(id_tipo, tipo_denuncia, descripcion, id_area):
    """Actualiza un tipo de denuncia existente."""
    tipo = Tipo_Denuncia.query.get(id_tipo)
    if tipo:
        tipo.tipo_denuncia = tipo_denuncia
        tipo.descripcion = descripcion
        tipo.id_area = id_area
        bd.session.commit()
        return True
    return False

def eliminar_tipo_denuncia(id_tipo):
    """Elimina un tipo de denuncia de la base de datos."""
    tipo = Tipo_Denuncia.query.get(id_tipo)
    if tipo:
        bd.session.delete(tipo)
        bd.session.commit()
        return True
    return False
