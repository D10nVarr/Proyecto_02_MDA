import unittest
import os
import io
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.logic.administrador_registros import formatear_registro, agregar_contacto, leer_contacto, TAMANO_REGISTRO

class TestAdministradorRegistros(unittest.TestCase):
    def setUp(self):
        self.ruta_prueba = "test_contactos.dat"
        if os.path.exists(self.ruta_prueba): os.remove(self.ruta_prueba)
        with open(self.ruta_prueba, "w", encoding="utf-8") as f: pass

    def tearDown(self):
        if os.path.exists(self.ruta_prueba): os.remove(self.ruta_prueba)

    def test_tamano_fijo(self):
        registro = formatear_registro(102030, "Juan Perez", "5555-1234", "juan@correo.com", "Quetzaltenango")
        self.assertEqual(len(registro), TAMANO_REGISTRO)
        self.assertTrue(registro.endswith("\n"))

    def test_acceso_aleatorio(self):
        agregar_contacto(self.ruta_prueba, 0, 101, "Ana Lopez", "1111-2222", "ana@correo.com", "Guatemala")
        agregar_contacto(self.ruta_prueba, 2, 999, "Carlos Perez", "3333-4444", "carlos@correo.com", "Xela")
        contacto = leer_contacto(self.ruta_prueba, 2)
        self.assertEqual(contacto["id"], 999)
        self.assertEqual(contacto["ciudad"], "Xela")

def ejecutar_pruebas_gui():
    stream_salida = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream_salida, verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdministradorRegistros)
    runner.run(suite)
    return stream_salida.getvalue()

if __name__ == "__main__":
    unittest.main()