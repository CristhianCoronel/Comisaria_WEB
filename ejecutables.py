# from flask_bcrypt import Bcrypt

# bcrypt = Bcrypt()

# # Contraseñas/códigos originales
# codigo_usuario1 = 'policia123'
# codigo_usuario2 = 'policia456'

# # Generamos los hashes
# hash1 = bcrypt.generate_password_hash(codigo_usuario1).decode('utf-8')
# hash2 = bcrypt.generate_password_hash(codigo_usuario2).decode('utf-8')

# print("Usuario 1 hash:", hash1)
# print("Usuario 2 hash:", hash2)
# Instala graphviz si no lo tienes: pip install graphviz
import graphviz

# Crear objeto Digraph
dot = graphviz.Digraph(comment='Diagrama ER Sistema de Denuncias', format='png')

# Definir entidades y atributos
entidades = {
    'Persona': ['id_persona PK', 'nombre_completo', 'fecha_nacimiento', 'nacionalidad', 'estado_civil', 
                'domicilio', 'telefono', 'correo_electronico', 'tipo_documento', 'numero_documento'],
    'Denuncia': ['id_denuncia PK', 'id_persona FK', 'id_tipo_denuncia FK', 'id_estado_denuncia FK', 
                 'fecha_denuncia', 'hora_denuncia', 'lugar', 'descripcion_general'],
    'Tipo_Denuncia': ['id_tipo_denuncia PK', 'nombre_tipo_denuncia'],
    'Estado_Denuncia': ['id_estado_denuncia PK', 'nombre_estado'],
    'Detalle_Denuncia': ['id_detalle PK', 'id_denuncia FK', 'subtipo', 'descripcion_detalle', 'campos_especificos'],
    'Bienes': ['id_bien PK', 'id_denuncia FK', 'id_tipo_bien FK', 'nombre_bien', 'valor_estimado'],
    'Detalle_Bienes': ['id_detalle_bien PK', 'id_bien FK', 'marca', 'modelo', 'color', 
                       'numero_serie_IMEI_placa', 'anio', 'caracteristicas_especiales'],
    'Vehiculo': ['id_vehiculo PK', 'id_bien FK', 'VIN', 'placas', 'anio', 'marca', 'modelo'],
    'Sospechoso': ['id_sospechoso PK', 'nombre', 'descripcion', 'contacto'],
    'Denuncia_Sospechoso': ['id_denuncia FK', 'id_sospechoso FK'],
    'Testigo': ['id_testigo PK', 'nombre', 'contacto'],
    'Denuncia_Testigo': ['id_denuncia FK', 'id_testigo FK'],
    'Evidencia': ['id_evidencia PK', 'id_denuncia FK', 'tipo_evidencia', 'descripcion', 'ruta_archivo_URL'],
    'Seguimiento_Denuncia': ['id_seguimiento PK', 'id_denuncia FK', 'fecha', 'descripcion_accion', 'responsable'],
    'Medidas_Proteccion': ['id_medida PK', 'id_denuncia FK', 'tipo_medida', 'descripcion', 'fecha_emision']
}

# Agregar entidades al grafo
for entidad, atributos in entidades.items():
    label = entidad + '\n' + '\n'.join(atributos)
    dot.node(entidad, label, shape='box')

# Definir relaciones
relaciones = [
    ('Persona', 'Denuncia'),
    ('Tipo_Denuncia', 'Denuncia'),
    ('Estado_Denuncia', 'Denuncia'),
    ('Denuncia', 'Detalle_Denuncia'),
    ('Denuncia', 'Bienes'),
    ('Bienes', 'Detalle_Bienes'),
    ('Bienes', 'Vehiculo'),
    ('Denuncia', 'Denuncia_Sospechoso'),
    ('Sospechoso', 'Denuncia_Sospechoso'),
    ('Denuncia', 'Denuncia_Testigo'),
    ('Testigo', 'Denuncia_Testigo'),
    ('Denuncia', 'Evidencia'),
    ('Denuncia', 'Seguimiento_Denuncia'),
    ('Denuncia', 'Medidas_Proteccion')
]

# Agregar relaciones al grafo
for origen, destino in relaciones:
    dot.edge(origen, destino)

# Guardar y renderizar
dot.render('diagrama_ER_denuncias', view=True)

print("Diagrama generado: diagrama_ER_denuncias.png")
