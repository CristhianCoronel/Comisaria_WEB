# controllers/controlador_comisaria.py
from models.Comisaria import Comisaria
from bd import bd

def obtener_comisarias():
    return Comisaria.query.all()

def obtener_comisaria_por_id(id_comisaria):
    return Comisaria.query.get(id_comisaria)

def insertar_comisaria(nombre, direccion, ubigeo, telefono):
    try:
        nueva = Comisaria(
            nombre=nombre,
            direccion=direccion,
            ubigeo=ubigeo,
            telefono=telefono
        )
        if nueva:
            bd.session.add(nueva)
            bd.session.commit()
            return True
        print("Error pues")
        return False
    except Exception as e:
        bd.session.rollback()
        print("Error:", e)
        return False

def modificar_comisaria(id_comisaria, nombre, direccion, ubigeo, telefono):
    try:
        comisaria = Comisaria.query.get(id_comisaria)
        if comisaria:
            comisaria.nombre = nombre
            comisaria.direccion = direccion
            comisaria.ubigeo = ubigeo
            comisaria.telefono = telefono
            bd.session.commit()
            return True
        print("Error pues")
        return False
    except Exception as e:
        bd.session.rollback()
        print("Error:", e)
        return False

# def eliminar_comisaria(id_comisaria):
#     """Elimina una comisaría de la base de datos."""
#     comisaria = Comisaria.query.get(id_comisaria)
#     if comisaria:
#         bd.session.delete(comisaria)
#         bd.session.commit()
#         return True
#     return False

def obtener_comisaria_nombre_ubigeo(nombre=None, ubigeo=None):
    base_query = Comisaria.query

    if not nombre and not ubigeo:
        return base_query.order_by(Comisaria.id_comisaria).all()

    # --- Filtro por nombre ---
    query_nombre = base_query
    if nombre:
        query_nombre = query_nombre.filter(Comisaria.nombre.ilike(f"%{nombre}%"))
    res_nombre = query_nombre.all()

    # --- Filtro por ubigeo ---
    query_ubigeo = base_query
    if ubigeo:
        query_ubigeo = query_ubigeo.filter(Comisaria.ubigeo.ilike(f"%{ubigeo}%"))
    res_ubigeo = query_ubigeo.all()

    # Si solo hubo filtro nombre
    if nombre and not ubigeo:
        return res_nombre

    # Si solo hubo filtro ubigeo
    if ubigeo and not nombre:
        return res_ubigeo

    # --- Caso: ambos filtros → comparar tamaños ---
    if len(res_nombre) >= len(res_ubigeo):
        final_query = Comisaria.query.filter(
            Comisaria.nombre.ilike(f"%{nombre}%")
        ).filter(
            Comisaria.ubigeo.ilike(f"%{ubigeo}%")
        )
    else:
        final_query = Comisaria.query.filter(
            Comisaria.ubigeo.ilike(f"%{ubigeo}%")
        ).filter(
            Comisaria.nombre.ilike(f"%{nombre}%")
        )

    return final_query.order_by(Comisaria.id_comisaria).all()

