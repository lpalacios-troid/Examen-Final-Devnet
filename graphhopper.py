import os
import requests

API_KEY = os.getenv("GRAPHHOPPER_API_KEY")

ciudades = {
    "santiago": (-33.4489, -70.6693),
    "copiapo": (-27.3668, -70.3322),
    "la serena": (-29.9027, -71.2519),
    "mendoza": (-32.8895, -68.8458),
    "buenos aires": (-34.6037, -58.3816)
}


def obtener_coordenadas(ciudad):
    ciudad = ciudad.lower().strip()

    if ciudad in ciudades:
        return ciudades[ciudad]

    print("Ciudad no disponible en la lista.")
    print("Ciudades disponibles:")
    for nombre in ciudades:
        print("-", nombre.title())

    return None


while True:

    origen = input("\nCiudad de Origen (o 'v' para salir): ")

    if origen.lower() == "v":
        print("Programa finalizado.")
        break

    destino = input("Ciudad de Destino (o 'v' para salir): ")

    if destino.lower() == "v":
        print("Programa finalizado.")
        break

    origen_coord = obtener_coordenadas(origen)
    destino_coord = obtener_coordenadas(destino)

    if origen_coord is None or destino_coord is None:
        continue

    print("\nSeleccione el tipo de transporte:")
    print("1. Auto")
    print("2. Bicicleta")
    print("3. Caminando")

    opcion = input("Ingrese una opción: ")

    perfiles = {
        "1": "car",
        "2": "bike",
        "3": "foot"
    }

    if opcion not in perfiles:
        print("Opción de transporte no válida.")
        continue

    perfil = perfiles[opcion]

    url = "https://graphhopper.com/api/1/route"

    parametros = {
        "point": [
            f"{origen_coord[0]},{origen_coord[1]}",
            f"{destino_coord[0]},{destino_coord[1]}"
        ],
        "profile": perfil,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    respuesta = requests.get(url, params=parametros)

    if respuesta.status_code != 200:
        print("\nError al consultar GraphHopper:")
        print(respuesta.text)
        continue

    datos = respuesta.json()
    ruta = datos["paths"][0]

    distancia_km = ruta["distance"] / 1000
    distancia_millas = distancia_km * 0.621371
    duracion_minutos = ruta["time"] / 60000

    print("\n========== RESULTADO ==========")
    print(f"Origen: {origen.title()}")
    print(f"Destino: {destino.title()}")
    print(f"Transporte: {perfil}")
    print(f"Duración: {duracion_minutos:.2f} minutos")
    print(f"Distancia: {distancia_km:.2f} km")
    print(f"Distancia: {distancia_millas:.2f} millas")

    print("\n========== NARRATIVA DE LA RUTA ==========")

    for instruccion in ruta["instructions"]:
        print(instruccion["text"])
