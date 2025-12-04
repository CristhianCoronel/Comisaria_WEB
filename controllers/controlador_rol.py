from models.Models import Rol
from bd import bd

def obtener_roles():
    return Rol.query.all()

def obtener_rol_por_id(id_rol):
    return Rol.query.get(id_rol)

def insertar_rol(nombre):
    try:
        nuevo = Rol(nombre=nombre)
        bd.session.add(nuevo)
        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al insertar rol:", e)
        return False
    
def modificar_rol(id_rol, nombre):
    try:
        rol = Rol.query.get(id_rol)
        if not rol:
            print("Rol no encontrado")
            return False
        rol.nombre = nombre
        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al modificar rol:", e)
        return False