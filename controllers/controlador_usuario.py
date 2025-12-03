# controllers/controlador_usuario.py
from models.Usuario import Usuario
from bd import bd

def obtener_usuarios():
    """Devuelve todos los usuarios registrados."""
    return Usuario.query.all()

def obtener_usuario_por_id(id_usuario):
    """Devuelve un usuario específico por su ID."""
    return Usuario.query.get(id_usuario)

def obtener_siguiente_id_usuario():
    ultima_persona = Usuario.query.order_by(Usuario.id_usuario.desc()).first()
    
    if ultima_persona:
        return ultima_persona.id_usuario + 1
    else:
        # Si no hay registros, empezamos desde 1
        return 1

def obtener_usuario_por_dni(dni_usuario):
    return Usuario.query.filter_by(dni=dni_usuario).first()

def insertar_usuario(dni, nombres, ape_paterno, ape_materno, codigo_usuario, estado, id_comisaria, id_rango, id_rol, tipo_usuario):
    try:
        id_usuario = obtener_siguiente_id_usuario()
        print("Nuevo id:", id_usuario)
        nuevo = Usuario(
            id_usuario=id_usuario,
            dni=dni,
            nombres=nombres,
            ape_paterno=ape_paterno,
            ape_materno=ape_materno,
            codigo_usuario=codigo_usuario,
            estado=estado,
            id_comisaria=id_comisaria,
            id_rango=id_rango,
            id_rol=id_rol,
            tipo_usuario=tipo_usuario
        )
        if nuevo:
            bd.session.add(nuevo)
            bd.session.commit()
            return True
        return False
    except Exception as e:
        bd.session.rollback()
        print("Error:", e)
        return False


def modificar_usuario(id_usuario, dni, nombres, ape_paterno, ape_materno, estado, id_comisaria, id_rango, id_rol, tipo_usuario):
    try:
        usuario = Usuario.query.get(id_usuario)
        if usuario:
            usuario.dni = dni
            usuario.nombres = nombres
            usuario.ape_paterno = ape_paterno
            usuario.ape_materno = ape_materno
            usuario.estado = estado
            usuario.id_comisaria = id_comisaria
            usuario.id_rango = id_rango
            usuario.id_rol = id_rol
            usuario.tipo_usuario = tipo_usuario
            bd.session.commit()
            return True
        return False
    except Exception as e:
        bd.session.rollback()
        print("Error:", e)
        return False

def eliminar_usuario(id_usuario):
    """Elimina un usuario de la base de datos."""
    usuario = Usuario.query.get(id_usuario)
    if usuario:
        bd.session.delete(usuario)
        bd.session.commit()
        return True
    return False

def validar_usuario_activo(dni_usuario):
    return Usuario.query.filter_by(dni=dni_usuario, estado='A').first()

def obtener_persona_nombre_dni(nombre=None, dni=None):
    base_query = Usuario.query

    if not nombre and not dni:
        return base_query.order_by(Usuario.id_usuario).all()

    query_nombre = base_query
    if nombre:
        query_nombre = query_nombre.filter(Usuario.nombres.ilike(f"%{nombre}%"))
    res_nombre = query_nombre.all()

    query_dni = base_query
    if dni:
        query_dni = query_dni.filter(Usuario.dni.ilike(f"%{dni}%"))
    res_dni = query_dni.all()

    # --- Decidir qué filtro tiene más resultados ---
    len_nombre = len(res_nombre)
    len_dni = len(res_dni)

    if nombre and not dni:
        return res_nombre

    if dni and not nombre:
        return res_dni

    # Caso: ambos existen → comparar tamaños
    if len_nombre >= len_dni:
        final_query = Usuario.query.filter(
            Usuario.nombres.ilike(f"%{nombre}%")
        ).filter(
            Usuario.dni.ilike(f"%{dni}%")
        )
    else:
        final_query = Usuario.query.filter(
            Usuario.dni.ilike(f"%{dni}%")
        ).filter(
            Usuario.nombres.ilike(f"%{nombre}%")
        )

    return final_query.order_by(Usuario.id_usuario).all()

def cambiar_codigo_usuario(id_usuario, codigo_usuario):
    try:
        usuario = Usuario.query.get(id_usuario)
        if usuario:
            usuario.codigo_usuario = codigo_usuario
            bd.session.commit()
            return True
        return False
    except Exception as e:
        bd.session.rollback()
        print("Error:", e)
        return False

def duplicado_dni(dni):
    usuario = Usuario.query.filter_by(dni=dni).first()
    if usuario:
        return True
    return False