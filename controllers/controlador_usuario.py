# controllers/controlador_usuario.py
from models.Usuario import Usuario
from bd import bd

def obtener_usuarios():
    """Devuelve todos los usuarios registrados."""
    return Usuario.query.all()

def obtener_usuario_por_id(id_usuario):
    """Devuelve un usuario específico por su ID."""
    return Usuario.query.get(id_usuario)

def insertar_usuario(dni, nombres, ape_paterno, ape_materno, codigo_usuario, estado, id_comisaria, id_rango, id_rol, tipo_usuario):
    """Inserta un nuevo usuario en la base de datos."""
    nuevo = Usuario(
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
    bd.session.add(nuevo)
    bd.session.commit()

def modificar_usuario(id_usuario, dni, nombres, ape_paterno, ape_materno, codigo_usuario, estado, id_comisaria, id_rango, id_rol, tipo_usuario):
    """Actualiza un usuario existente."""
    usuario = Usuario.query.get(id_usuario)
    if usuario:
        usuario.dni = dni
        usuario.nombres = nombres
        usuario.ape_paterno = ape_paterno
        usuario.ape_materno = ape_materno
        usuario.codigo_usuario = codigo_usuario
        usuario.estado = estado
        usuario.id_comisaria = id_comisaria
        usuario.id_rango = id_rango
        usuario.id_rol = id_rol
        usuario.tipo_usuario = tipo_usuario
        bd.session.commit()
        return True
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