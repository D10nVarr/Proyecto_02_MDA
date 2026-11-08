import json
import os

def cargar_indice(ruta):

    if not os.path.exists(ruta):
        return {}
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, FileNotFoundError):
        print("El archivo índice estaba corrupto o no existe. Se creará uno nuevo.")
        return {}

def guardar_indice(ruta, indice):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, indent=4)

def obtener_siguiente_registro(indice):

    if not indice:
        return 0
    return len(indice)