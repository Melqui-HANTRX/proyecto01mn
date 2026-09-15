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