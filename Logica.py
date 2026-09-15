import os
import json


class GestorConfiguracion:
    def __init__(self):
        # Nombres por defecto si el "usuario" decide iniciar uno nuevo
        self.nombre_archivo = "config.json"
        self.archivo_respaldo = "config.bak"
        self.archivo_temporal = "config.tmp"

        self.configuracion_defecto = {
            "nombre_usuario": "Usuario",
            "tema_interfaz": "claro",
            "idioma": "es/es-ES",
            "tamanio_fuente": "12",
            "color_menu": "#EEEEEE",
            "color_letra": "#000000",
            "foto_perfil": ""
        }
        self.configuracion_actual = self.configuracion_defecto.copy()

    def cargar_configuracion(self, ruta_archivo=None):
        """Intenta cargar la configuración desde un archivo específico si se provee."""
        if ruta_archivo:
            self.nombre_archivo = ruta_archivo
            base = os.path.splitext(ruta_archivo)[0]
            self.archivo_respaldo = f"{base}.bak"
            self.archivo_temporal = f"{base}.tmp"