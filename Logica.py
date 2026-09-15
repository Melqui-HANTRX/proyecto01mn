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

            try:
                with open(self.nombre_archivo, "r", encoding="utf-8") as archivo:
                    self.configuracion_actual = json.load(archivo)

                    # Rellena claves faltantes con valores por defecto
                    for key in self.configuracion_defecto:
                        if key not in self.configuracion_actual:
                            self.configuracion_actual[key] = self.configuracion_defecto[key]

                    return self.configuracion_actual, "exito"

            except FileNotFoundError:
                self.configuracion_actual = self.configuracion_defecto.copy()
                return self.configuracion_actual, "no_encontrado"

            except json.JSONDecodeError:
                self.configuracion_actual = self.configuracion_defecto.copy()
                return self.configuracion_actual, "invalido"

            except PermissionError:
                self.configuracion_actual = self.configuracion_defecto.copy()
                return self.configuracion_actual, "sin_permisos"

        def guardar_configuracion(self, datos_configuracion):
            """Patrón de escritura segura usando archivo temporal."""
            try:
                if os.path.exists(self.nombre_archivo):
                    with open(self.nombre_archivo, "r", encoding="utf-8") as original:
                        contenido_anterior = original.read()

                    with open(self.archivo_respaldo, "w", encoding="utf-8") as respaldo:
                        respaldo.write(contenido_anterior)

                with open(self.archivo_temporal, "w", encoding="utf-8") as temporal:
                    json.dump(datos_configuracion, temporal, indent=4, ensure_ascii=False)

                os.replace(self.archivo_temporal, self.nombre_archivo)

                self.configuracion_actual = datos_configuracion.copy()
                return True

            except Exception as e:
                # Imprime el error para que la variable 'e' sea utilizada y no marque advertencia
                print(f"Fallo crítico al guardar (capturado por seguridad): {e}")
                if os.path.exists(self.archivo_temporal):
                    os.remove(self.archivo_temporal)
                return False