# Proyecto 2: Agenda de Contactos con Acceso Aleatorio

Este proyecto es una aplicación de escritorio desarrollada en Python que administra una agenda de contactos utilizando **archivos de texto con registros de tamaño fijo y acceso aleatorio**. Fue desarrollado como parte de las actividades de la Facultad de Ingeniería de la Universidad Rafael Landívar.

## Características Principales

*   **Acceso Aleatorio (`seek` y `tell`):** Lectura y escritura en el lugar, sin necesidad de recorrer el archivo secuencialmente ni reescribirlo por completo.
*   **Registros de Tamaño Fijo:** Cada contacto ocupa exactamente 150 bytes, logrados mediante un formateo riguroso de cadenas de texto.
*   **Índice Primario:** Implementación de un índice guardado en un archivo JSON que mapea en memoria RAM el ID único de cada contacto con su posición en bytes en el disco.
*   **Verificación de Integridad:** Uso del algoritmo SHA-256 (`hashlib`) para garantizar que el archivo de datos no sea modificado maliciosamente por fuera del programa.
*   **Exportación de Datos:** Capacidad de exportar la agenda a un archivo `.json` y generar un reporte en PDF utilizando `fpdf2`.
*   **Gestión de Respaldos:** Creación de backups comprimidos en formato `.zip` con cálculo de la tasa de compresión.
*   **Metadatos de Sistema:** Lectura en tiempo real del peso del archivo, permisos de sistema (lectura/escritura) y fecha de última modificación usando `os` y `pathlib`.
*   **Pruebas Unitarias:** Incluye un módulo de `unittest` ejecutable desde la interfaz para garantizar matemáticamente que los registros miden exactamente lo estipulado.

## Estructura del Proyecto

```text
Proyecto2_MDA/
├── data/                       # Archivos de persistencia generados por la app
│   ├── contactos.dat           # Base de datos principal de tamaño fijo
│   ├── contactos.sha256        # Archivo de seguridad con el hash
│   └── indice.json             # Índice primario guardado en disco
├── docs/                       # Documentación técnica
│   └── Manual_Proyecto2.pdf
├── exports/                    # Reportes y copias de seguridad
│   ├── exportacion.json
│   ├── reporte_contactos.pdf
│   └── respaldo.zip
├── src/                        # Código fuente
│   ├── gui/                    # Módulo de interfaz gráfica (PySide6)
│   ├── logic/                  # Lógica de negocio e integridad
│   └── utils/                  # Herramientas de compresión y reporte
├── tests/                      # Módulo de pruebas unitarias
│   └── test_registros.py
├── README.md
└── main.py                 # Punto de arranque de la aplicación
```

## Requisitos Previos e Instalación

Para ejecutar este proyecto, es necesario tener instalado Python 3.10 o superior. 
Las dependencias externas utilizadas para la interfaz gráfica y la generación de PDFs son **PySide6** y **fpdf2**.

Puedes instalar las dependencias ejecutando el siguiente comando en tu terminal:

```bash
pip install PySide6 fpdf2
```

## Cómo ejecutar el proyecto

Para evitar problemas ubicarse en el archivo main.py