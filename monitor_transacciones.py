from contextlib import contextmanager
from bd import get_connection  # usa tu conexión actual a la base de datos

@contextmanager
def monitor_transaccion():
    """
    Monitor de Procesamiento de Transacciones (TPM).
    Garantiza commit o rollback automático.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor  # Aquí se ejecutan las operaciones SQL
        conn.commit()
        print("✅ Transacción confirmada correctamente")
    except Exception as e:
        conn.rollback()
        print("❌ Error en la transacción:", e)
        raise
    finally:
        cursor.close()
        conn.close()