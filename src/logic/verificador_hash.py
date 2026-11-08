import hashlib
import os


def calcular_hash_archivo(ruta):

    if not os.path.exists(ruta):
        return None

    sha256 = hashlib.sha256()
    with open(ruta, "rb") as archivo:
        while True:
            bloque = archivo.read(4096)
            if not bloque:
                break
            sha256.update(bloque)

    return sha256.hexdigest()


def guardar_hash(ruta_hash, hash_calculado):
    if hash_calculado:
        with open(ruta_hash, "w", encoding="utf-8") as archivo:
            archivo.write(hash_calculado)


def leer_hash(ruta_hash):

    if not os.path.exists(ruta_hash):
        return None
    with open(ruta_hash, "r", encoding="utf-8") as archivo:
        return archivo.read().strip()


def verificar_integridad(ruta_datos, ruta_hash):
    hash_almacenado = leer_hash(ruta_hash)
    hash_actual = calcular_hash_archivo(ruta_datos)

    if not hash_almacenado or not hash_actual:
        return None

    return hash_actual == hash_almacenado


def actualizar_seguridad(ruta_datos, ruta_hash):
    nuevo_hash = calcular_hash_archivo(ruta_datos)
    guardar_hash(ruta_hash, nuevo_hash)