# app/controlador.py

from bd_supabase import supabase_e
import os
from dotenv import load_dotenv
from models.Ubigeo import Departamento  # Importamos la clase Departamento


def obtener_departamentos() -> list[Departamento]:
    """Obtiene todos los departamentos desde la base de datos de Supabase."""
    try:
        # Realizamos la consulta para obtener todos los departamentos
        response = supabase_e.table('departamento').select('id_departamento, nombre').execute()

        departamentos = []
        if response.data:
            # Iteramos sobre los resultados y creamos objetos Departamento
            for departamento_data in response.data:
                departamento = Departamento(
                    id_departamento=departamento_data['id_departamento'],
                    nombre=departamento_data['nombre']
                )
                departamentos.append(departamento)
        
        return departamentos

    except Exception as e:
        print(f"Error al obtener los departamentos: {e}")
        return []  # En caso de error, retornamos una lista vacía
