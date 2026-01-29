import requests
import os
from dotenv import load_dotenv
import time
from requests.exceptions import ReadTimeout, HTTPError

def fetch_with_retries(url, params, headers, retries=5):
    timeout = 15 # Aumentamos a 15 segundos
    for i in range(retries):
        try:
            print(f"📡 Intento {i+1} de {retries}...")
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except (ReadTimeout, HTTPError) as e:
            wait_time = (i + 1) * 5 # Espera 5, 10, 15... segundos
            print(f"⚠️ Error de conexión: {e}. Reintentando en {wait_time}s...")
            time.sleep(wait_time)
            # Aumentamos el timeout para el siguiente intento
            timeout += 10
    return None

# ... (tu configuración de API Key aquí)

load_dotenv()
# Verifica que el nombre coincida con tu .env
api_key = os.getenv("pokemon_api") 

url = "https://api.pokemontcg.io/v2/sets"
headers = {"X-Api-Key": api_key} if api_key else {}
# Pedimos solo el último set por fecha, sin rodeos
params = {"pageSize": 1, "orderBy": "-releaseDate"}

data = fetch_with_retries(url, params, headers)