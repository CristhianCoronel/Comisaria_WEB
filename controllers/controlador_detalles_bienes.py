# controllers/controlador_detalle_bienes.py
from models.Bienes import Detalle_Bienes
from bd import bd

def obtener_detalles_bienes():
    """Devuelve todos los detalles de bienes registrados."""
    return Detalle_Bienes.query.all()

def obtener_detalle_bien_por_id(id_detalle):
    """Devuelve un detalle de bien específico por su ID."""
    return Detalle_Bienes.query.get(id_detalle)

def insertar_detalle_bien(id_denuncia, id_categoria, nombre, monto_asciende, descripcion, tipo_bien):
    """Inserta un nuevo detalle de bien en la base de datos."""
    nuevo = Detalle_Bienes(
        id_denuncia=id_denuncia,
        id_categoria=id_categoria,
        nombre=nombre,
        monto_asciende=monto_asciende,
        descripcion=descripcion,
        tipo_bien=tipo_bien
    )
    bd.session.add(nuevo)
    bd.session.commit()

def modificar_detalle_bien(id_detalle, id_denuncia, id_categoria, nombre, monto_asciende, descripcion, tipo_bien):
    """Actualiza un detalle de bien existente."""
    detalle = Detalle_Bienes.query.get(id_detalle)
    if detalle:
        detalle.id_denuncia = id_denuncia
        detalle.id_categoria = id_categoria
        detalle.nombre = nombre
        detalle.monto_asciende = monto_asciende
        detalle.descripcion = descripcion
        detalle.tipo_bien = tipo_bien
        bd.session.commit()
        return True
    return False

def eliminar_detalle_bien(id_detalle):
    """Elimina un detalle de bien de la base de datos."""
    detalle = Detalle_Bienes.query.get(id_detalle)
    if detalle:
        bd.session.delete(detalle)
        bd.session.commit()
        return True
    return False
