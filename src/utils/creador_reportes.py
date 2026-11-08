import os
import zipfile
from pathlib import Path
from datetime import datetime


def crear_respaldo_zip(rutas_origen, ruta_zip):

    tamano_original = 0
    archivos_respaldados = 0


    with zipfile.ZipFile(ruta_zip, "w", compression=zipfile.ZIP_DEFLATED) as zip_archivo:
        for ruta in rutas_origen:
            if os.path.exists(ruta):
                tamano_original += os.path.getsize(ruta)

                zip_archivo.write(ruta, arcname=os.path.basename(ruta))
                archivos_respaldados += 1

    if archivos_respaldados > 0:
        tamano_comprimido = os.path.getsize(ruta_zip)
        return tamano_original, tamano_comprimido
    else:
        return 0, 0


def obtener_informacion_archivo(ruta):

    ruta_path = Path(ruta)
    if not ruta_path.exists():
        return None

    datos = ruta_path.stat()
    fecha_mod = datetime.fromtimestamp(datos.st_mtime).strftime("%d/%m/%Y %H:%M:%S")


    permiso_lectura = os.access(ruta, os.R_OK)
    permiso_escritura = os.access(ruta, os.W_OK)

    return {
        "nombre": ruta_path.name,
        "tamano_bytes": datos.st_size,
        "ultima_modificacion": fecha_mod,
        "lectura": "Sí" if permiso_lectura else "No",
        "escritura": "Sí" if permiso_escritura else "No"
    }