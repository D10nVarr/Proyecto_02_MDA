from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox


class DialogoBuscar(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Buscar Contacto")
        self.resize(300, 100)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.input_id = QLineEdit()
        form_layout.addRow("ID a buscar:", self.input_id)

        layout.addLayout(form_layout)

        # Botones
        layout_botones = QHBoxLayout()
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.validar_y_aceptar)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)

        layout_botones.addWidget(btn_buscar)
        layout_botones.addWidget(btn_cancelar)
        layout.addLayout(layout_botones)

        self.setLayout(layout)

    def validar_y_aceptar(self):
        if not self.input_id.text().isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser un número entero.")
            return
        self.accept()

    def obtener_id(self):
        return int(self.input_id.text())


class DialogoContacto(QDialog):
    def __init__(self, parent=None, contacto_existente=None):
        super().__init__(parent)

        self.es_modificacion = contacto_existente is not None
        titulo = "Modificar Contacto" if self.es_modificacion else "Agregar Contacto"
        self.setWindowTitle(titulo)
        self.resize(350, 250)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.input_id = QLineEdit()
        self.input_nombre = QLineEdit()
        self.input_telefono = QLineEdit()
        self.input_correo = QLineEdit()
        self.input_ciudad = QLineEdit()


        if self.es_modificacion:
            self.input_id.setText(str(contacto_existente["id"]))
            self.input_id.setReadOnly(True)
            self.input_nombre.setText(contacto_existente["nombre"])
            self.input_telefono.setText(contacto_existente["telefono"])
            self.input_correo.setText(contacto_existente["correo"])
            self.input_ciudad.setText(contacto_existente["ciudad"])

        form_layout.addRow("ID (Entero, Único):", self.input_id)
        form_layout.addRow("Nombre:", self.input_nombre)
        form_layout.addRow("Teléfono:", self.input_telefono)
        form_layout.addRow("Correo:", self.input_correo)
        form_layout.addRow("Ciudad:", self.input_ciudad)

        layout.addLayout(form_layout)

        # Botones
        layout_botones = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.validar_y_aceptar)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)

        layout_botones.addWidget(btn_guardar)
        layout_botones.addWidget(btn_cancelar)
        layout.addLayout(layout_botones)

        self.setLayout(layout)

    def validar_y_aceptar(self):
        if not self.input_id.text().isdigit():
            QMessageBox.warning(self, "Error", "El ID debe ser un número válido.")
            return

        if not all([self.input_nombre.text(), self.input_telefono.text(),
                    self.input_correo.text(), self.input_ciudad.text()]):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        self.accept()

    def obtener_datos(self):
        return {
            "id": int(self.input_id.text()),
            "nombre": self.input_nombre.text().strip(),
            "telefono": self.input_telefono.text().strip(),
            "correo": self.input_correo.text().strip(),
            "ciudad": self.input_ciudad.text().strip()
        }