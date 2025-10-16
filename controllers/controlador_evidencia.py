# controladores/controlador_evidencia.py

from bd import obtener_conexion
from models.Evidencia import Evidencia  # Importar la clase Evidencia

def insertar_evidencia(evidencia: Evidencia):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.callproc('pa_insert_evidencia', (
                evidencia.titulo,
                evidencia.url_adjunto,
                evidencia.descripcion,
                evidencia.id_denuncia
            ))
        conexion.commit()
    finally:
        conexion.close()

def modificar_evidencia(evidencia: Evidencia):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.callproc('pa_update_evidencia', (
                evidencia.id_evidencia,
                evidencia.titulo,
                evidencia.url_adjunto,
                evidencia.descripcion,
                evidencia.id_denuncia
            ))
        conexion.commit()
    finally:
        conexion.close()

def eliminar_evidencia(id_evidencia: int):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.callproc('pa_delete_evidencia', (id_evidencia,))
        conexion.commit()
    finally:
        conexion.close()

def obtener_evidencia(id_evidencia: int) -> Evidencia | None:
    conexion = obtener_conexion()
    evidencia = None
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id_evidencia, titulo, url_adjunto, descripcion, id_denuncia FROM evidencia WHERE id_evidencia = %s", (id_evidencia,))
            fila = cursor.fetchone()
            if fila:
                evidencia = Evidencia(*fila)
    finally:
        conexion.close()
    return evidencia
