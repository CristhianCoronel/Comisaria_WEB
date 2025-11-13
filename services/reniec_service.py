import requests
from main import FACILIZA_TOKEN, FACILIZA_URL

def consultar_dni_faciliza(dni: str):
    """
    Llama a la API de Faciliza y devuelve el dict `data` con los datos del DNI
    o None si no lo encuentra / hubo error.
    """
    if not FACILIZA_TOKEN:
        print("⚠ FACILIZA_TOKEN no configurado")
        return None

    try:
        headers = {
            "Authorization": f"Bearer {FACILIZA_TOKEN}"
        }
        url = f"{FACILIZA_URL}/{dni}"
        resp = requests.get(url, headers=headers, timeout=5)

        if resp.status_code != 200:
            print("Error API Faciliza:", resp.status_code, resp.text)
            return None

        payload = resp.json()
        if not payload.get("success"):
            print("API respondió sin éxito:", payload)
            return None

        return payload.get("data")  # aquí viene: numero, nombres, apellido_paterno, ...
    except Exception as e:
        print("Excepción llamando API Faciliza:", e)
        return None
