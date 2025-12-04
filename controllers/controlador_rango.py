# controllers/controlador_rango.py
from models.Models import Rango
from bd import bd

def obtener_rangos():
    return Rango.query.all()

def obtener_rango_por_id(id_rango):
    return Rango.query.get(id_rango)

def insertar_rango(nombre):
    try:
        nuevo = Rango(nombre=nombre)
        bd.session.add(nuevo)
        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al insertar rango:", e)
        return False

def modificar_rango(id_rango, nombre):
    try:
        rango = Rango.query.get(id_rango)
        if not rango:
            print("Rango no encontrado")
            return False
        rango.nombre = nombre
        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al modificar rango:", e)
        return False

# def eliminar_rango(id_rango):
#     """Elimina un rango de la base de datos."""
#     try:
#         rango = Rango.query.get(id_rango)
#         if rango:
#             bd.session.delete(rango)
#             bd.session.commit()
#             return True
#         return False
#     except Exception as e:
#         bd.session.rollback()
#         print("Error al eliminar rango:", e)
#         return False
