from pokedex import Pokedex
from utils import obtener_datos_pokeapi, guardar_html

def mostrar_menu():
    print("\n=== MENÚ POKÉDEX ===")
    print("1. Mostrar Pokédex")
    print("2. Agregar Pokémon")
    print("3. Salir")

def agregar_pokemon_interactivo(pokedex):
    print("\n➕ Agregar Pokémon")
    nombre = input("Nombre del Pokémon: ").strip()
    
    datos = obtener_datos_pokeapi(nombre)
    if not datos:
        return
    
    print(f"\n🆔 ID: {datos['id']}")
    print(f"📝 Nombre: {datos['name']}")
    print(f"🎨 Tipos: {', '.join(datos['types'])}")
    print(f"❤️ HP: {datos['stats']['hp']}")
    print(f"⚔️ Ataque: {datos['stats']['attack']}")
    
    if input("\n¿Agregar este Pokémon? (s/n): ").lower() == 's':
        try:
            html = pokedex.agregar_pokemon(datos)
            if guardar_html(html):
                print(f"✅ ¡{datos['name']} agregado exitosamente!")
                print("ℹ️ Tabla HTML actualizada y abierta en tu navegador.")
            else:
                print("⚠️ Pokémon agregado pero error al guardar HTML")
        except ValueError as e:
            print(f"❌ {e}")

def main():
    pokedex = Pokedex()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            if guardar_html(pokedex.generar_html()):
                print("✅ Tabla generada y abierta en navegador")
        elif opcion == "2":
            agregar_pokemon_interactivo(pokedex)
        elif opcion == "3":
            print("¡Hasta pronto!")
            break
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    main()