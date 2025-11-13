# services/transaction_manager.py
from contextlib import contextmanager
from bd import bd
from flask import current_app

@contextmanager
def transaccion(nombre="operacion"):
    try:
        yield
        bd.session.commit()
    except Exception as e:
        bd.session.rollback()
        current_app.logger.error(f"Error en transacción [{nombre}]: {e}")
        raise
