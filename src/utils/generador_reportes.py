import json
from datetime import datetime
from fpdf import FPDF


def exportar_a_json(contactos_lista, ruta_json):

    with open(ruta_json, "w", encoding="utf-8") as archivo:
        json.dump(contactos_lista, archivo, indent=4, ensure_ascii=False)

    return ruta_json


def generar_reporte_pdf(ruta_json, ruta_pdf):

    try:
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            contactos = json.load(archivo)
    except FileNotFoundError:
        print("El archivo JSON no existe para generar el reporte.")
        return False

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)

    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.cell(0, 10, f"Reporte de Agenda - {fecha_actual}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", size=10)
    for c in contactos:
        texto_linea1 = f"ID: {c['id']} | Nombre: {c['nombre']} | Tel: {c['telefono']}"
        texto_linea2 = f"Correo: {c['correo']} | Ciudad: {c['ciudad']}"

        pdf.cell(0, 8, texto_linea1, new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, texto_linea2, new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 5, "-" * 80, new_x="LMARGIN", new_y="NEXT")

    pdf.output(ruta_pdf)
    return True