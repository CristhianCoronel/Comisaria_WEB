from monitor_transacciones import monitor_transaccion
from models.Denuncia import insertar_denuncia  # ajusta si tu modelo tiene otro nombre

def procesar_denuncia(datos):
    """
    Lógica de mediación.
    - Valida los datos
    - Controla el flujo
    - Usa el monitor transaccional
    """
    if not datos.get("descripcion"):
        raise ValueError("La descripción es obligatoria")
    if not datos.get("dni"):
        raise ValueError("El DNI del denunciante es obligatorio")

    # Usa el monitor para ejecutar dentro de una transacción segura
    with monitor_transaccion() as cursor:
        insertar_denuncia(cursor, datos)