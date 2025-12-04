# controllers/controlador_usuario.py
from models.Models import Usuario
from bd import bd


def obtener_usuarios():
    return Usuario.query.all()

def obtener_usuario_por_id(id_usuario):
    return Usuario.query.get(id_usuario)

def obtener_usuario_por_dni(dni_usuario):
    return Usuario.query.filter_by(dni=dni_usuario).first()

def insertar_usuario(dni, nombres, ape_paterno, ape_materno, codigo_usuario, clave,
                     id_comisaria, id_rango, id_rol, estado='A'):
    try:
        nuevo = Usuario(
            dni=dni,
            nombres=nombres,
            ape_paterno=ape_paterno,
            ape_materno=ape_materno,
            codigo_usuario=codigo_usuario,
            clave=clave,
            id_comisaria=id_comisaria,
            id_rango=id_rango,
            id_rol=id_rol,
            estado=estado
        )
        bd.session.add(nuevo)
        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al insertar usuario:", e)
        return False

def modificar_usuario(id_usuario, dni=None, nombres=None, ape_paterno=None, ape_materno=None,
                      codigo_usuario=None, clave=None, id_comisaria=None, id_rango=None, id_rol=None):
    try:
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            print("Usuario no encontrado")
            return False

        if dni: usuario.dni = dni
        if nombres: usuario.nombres = nombres
        if ape_paterno: usuario.ape_paterno = ape_paterno
        if ape_materno: usuario.ape_materno = ape_materno
        if codigo_usuario: usuario.codigo_usuario = codigo_usuario
        if clave: usuario.clave = clave
        if id_comisaria: usuario.id_comisaria = id_comisaria
        if id_rango: usuario.id_rango = id_rango
        if id_rol: usuario.id_rol = id_rol

        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al modificar usuario:", e)
        return False

def cambiar_estado(id_usuario, nuevo_estado):
    """
    Cambia el estado del usuario ('A' = Activo, 'I' = Inactivo, 'R' = Retirado)
    """
    try:
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            print("Usuario no encontrado")
            return False

        usuario.estado = nuevo_estado
        bd.session.commit()
        return True
    except Exception as e:
        bd.session.rollback()
        print("Error al cambiar estado:", e)
        return False

def obtener_usuarios_nombre_dni(nombre=None, dni=None):
    query_base = Usuario.query

    if not nombre and not dni:
        return query_base.order_by(Usuario.id_usuario).all()

    query_nombre = query_base
    if nombre:
        query_nombre = query_nombre.filter(Usuario.nombres.ilike(f"%{nombre}%"))

    query_dni = query_base
    if dni:
        query_dni = query_dni.filter(Usuario.dni.ilike(f"%{dni}%"))

    count_nombre = query_nombre.count() if nombre else 0
    count_dni = query_dni.count() if dni else 0

    if count_nombre >= count_dni:
        query_final = query_nombre
        if dni:
            query_final = query_final.filter(Usuario.dni.ilike(f"%{dni}%"))
    else:
        query_final = query_dni
        if nombre:
            query_final = query_final.filter(Usuario.nombres.ilike(f"%{nombre}%"))

    return query_final.order_by(Usuario.id_usuario).all()

