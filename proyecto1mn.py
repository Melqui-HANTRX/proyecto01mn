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

    def accion_simulada(self):
        messagebox.showinfo(self.obtener_texto("alerta_titulo"), self.obtener_texto("alerta_texto"))

    def crear_menu(self):
        menu_bar = tk.Menu(self, bg=self.configuracion.get("color_menu", "#EEEEEE"))

        opciones = [
            (self.obtener_texto("menu_archivo"), [self.obtener_texto("menu_nuevo"), self.obtener_texto("menu_abrir")]),
            (self.obtener_texto("menu_edicion"), [self.obtener_texto("menu_copiar")]),
            (self.obtener_texto("menu_ver"), [self.obtener_texto("menu_zoom")])
        ]

        for menu_name, sub_items in opciones:
            menu_simulado = tk.Menu(menu_bar, tearoff=0)
            for item in sub_items:
                menu_simulado.add_command(label=item, command=self.accion_simulada)
            menu_bar.add_cascade(label=menu_name, menu=menu_simulado)

        menu_bar.add_command(label="Settings", command=self.abrir_settings)
        self.config(menu=menu_bar)

    def construir_pantalla_principal(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")

        try:
            tam_fuente = int(self.configuracion.get("tamanio_fuente", "18"))
        except ValueError:
            tam_fuente = 18

        nombre_usuario = self.configuracion.get('nombre_usuario', 'Usuario')

        self.lbl_titulo = tk.Label(
            self.main_frame,
            text=f"{self.obtener_texto('bienvenido')}, {nombre_usuario}",
            font=("Segoe UI", tam_fuente, "bold"),
            fg=self.configuracion.get("color_letra", "#000000"),
            justify="center"
        )
        self.lbl_titulo.pack(pady=(60, 5))

        self.lbl_subtitulo = tk.Label(
            self.main_frame,
            text=self.obtener_texto("subtitulo"),
            font=("Segoe UI", 10),
            justify="center"
        )
        self.lbl_subtitulo.pack(pady=(0, 20))

        self.lbl_imagen = tk.Label(self.main_frame)
        self.lbl_imagen.pack(pady=(10, 20))

        self.cargar_foto_perfil()

    def cargar_foto_perfil(self):
        ruta_foto = self.configuracion.get("foto_perfil", "")
        bg_color = "#2b2b2b" if self.configuracion["tema_interfaz"] == "oscuro" else "#ffffff"

        if self.lbl_imagen:
            self.lbl_imagen.configure(bg=bg_color)

        if ruta_foto and os.path.exists(ruta_foto):
            if HAS_PIL:
                try:
                    img = Image.open(ruta_foto)
                    img = img.resize((200, 200), Image.Resampling.LANCZOS)
                    self.foto_tk = ImageTk.PhotoImage(img)
                    # noinspection PyTypeChecker
                    self.lbl_imagen.config(image=self.foto_tk, text="")
                except Exception as e:
                    print(f"Error al procesar la imagen: {e}")
                    self.lbl_imagen.config(image="", text="[Error al cargar imagen]", fg="red")
            else:
                self.lbl_imagen.config(image="", text="[Instalar Pillow (PIL) para ver imagen]", fg="red")
        else:
            self.lbl_imagen.config(image="", text="[Sin foto de perfil]", fg="#888888")

    def abrir_settings(self):
        VentanaSettings(self, self.gestor, self.configuracion, self.actualizar_aplicacion)

    def actualizar_aplicacion(self, nueva_configuracion):
        self.configuracion = nueva_configuracion
        self.aplicar_estilos_generales()
        try:
            tam = int(self.configuracion["tamanio_fuente"])
        except ValueError:
            tam = 18

        nombre_usuario = self.configuracion.get('nombre_usuario', 'Usuario')

        if self.lbl_titulo:
            self.lbl_titulo.config(
                text=f"{self.obtener_texto('bienvenido')}, {nombre_usuario}",
                font=("Segoe UI", tam, "bold"),
                fg=self.configuracion["color_letra"]
            )

        if self.lbl_subtitulo:
            self.lbl_subtitulo.config(text=self.obtener_texto("subtitulo"))

        self.crear_menu()
        self.cargar_foto_perfil()


class VentanaSettings(tk.Toplevel):
    def __init__(self, parent, gestor, configuracion_actual, callback_actualizar):
        super().__init__(parent)
        self.title("Ventana de Settings")
        self.geometry("600x550")
        self.grab_set()

        self.gestor = gestor
        self.config = configuracion_actual.copy()
        self.callback_actualizar = callback_actualizar

        self.ent_nombre = None
        self.cmb_tema = None
        self.cmb_idioma = None
        self.ent_fuente = None
        self.ent_cmenu = None
        self.ent_cletra = None
        self.ent_foto = None

        self.construir_formulario()

    def construir_formulario(self):
        form_frame = tk.Frame(self, padx=20, pady=20)
        form_frame.pack(expand=True, fill="both")

        frame_nombre = ttk.LabelFrame(form_frame, text="Nombre Usuario")
        frame_nombre.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.ent_nombre = ttk.Entry(frame_nombre, width=60)
        self.ent_nombre.insert(0, self.config.get("nombre_usuario", ""))
        self.ent_nombre.pack(fill="x", padx=10, pady=10)

        frame_tema = ttk.LabelFrame(form_frame, text="Tema Interfaz")
        frame_tema.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.cmb_tema = ttk.Combobox(frame_tema, values=["claro", "oscuro"], state="readonly")
        self.cmb_tema.set(self.config.get("tema_interfaz", "claro"))
        self.cmb_tema.pack(fill="x", padx=10, pady=10)

        frame_idioma = ttk.LabelFrame(form_frame, text="Idioma")
        frame_idioma.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        self.cmb_idioma = ttk.Combobox(frame_idioma, values=["es", "es-ES", "en", "en-US"], state="readonly")
        self.cmb_idioma.set(self.config.get("idioma", "es-ES"))
        self.cmb_idioma.pack(fill="x", padx=10, pady=10)

        frame_fuente = ttk.LabelFrame(form_frame, text="Tamaño fuente (Número entero)")
        frame_fuente.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.ent_fuente = ttk.Entry(frame_fuente)
        self.ent_fuente.insert(0, str(self.config.get("tamanio_fuente", "12")))
        self.ent_fuente.pack(fill="x", padx=10, pady=10)

        frame_cmenu = ttk.LabelFrame(form_frame, text="Color de Menú")
        frame_cmenu.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        self.ent_cmenu = ttk.Entry(frame_cmenu)
        self.ent_cmenu.insert(0, self.config.get("color_menu", "#EEEEEE"))
        self.ent_cmenu.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        ttk.Button(frame_cmenu, text="🎨", width=3,
                   command=lambda: self.elegir_color("color_menu", self.ent_cmenu)).pack(side="right", padx=(0, 10))

        frame_cletra = ttk.LabelFrame(form_frame, text="Color de Letra")
        frame_cletra.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        self.ent_cletra = ttk.Entry(frame_cletra)
        self.ent_cletra.insert(0, self.config.get("color_letra", "#000000"))
        self.ent_cletra.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        ttk.Button(frame_cletra, text="🎨", width=3,
                   command=lambda: self.elegir_color("color_letra", self.ent_cletra)).pack(side="right", padx=(0, 10))

        frame_foto = ttk.LabelFrame(form_frame, text="Foto de Perfil (Ruta)")
        frame_foto.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.ent_foto = ttk.Entry(frame_foto)
        self.ent_foto.insert(0, self.config.get("foto_perfil", ""))
        self.ent_foto.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        ttk.Button(frame_foto, text="Examinar...", command=self.elegir_foto).pack(side="right", padx=(0, 10), pady=10)

        botones_frame = tk.Frame(self)
        botones_frame.pack(pady=10)
        ttk.Button(botones_frame, text="Cancelar", command=self.destroy).pack(side="left", padx=10)
        ttk.Button(botones_frame, text="Guardar Configuración", command=self.guardar).pack(side="left", padx=10)

    @staticmethod
    def elegir_color(clave, entry_widget):
        color_seleccionado = colorchooser.askcolor(title=f"Seleccionar {clave}")[1]
        if color_seleccionado:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, color_seleccionado)

    def elegir_foto(self):
        ruta = filedialog.askopenfilename(title="Seleccionar foto de perfil",
                                          filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if ruta:
            if self.ent_foto:
                self.ent_foto.delete(0, tk.END)
                self.ent_foto.insert(0, ruta)

    def guardar(self):
        if self.ent_fuente and not self.ent_fuente.get().isdigit():
            messagebox.showerror("Error de Validación", "El tamaño de fuente debe ser un número entero.")
            return

        nueva_config = {
            "nombre_usuario": self.ent_nombre.get() if self.ent_nombre else "",
            "tema_interfaz": self.cmb_tema.get() if self.cmb_tema else "",
            "idioma": self.cmb_idioma.get() if self.cmb_idioma else "",
            "tamanio_fuente": self.ent_fuente.get() if self.ent_fuente else "",
            "color_menu": self.ent_cmenu.get() if self.ent_cmenu else "",
            "color_letra": self.ent_cletra.get() if self.ent_cletra else "",
            "foto_perfil": self.ent_foto.get() if self.ent_foto else ""
        }

        if self.gestor.guardar_configuracion(nueva_config):
            self.callback_actualizar(nueva_config)
            messagebox.showinfo("Éxito", "Configuración guardada de forma segura.")
            self.destroy()
        else:
            messagebox.showerror("Error Crítico", "No se pudo guardar la configuración.")


if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()