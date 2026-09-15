import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
from Logica import GestorConfiguracion

# descargamos PIL (Pillow) para manejar imágenes JPG/PNG
try:
    from PIL import Image, ImageTk

    HAS_PIL = True
except ImportError:
    Image = None
    ImageTk = None
    HAS_PIL = False


class AppPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Manejo de Archivos - Proyecto 1")
        self.geometry("1000x600")
        self.configure(bg="#f0f2f5")

        self.gestor = GestorConfiguracion()
        self.configuracion = None

        # Declaración de atributos de instancia para cumplir
        self.inicio_frame = None
        self.main_frame = None
        self.lbl_titulo = None
        self.lbl_subtitulo = None
        self.lbl_imagen = None
        self.foto_tk = None

        self.construir_pantalla_inicio()
    def obtener_texto(self, clave):
        """Diccionario de traducción dinámico."""
        idioma = self.configuracion.get("idioma", "es").lower()
        es_ingles = "en" in idioma

        diccionario = {
            "bienvenido": "Welcome to the System" if es_ingles else "Bienvenido al Sistema",
            "subtitulo": "The program has started successfully with the chosen configuration." if es_ingles else "El programa ha iniciado correctamente con la configuración elegida.",
            "menu_archivo": "File" if es_ingles else "Archivo",
            "menu_edicion": "Edit" if es_ingles else "Edición",
            "menu_ver": "View" if es_ingles else "Ver",
            "menu_nuevo": "New (Simulated)" if es_ingles else "Nuevo (Simulado)",
            "menu_abrir": "Open (Simulated)" if es_ingles else "Abrir (Simulado)",
            "menu_copiar": "Copy (Simulated)" if es_ingles else "Copiar (Simulado)",
            "menu_zoom": "Zoom (Simulated)" if es_ingles else "Zoom (Simulado)",
            "alerta_titulo": "Simulated Option" if es_ingles else "Opción Simulada",
            "alerta_texto": "This option is simulated to comply with the rubric." if es_ingles else "Esta opción es simulada para cumplir con la rúbrica."
        }
        return diccionario.get(clave, "")

    def construir_pantalla_inicio(self):
        self.inicio_frame = tk.Frame(self, bg="#f0f2f5")
        self.inicio_frame.pack(expand=True, fill="both")

        tarjeta = tk.Frame(self.inicio_frame, bg="white", highlightbackground="#d0d0d0", highlightthickness=1)
        tarjeta.pack(expand=True, padx=40, pady=40)

        frame_textos = tk.Frame(tarjeta, bg="white")
        frame_textos.pack(padx=60, pady=(40, 20))

        tk.Label(frame_textos, text="Configuración Inicial", font=("Segoe UI", 18, "bold"), bg="white",
                 fg="#000000").pack(pady=(0, 5))
        tk.Label(frame_textos, text="¿Qué configuración deseas cargar para iniciar el sistema?", font=("Segoe UI", 11),
                 bg="white", fg="#555555").pack()

        frame_botones = tk.Frame(tarjeta, bg="white")
        frame_botones.pack(padx=60, pady=(0, 40))

        tk.Button(frame_botones, text="Usar Base por Defecto", font=("Segoe UI", 10, "bold"), fg="#2b579a", bg="white",
                  relief="flat", cursor="hand2", command=self.iniciar_con_defecto).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cargar Archivo", font=("Segoe UI", 10, "bold"), fg="white", bg="#2b579a",
                  relief="flat", cursor="hand2", padx=20, pady=8, command=self.iniciar_con_archivo).pack(side="left",
                                                                                                         padx=10)

    def iniciar_con_defecto(self):
        self.configuracion = self.gestor.configuracion_defecto.copy()
        self.transicion_a_principal()

    def iniciar_con_archivo(self):
        ruta = filedialog.askopenfilename(title="Selecciona tu archivo de configuración",
                                          filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")])
        if ruta:
            self.configuracion, estado = self.gestor.cargar_configuracion(ruta_archivo=ruta)
            if estado == "invalido":
                messagebox.showwarning("Archivo Corrupto",
                                       "El archivo seleccionado está corrupto. Iniciando con valores por defecto.")
            elif estado == "sin_permisos":
                messagebox.showerror("Sin Permisos",
                                     "No tienes permisos de lectura sobre ese archivo. Iniciando con valores por defecto.")
            self.transicion_a_principal()

    def transicion_a_principal(self):
        if self.inicio_frame:
            self.inicio_frame.destroy()
        self.crear_menu()
        self.construir_pantalla_principal()
        self.aplicar_estilos_generales()

    def aplicar_estilos_generales(self):
        bg_color = "#2b2b2b" if self.configuracion["tema_interfaz"] == "oscuro" else "#ffffff"
        self.configure(bg=bg_color)
        if self.main_frame:
            self.main_frame.configure(bg=bg_color)
        if self.lbl_titulo:
            self.lbl_titulo.configure(bg=bg_color)
        if self.lbl_subtitulo:
            self.lbl_subtitulo.configure(bg=bg_color,
                                         fg="#bbbbbb" if self.configuracion["tema_interfaz"] == "oscuro" else "#555555")
        if self.lbl_imagen:
            self.lbl_imagen.configure(bg=bg_color)
