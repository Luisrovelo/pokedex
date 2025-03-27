import requests
import webbrowser
from pathlib import Path

def obtener_datos_pokeapi(nombre):
    """Obtiene datos de PokeAPI con manejo robusto de errores"""
    try:
        response = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}",
            timeout=10  # Timeout de 10 segundos
        )
        response.raise_for_status()
        data = response.json()

        return {
            "id": data["id"],
            "name": data["name"].capitalize(),
            "types": [t["type"]["name"].capitalize() for t in data["types"]],
            "stats": {
                "hp": data["stats"][0]["base_stat"],
                "attack": data["stats"][1]["base_stat"],
                "defense": data["stats"][2]["base_stat"],
                "special-attack": data["stats"][3]["base_stat"],
                "special-defense": data["stats"][4]["base_stat"],
                "speed": data["stats"][5]["base_stat"]
            }
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            sugerencias = {
                'mewtow': 'mewtwo',
                'pikachu': 'pikachu',
                'charizard': 'charizard'
            }
            if nombre.lower() in sugerencias:
                print(f"⚠️ ¿Quizás quisiste decir '{sugerencias[nombre.lower()]}'?")
            else:
                print("⚠️ Pokémon no encontrado. Verifica el nombre.")
        else:
            print(f"❌ Error de conexión: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def guardar_html(contenido):
    """Guarda el HTML y lo abre en el navegador"""
    try:
        ruta = Path("pokedex.html")
        ruta.write_text(contenido, encoding="utf-8")
        webbrowser.open(f"file://{ruta.absolute()}")
        return True
    except Exception as e:
        print(f"❌ Error al guardar HTML: {e}")
        return False