import os

LARGO_ID = 10
LARGO_NOMBRE = 40
LARGO_TELEFONO = 15
LARGO_CORREO = 40
LARGO_CIUDAD = 44
TAMANO_REGISTRO = 150

def formatear_registro(id_val, nombre, telefono, correo, ciudad):

    id_str = str(id_val).ljust(LARGO_ID)[:LARGO_ID]
    nom_str = str(nombre).ljust(LARGO_NOMBRE)[:LARGO_NOMBRE]
    tel_str = str(telefono).ljust(LARGO_TELEFONO)[:LARGO_TELEFONO]
    cor_str = str(correo).ljust(LARGO_CORREO)[:LARGO_CORREO]
    ciu_str = str(ciudad).ljust(LARGO_CIUDAD)[:LARGO_CIUDAD]

    return f"{id_str}{nom_str}{tel_str}{cor_str}{ciu_str}\n"


def inicializar_archivo(ruta):
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as archivo:
            pass


def agregar_contacto(ruta, numero_registro, id_val, nombre, telefono, correo, ciudad):
    registro = formatear_registro(id_val, nombre, telefono, correo, ciudad)

    with open(ruta, "r+", encoding="utf-8") as archivo:
        posicion = numero_registro * TAMANO_REGISTRO
        archivo.seek(posicion)

        print(f"Escribiendo registro en la posición del archivo (bytes): {archivo.tell()}")
        archivo.write(registro)


def leer_contacto(ruta, numero_registro):

    with open(ruta, "r", encoding="utf-8") as archivo:
        posicion = numero_registro * TAMANO_REGISTRO
        archivo.seek(posicion)

        datos = archivo.read(TAMANO_REGISTRO)

        if datos and len(datos) >= (TAMANO_REGISTRO - 1):
            id_val = datos[0:10].strip()
            nombre = datos[10:50].strip()
            telefono = datos[50:65].strip()
            correo = datos[65:105].strip()
            ciudad = datos[105:149].strip()

            return {
                "id": int(id_val),
                "nombre": nombre,
                "telefono": telefono,
                "correo": correo,
                "ciudad": ciudad
            }
        return None

def modificar_contacto(ruta, numero_registro, id_val, nombre, telefono, correo, ciudad):
    registro = formatear_registro(id_val, nombre, telefono, correo, ciudad)

    with open(ruta, "r+", encoding="utf-8") as archivo:
        posicion = numero_registro * TAMANO_REGISTRO
        archivo.seek(posicion)
        archivo.write(registro)