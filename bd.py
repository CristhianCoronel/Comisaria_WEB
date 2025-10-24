from flask_sqlalchemy import SQLAlchemy

# Crear la instancia del ORM
bd = SQLAlchemy()

## se movio al main  las credenciales



# # database.py
# import psycopg2

# def obtener_conexion():
#     return psycopg2.connect(
#         host='localhost',
#         port=5432,
#         user='postgres',
#         password='usat_2025',
#         dbname='bd_comisaria'
#     )
