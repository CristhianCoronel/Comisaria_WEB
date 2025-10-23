from bd import obtener_conexion


def insertar_persona(dni, nombres, apellidos, fecha_nacimiento, telefono, direccion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO persona (dni, nombres, apellidos, fecha_nacimiento, telefono, direccion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (dni, nombres, apellidos, fecha_nacimiento, telefono, direccion))
    conexion.commit()
    conexion.close()


def obtener_personas():
    conexion = obtener_conexion()
    personas = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT id_persona, dni, nombres, apellidos, fecha_nacimiento, telefono, direccion
            FROM persona
            ORDER BY id_persona
        """)
        personas = cursor.fetchall()
    conexion.close()
    return personas


def eliminar_persona(id_persona):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM persona WHERE id_persona = %s", (id_persona,))
    conexion.commit()
    conexion.close()


def obtener_persona_por_id(id_persona):
    conexion = obtener_conexion()
    persona = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT id_persona, dni, nombres, apellidos, fecha_nacimiento, telefono, direccion
            FROM persona
            WHERE id_persona = %s
        """, (id_persona,))
        persona = cursor.fetchone()
    conexion.close()
    return persona


def actualizar_persona(dni, nombres, apellidos, fecha_nacimiento, telefono, direccion, id_persona):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE persona
            SET dni = %s,
                nombres = %s,
                apellidos = %s,
                fecha_nacimiento = %s,
                telefono = %s,
                direccion = %s
            WHERE id_persona = %s
        """, (dni, nombres, apellidos, fecha_nacimiento, telefono, direccion, id_persona))
    conexion.commit()
    conexion.close()

def obtener_persona_nombre_dni(nombre, dni):
    conexion = obtener_conexion()
    personas = []
    query = """
        SELECT id_persona, dni, nombres, apellidos, fecha_nacimiento, telefono, direccion
        FROM persona
        WHERE 1=1
    """
    parametros = []

    if nombre:  # si no está vacío, se agrega a la consulta
        query += " AND nombres ILIKE %s"
        parametros.append(f"%{nombre}%")
    if dni:  # si no está vacío, también se agrega
        query += " AND dni ILIKE %s"
        parametros.append(f"%{dni}%")

    query += " ORDER BY id_persona"

    with conexion.cursor() as cursor:
        cursor.execute(query, tuple(parametros))
        personas = cursor.fetchall()

    conexion.close()
    return personas
