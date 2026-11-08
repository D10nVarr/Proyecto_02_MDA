import sys
import os

DIRECTORIO_SRC = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = os.path.abspath(os.path.join(DIRECTORIO_SRC, ".."))

if RAIZ_PROYECTO not in sys.path:
    sys.path.insert(0, RAIZ_PROYECTO)

from PySide6.QtWidgets import QApplication

from src.gui.ventana_principal import VentanaPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())