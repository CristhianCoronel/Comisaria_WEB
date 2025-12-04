from models.Models import Comisaria, Distrito
from bd import bd

def obtener_comisarias():
    return Comisaria.query.all()

def obtener_comisaria_por_id(id_comisaria):
    return Comisaria.query.get(id_comisaria)

def insertar_comisaria(nombre, direccion, id_distrito):
    try:
        nueva = Comisaria(
            nombre=nombre,
            direccion=direccion,
            id_distrito=id_distrito
        )
        bd.session.add(nueva)
        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error:", e)
        return False

def modificar_comisaria(id_comisaria, nombre, direccion, id_distrito):
    try:
        comisaria = Comisaria.query.get(id_comisaria)
        if comisaria:
            comisaria.nombre = nombre
            comisaria.direccion = direccion
            comisaria.id_distrito = id_distrito
            bd.session.commit()
            return True
        print("Comisaría no encontrada")
        return False
    except Exception as e:
        bd.session.rollback()
        print("Error:", e)
        return False

# Eliminar comisaría
# def eliminar_comisaria(id_comisaria):
#     try:
#         comisaria = Comisaria.query.get(id_comisaria)
#         if comisaria:
#             bd.session.delete(comisaria)
#             bd.session.commit()
#             return True
#         return False
#     except Exception as e:
#         bd.session.rollback()
#         print("Error:", e)
#         return False


def obtener_comisaria_nombre_ubigeo(nombre=None, ubigeo=None):
    base_query = Comisaria.query.join(Distrito)

    # Si no se aplica ningún filtro
    if not nombre and not ubigeo:
        return base_query.order_by(Comisaria.id_comisaria).all()
    
    if nombre:
        res_nombre = base_query.filter(Comisaria.nombre.ilike(f"%{nombre}%")).all()
    else:
        res_nombre = []

    if ubigeo:
        res_ubigeo = base_query.filter(Distrito.ubigeo.ilike(f"%{ubigeo}%")).all()
    else:
        res_ubigeo = []

    if len(res_nombre) >= len(res_ubigeo):
        query_final = base_query
        if nombre:
            query_final = query_final.filter(Comisaria.nombre.ilike(f"%{nombre}%"))
        if ubigeo:
            query_final = query_final.filter(Distrito.ubigeo.ilike(f"%{ubigeo}%"))
    else:
        query_final = base_query
        if ubigeo:
            query_final = query_final.filter(Distrito.ubigeo.ilike(f"%{ubigeo}%"))
        if nombre:
            query_final = query_final.filter(Comisaria.nombre.ilike(f"%{nombre}%"))

    return query_final.order_by(Comisaria.id_comisaria).all()
