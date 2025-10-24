# controllers/controlador_d_asalto.py
from models.Tipo_Denuncia import D_Asalto
from bd import bd

def obtener_asaltos():
    """Devuelve todos los registros de asalto."""
    return D_Asalto.query.all()

def obtener_asalto_por_id(id_denuncia):
    """Devuelve un registro de asalto específico por ID de denuncia."""
    return D_Asalto.query.get(id_denuncia)

def insertar_asalto(id_denuncia, hubo_violencia):
    """Inserta un nuevo registro de asalto en la base de datos."""
    nuevo = D_Asalto(
        id_denuncia=id_denuncia,
        hubo_violencia=hubo_violencia
    )
    bd.session.add(nuevo)
    bd.session.commit()

def modificar_asalto(id_denuncia, hubo_violencia):
    """Actualiza un registro de asalto existente."""
    asalto = D_Asalto.query.get(id_denuncia)
    if asalto:
        asalto.hubo_violencia = hubo_violencia
        bd.session.commit()
        return True
    return False

def eliminar_asalto(id_denuncia):
    """Elimina un registro de asalto de la base de datos."""
    asalto = D_Asalto.query.get(id_denuncia)
    if asalto:
        bd.session.delete(asalto)
        bd.session.commit()
        return True
    return False
