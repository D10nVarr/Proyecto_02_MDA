import os
import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtGui import QAction, QFont
from PySide6.QtCore import Qt

from src.logic.administrador_registros import agregar_contacto, leer_contacto, modificar_contacto, inicializar_archivo
from src.logic.gestor_indice import cargar_indice, guardar_indice, obtener_siguiente_registro
from src.logic.verificador_hash import verificar_integridad, actualizar_seguridad
from src.utils.generador_reportes import exportar_a_json, generar_reporte_pdf
from src.utils.creador_reportes import crear_respaldo_zip, obtener_informacion_archivo

from src.gui.vistas_secundarias import DialogoContacto, DialogoBuscar


RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if RAIZ not in sys.path:
    sys.path.append(RAIZ)

from tests.test_registros import ejecutar_pruebas_gui


DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = os.path.abspath(os.path.join(DIRECTORIO_ACTUAL, "..", ".."))

CARPETA_DATA = os.path.join(RAIZ_PROYECTO, "data")
CARPETA_EXPORTS = os.path.join(RAIZ_PROYECTO, "exports")

RUTA_DATOS = os.path.join(CARPETA_DATA, "contactos.dat")
RUTA_INDICE = os.path.join(CARPETA_DATA, "indice.json")
RUTA_HASH = os.path.join(CARPETA_DATA, "contactos.sha256")
RUTA_JSON_EXPORT = os.path.join(CARPETA_EXPORTS, "exportacion.json")
RUTA_PDF = os.path.join(CARPETA_EXPORTS, "reporte_contactos.pdf")
RUTA_ZIP = os.path.join(CARPETA_EXPORTS, "respaldo.zip")


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agenda de Contactos - Proyecto 2")
        self.resize(600, 400)

        # Creación de carpetas en la raíz
        os.makedirs(CARPETA_DATA, exist_ok=True)
        os.makedirs(CARPETA_EXPORTS, exist_ok=True)

        inicializar_archivo(RUTA_DATOS)
        self.indice = cargar_indice(RUTA_INDICE)

        self._configurar_ui()
        self._configurar_menus()
        self._verificar_integridad_inicio()

    def _configurar_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        titulo = QLabel("Sistema de Agenda de Contactos")
        titulo.setFont(QFont("Arial", 18, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        sub = QLabel("-------------------------------------------------")
        sub.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(titulo)
        layout.addWidget(sub)
        layout.addStretch()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _configurar_menus(self):
        menu = self.menuBar()

        m_contactos = menu.addMenu("Contactos")
        a_agregar = QAction("Agregar Contacto", self)
        a_agregar.triggered.connect(self.agregar_contacto_gui)
        m_contactos.addAction(a_agregar)

        a_buscar = QAction("Buscar / Modificar por ID", self)
        a_buscar.triggered.connect(self.buscar_modificar_gui)
        m_contactos.addAction(a_buscar)

        m_exportar = menu.addMenu("Exportar")
        a_pdf = QAction("Exportar a JSON y PDF", self)
        a_pdf.triggered.connect(self.exportar_datos_gui)
        m_exportar.addAction(a_pdf)

        m_herramientas = menu.addMenu("Herramientas")
        a_integridad = QAction("Verificar Integridad", self)
        a_integridad.triggered.connect(self._verificar_integridad_inicio)
        m_herramientas.addAction(a_integridad)

        a_respaldo = QAction("Crear Respaldo ZIP", self)
        a_respaldo.triggered.connect(self.crear_respaldo_gui)
        m_herramientas.addAction(a_respaldo)

        a_info = QAction("Información del Archivo", self)
        a_info.triggered.connect(self.info_archivo_gui)
        m_herramientas.addAction(a_info)

        m_herramientas.addSeparator()
        a_test = QAction("Ejecutar Pruebas (Test Registros)", self)
        a_test.triggered.connect(self.ejecutar_pruebas_unitarias)
        m_herramientas.addAction(a_test)

        m_ayuda = menu.addMenu("Ayuda")
        a_acerca = QAction("Acerca de...", self)
        a_acerca.triggered.connect(
            lambda: QMessageBox.information(self, "Ayuda", "Sistema de Agenda con Acceso Aleatorio.\nProyecto 2 - MDA"))
        m_ayuda.addAction(a_acerca)

    def _verificar_integridad_inicio(self):
        estado = verificar_integridad(RUTA_DATOS, RUTA_HASH)
        if estado is False:
            QMessageBox.critical(self, "Alerta de Seguridad",
                                 "El archivo de contactos fue modificado externamente.\nEl Hash SHA-256 no coincide.")
        elif estado is True:
            QMessageBox.information(self, "Integridad", "El archivo de contactos está íntegro y seguro.")

    def agregar_contacto_gui(self):
        dialogo = DialogoContacto(self)
        if dialogo.exec():
            datos = dialogo.obtener_datos()
            id_str = str(datos["id"])
            if id_str in self.indice:
                QMessageBox.warning(self, "Error", "El ID ya existe en el índice.")
                return

            num_registro = obtener_siguiente_registro(self.indice)
            agregar_contacto(RUTA_DATOS, num_registro, datos["id"], datos["nombre"],
                             datos["telefono"], datos["correo"], datos["ciudad"])

            self.indice[id_str] = num_registro
            guardar_indice(RUTA_INDICE, self.indice)
            actualizar_seguridad(RUTA_DATOS, RUTA_HASH)
            QMessageBox.information(self, "Éxito", "Contacto agregado correctamente.")

    def buscar_modificar_gui(self):
        dialogo_buscar = DialogoBuscar(self)
        if dialogo_buscar.exec():
            id_buscado = str(dialogo_buscar.obtener_id())
            if id_buscado not in self.indice:
                QMessageBox.warning(self, "No encontrado", f"No existe un contacto con el ID: {id_buscado}")
                return

            num_registro = self.indice[id_buscado]
            contacto_actual = leer_contacto(RUTA_DATOS, num_registro)

            if contacto_actual:
                dialogo_mod = DialogoContacto(self, contacto_actual)
                if dialogo_mod.exec():
                    datos_nuevos = dialogo_mod.obtener_datos()
                    modificar_contacto(RUTA_DATOS, num_registro, datos_nuevos["id"], datos_nuevos["nombre"],
                                       datos_nuevos["telefono"], datos_nuevos["correo"], datos_nuevos["ciudad"])
                    actualizar_seguridad(RUTA_DATOS, RUTA_HASH)
                    QMessageBox.information(self, "Éxito", "Contacto modificado correctamente.")

    def exportar_datos_gui(self):
        if not self.indice:
            QMessageBox.warning(self, "Vacío", "No hay contactos para exportar.")
            return
        contactos_lista = [leer_contacto(RUTA_DATOS, num) for id_val, num in self.indice.items()]
        exportar_a_json(contactos_lista, RUTA_JSON_EXPORT)
        if generar_reporte_pdf(RUTA_JSON_EXPORT, RUTA_PDF):
            QMessageBox.information(self, "Exportación", f"Archivos JSON y PDF generados con éxito.")

    def crear_respaldo_gui(self):
        t_orig, t_comp = crear_respaldo_zip([RUTA_DATOS, RUTA_INDICE], RUTA_ZIP)
        if t_orig > 0:
            QMessageBox.information(self, "Respaldo ZIP",
                                    f"Respaldo creado.\nTamaño Original: {t_orig} bytes\nTamaño Comprimido: {t_comp} bytes")
        else:
            QMessageBox.warning(self, "Error", "No se encontraron archivos para respaldar.")

    def info_archivo_gui(self):
        info = obtener_informacion_archivo(RUTA_DATOS)
        if info:
            m = f"Nombre: {info['nombre']}\nTamaño: {info['tamano_bytes']} bytes\nModificación: {info['ultima_modificacion']}\nLectura: {info['lectura']}\nEscritura: {info['escritura']}"
            QMessageBox.information(self, "Info del Archivo", m)

    def ejecutar_pruebas_unitarias(self):
        resultado = ejecutar_pruebas_gui()
        QMessageBox.information(self, "Reporte de Pruebas", resultado)