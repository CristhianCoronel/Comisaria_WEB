# controllers/controlador_denuncia.py
from models.Denuncia import Denuncia
from bd import bd

def obtener_denuncias():
    """Devuelve todas las denuncias registradas."""
    return Denuncia.query.all()

def obtener_denuncia_por_id(id_denuncia):
    """Devuelve una denuncia específica por su ID."""
    return Denuncia.query.get(id_denuncia)

def insertar_denuncia(fecha_acto, lugar_hechos, descripcion, id_denunciante, id_denunciado, id_usuario, id_tipo_denuncia, ubigeo):
    """Inserta una nueva denuncia en la base de datos."""
    nueva = Denuncia(
        fecha_acto=fecha_acto,
        lugar_hechos=lugar_hechos,
        descripcion=descripcion,
        id_denunciante=id_denunciante,
        id_denunciado=id_denunciado,
        id_usuario=id_usuario,
        id_tipo_denuncia=id_tipo_denuncia,
        ubigeo=ubigeo
    )
    bd.session.add(nueva)
    bd.session.commit()

def modificar_denuncia(id_denuncia, fecha_acto, lugar_hechos, descripcion, id_denunciante, id_denunciado, id_usuario, id_tipo_denuncia, ubigeo, estado):
    """Actualiza una denuncia existente."""
    denuncia = Denuncia.query.get(id_denuncia)
    if denuncia:
        denuncia.fecha_acto = fecha_acto
        denuncia.lugar_hechos = lugar_hechos
        denuncia.descripcion = descripcion
        denuncia.id_denunciante = id_denunciante
        denuncia.id_denunciado = id_denunciado
        denuncia.id_usuario = id_usuario
        denuncia.id_tipo_denuncia = id_tipo_denuncia
        denuncia.ubigeo = ubigeo
        denuncia.estado = estado
        bd.session.commit()
        return True
    return False

def eliminar_denuncia(id_denuncia):
    """Elimina una denuncia de la base de datos."""
    denuncia = Denuncia.query.get(id_denuncia)
    if denuncia:
        bd.session.delete(denuncia)
        bd.session.commit()
        return True
    return False
