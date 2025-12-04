# controllers/controlador_evidencia.py
from models.Models import Evidencia
from bd import bd

# ---------------------------
# CONSULTAS
# ---------------------------

def obtener_evidencias():
    return Evidencia.query.all()

def obtener_evidencia_por_id(id_evidencia):
    return Evidencia.query.get(id_evidencia)

def obtener_evidencias_por_denuncia(id_denuncia):
    return Evidencia.query.filter_by(id_denuncia=id_denuncia).all()

def insertar_evidencia(titulo, descripcion, ruta, id_denuncia, tipo=None):
    try:
        nueva = Evidencia(
            titulo=titulo,
            descripcion=descripcion,
            ruta=ruta,
            id_denuncia=id_denuncia,
            tipo=tipo
        )
        bd.session.add(nueva)
        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al insertar evidencia:", e)
        return False

def modificar_evidencia(id_evidencia, titulo=None, descripcion=None, ruta=None, tipo=None, id_denuncia=None):
    try:
        evidencia = Evidencia.query.get(id_evidencia)
        if not evidencia:
            print("Evidencia no encontrada")
            return False

        if titulo: evidencia.titulo = titulo
        if descripcion: evidencia.descripcion = descripcion
        if ruta: evidencia.ruta = ruta
        if tipo: evidencia.tipo = tipo
        if id_denuncia: evidencia.id_denuncia = id_denuncia

        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al modificar evidencia:", e)
        return False

# def eliminar_evidencia(id_evidencia):
#     try:
#         evidencia = Evidencia.query.get(id_evidencia)
#         if evidencia:
#             bd.session.delete(evidencia)
#             bd.session.commit()
#             return True
#         return False
#     except Exception as e:
#         bd.session.rollback()
#         print("Error al eliminar evidencia:", e)
#         return False
