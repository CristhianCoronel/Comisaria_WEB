from supabase import create_client, Client  # Importar de la librería oficial
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL y la clave de Supabase desde las variables de entorno
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

# Crear el cliente de Supabase
supabase_e: Client = create_client(supabase_url, supabase_key)
