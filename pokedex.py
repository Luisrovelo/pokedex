import json
from pathlib import Path

class Pokedex:
    def __init__(self):
        self.pokemons = self.cargar_datos()

    def cargar_datos(self):
        try:
            with open("data/pokemon.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def existe_pokemon(self, identificador):
        """Busca por ID (int) o nombre (str)"""
        if isinstance(identificador, int):
            return any(p['id'] == identificador for p in self.pokemons)
        return any(p['name'].lower() == identificador.lower() for p in self.pokemons)

    def agregar_pokemon(self, pokemon_data):
        """Añade Pokémon y devuelve HTML actualizado"""
        if self.existe_pokemon(pokemon_data['id']) or self.existe_pokemon(pokemon_data['name']):
            raise ValueError("¡Este Pokémon ya existe en la Pokédex!")
        
        self.pokemons.append(pokemon_data)
        self.guardar_datos()
        return self.generar_html()

    def guardar_datos(self):
        with open("data/pokemon.json", "w") as f:
            json.dump(self.pokemons, f, indent=2)

    def generar_html(self):
        """Genera tabla HTML con estilos modernos"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pokédex</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                h1 {{
                    color: #e63946;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    border-radius: 8px;
                    overflow: hidden;
                }}
                th, td {{
                    padding: 12px 15px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #457b9d;
                    color: white;
                    font-weight: bold;
                }}
                tr:nth-child(even) {{
                    background-color: #f8f9fa;
                }}
                tr:hover {{
                    background-color: #e9ecef;
                }}
                img.pokemon-img {{
                    width: 60px;
                    height: 60px;
                    object-fit: contain;
                    transition: transform 0.2s;
                }}
                img.pokemon-img:hover {{
                    transform: scale(1.1);
                }}
                .nuevo {{
                    animation: highlight 2s;
                }}
                @keyframes highlight {{
                    from {{ background-color: #a7c957; }}
                    to {{ background-color: transparent; }}
                }}
            </style>
        </head>
        <body>
            <h1>Pokédex ({len(self.pokemons)} Pokémon)</h1>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Imagen</th>
                    <th>Nombre</th>
                    <th>Tipos</th>
                    <th>HP</th>
                    <th>Ataque</th>
                </tr>
        """

        for pokemon in sorted(self.pokemons, key=lambda x: x['id']):
            html += f"""
                <tr{' class="nuevo"' if pokemon == self.pokemons[-1] else ''}>
                    <td>{pokemon['id']}</td>
                    <td><img class="pokemon-img" src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon['id']}.png" alt="{pokemon['name']}"></td>
                    <td>{pokemon['name']}</td>
                    <td>{', '.join(pokemon['types'])}</td>
                    <td>{pokemon['stats']['hp']}</td>
                    <td>{pokemon['stats']['attack']}</td>
                </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """
        return html