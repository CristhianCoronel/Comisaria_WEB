# controllers/controlador_arma.py
from models.Models import Arma, Tipo_Arma
from bd import bd

def obtener_armas():
    return Arma.query.all()

def obtener_arma_por_id(id_arma):
    return Arma.query.get(id_arma)

def obtener_armas_por_denuncia(id_denuncia):
    return Arma.query.filter_by(id_denuncia=id_denuncia).all()

def insertar_arma(id_denuncia, id_tipo_arma, descripcion=None, cantidad=1):
    try:
        nueva = Arma(
            id_denuncia=id_denuncia,
            id_tipo_arma=id_tipo_arma,
            descripcion=descripcion,
            cantidad=cantidad
        )
        bd.session.add(nueva)
        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al insertar arma:", e)
        return False

def modificar_arma(id_arma, id_denuncia=None, id_tipo_arma=None, descripcion=None, cantidad=None):
    try:
        arma = Arma.query.get(id_arma)
        if not arma:
            print("Arma no encontrada")
            return False

        if id_denuncia: arma.id_denuncia = id_denuncia
        if id_tipo_arma: arma.id_tipo_arma = id_tipo_arma
        if descripcion: arma.descripcion = descripcion
        if cantidad is not None: arma.cantidad = cantidad

        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al modificar arma:", e)
        return False

# def eliminar_arma(id_arma):
#     try:
#         arma = Arma.query.get(id_arma)
#         if arma:
#             bd.session.delete(arma)
#             bd.session.commit()
#             return True
#         return False
#     except Exception as e:
#         bd.session.rollback()
#         print("Error al eliminar arma:", e)
#         return False

# ---------------------------
# CONSULTAS ADICIONALES
# ---------------------------

def obtener_tipo_armas():
    """Devuelve todos los tipos de arma registrados."""
    return Tipo_Arma.query.all()

def obtener_tipo_arma_por_id(id_tipo_arma):
    """Devuelve un tipo de arma específico por su ID."""
    return Tipo_Arma.query.get(id_tipo_arma)
