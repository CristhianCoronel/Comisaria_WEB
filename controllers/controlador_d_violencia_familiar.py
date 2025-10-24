# controllers/controlador_d_violencia_familiar.py
from models.Tipo_Denuncia import D_Violencia_Familiar
from bd import bd

def obtener_violencias_familiar():
    """Devuelve todos los registros de violencia familiar."""
    return D_Violencia_Familiar.query.all()

def obtener_violencia_familiar_por_id(id_denuncia):
    """Devuelve un registro de violencia familiar específico por ID de denuncia."""
    return D_Violencia_Familiar.query.get(id_denuncia)

def insertar_violencia_familiar(id_denuncia, tipo_violencia, relacion_agresor, medidas_proteccion):
    """Inserta un nuevo registro de violencia familiar en la base de datos."""
    nuevo = D_Violencia_Familiar(
        id_denuncia=id_denuncia,
        tipo_violencia=tipo_violencia,
        relacion_agresor=relacion_agresor,
        medidas_proteccion=medidas_proteccion
    )
    bd.session.add(nuevo)
    bd.session.commit()

def modificar_violencia_familiar(id_denuncia, tipo_violencia, relacion_agresor, medidas_proteccion):
    """Actualiza un registro de violencia familiar existente."""
    vf = D_Violencia_Familiar.query.get(id_denuncia)
    if vf:
        vf.tipo_violencia = tipo_violencia
        vf.relacion_agresor = relacion_agresor
        vf.medidas_proteccion = medidas_proteccion
        bd.session.commit()
        return True
    return False

def eliminar_violencia_familiar(id_denuncia):
    """Elimina un registro de violencia familiar de la base de datos."""
    vf = D_Violencia_Familiar.query.get(id_denuncia)
    if vf:
        bd.session.delete(vf)
        bd.session.commit()
        return True
    return False
