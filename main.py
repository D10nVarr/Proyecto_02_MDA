import sys
from PySide6.QtWidgets import QApplication
from src.gui.ventana_principal import VentanaPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Creamos y mostramos la ventana principal
    ventana = VentanaPrincipal()
    ventana.show()

    # Iniciamos el bucle de eventos de la aplicación
    sys.exit(app.exec())