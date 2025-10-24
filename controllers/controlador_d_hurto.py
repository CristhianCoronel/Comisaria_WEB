# controllers/controlador_d_hurto.py
from models.Tipo_Denuncia import D_Hurto
from bd import bd

def obtener_hurtos():
    """Devuelve todos los registros de hurto."""
    return D_Hurto.query.all()

def obtener_hurto_por_id(id_denuncia):
    """Devuelve un registro de hurto específico por ID de denuncia."""
    return D_Hurto.query.get(id_denuncia)

def insertar_hurto(id_denuncia, circunstancias):
    """Inserta un nuevo registro de hurto en la base de datos."""
    nuevo = D_Hurto(
        id_denuncia=id_denuncia,
        circunstancias=circunstancias
    )
    bd.session.add(nuevo)
    bd.session.commit()

def modificar_hurto(id_denuncia, circunstancias):
    """Actualiza un registro de hurto existente."""
    hurto = D_Hurto.query.get(id_denuncia)
    if hurto:
        hurto.circunstancias = circunstancias
        bd.session.commit()
        return True
    return False

def eliminar_hurto(id_denuncia):
    """Elimina un registro de hurto de la base de datos."""
    hurto = D_Hurto.query.get(id_denuncia)
    if hurto:
        bd.session.delete(hurto)
        bd.session.commit()
        return True
    return False
