# controllers/controlador_evidencia.py
from models.Evidencia import Evidencia
from bd import bd

def obtener_evidencias():
    """Devuelve todas las evidencias registradas."""
    return Evidencia.query.all()

def obtener_evidencia_por_id(id_evidencia):
    """Devuelve una evidencia específica por su ID."""
    return Evidencia.query.get(id_evidencia)

def insertar_evidencia(titulo, url_adjunto, descripcion, id_denuncia):
    """Inserta una nueva evidencia en la base de datos."""
    nueva = Evidencia(
        titulo=titulo,
        url_adjunto=url_adjunto,
        descripcion=descripcion,
        id_denuncia=id_denuncia
    )
    bd.session.add(nueva)
    bd.session.commit()

def modificar_evidencia(id_evidencia, titulo, url_adjunto, descripcion, id_denuncia):
    """Actualiza una evidencia existente."""
    evidencia = Evidencia.query.get(id_evidencia)
    if evidencia:
        evidencia.titulo = titulo
        evidencia.url_adjunto = url_adjunto
        evidencia.descripcion = descripcion
        evidencia.id_denuncia = id_denuncia
        bd.session.commit()
        return True
    return False

def eliminar_evidencia(id_evidencia):
    """Elimina una evidencia de la base de datos."""
    evidencia = Evidencia.query.get(id_evidencia)
    if evidencia:
        bd.session.delete(evidencia)
        bd.session.commit()
        return True
    return False
