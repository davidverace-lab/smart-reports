"""
Panel Cruce de Datos Hutchison
Panel para cargar archivos Excel con Drag & Drop
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from smart_reports.config.settings_hutchison import (
    get_color,
    get_font,
    get_button_config
)

# Verificar si tkinterdnd2 está disponible
try:
    from tkinterdnd2 import DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class CruceDatosHutchison(ctk.CTkFrame):
    """
    Panel de Cruce de Datos (antes "Actualizar Datos")

    Características:
    - Drag & Drop de archivos Excel
    - Click para seleccionar archivo
    - Procesamiento de archivos Transcript Status
    - Progreso visual
    """

    def __init__(self, parent, db=None):
        """
        Args:
            parent: Widget padre
            db: Conexión a base de datos
        """
        super().__init__(parent, fg_color=get_color('White'))

        self.db = db
        self.current_file = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_interface()

    def _create_interface(self):
        """Crear interfaz del panel"""

        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent',
            corner_radius=0
        )
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # === TÍTULO ===
        title_label = ctk.CTkLabel(
            scroll_frame,
            text='🔄 Cruce de Datos',
            font=get_font('title', 28, 'bold'),
            text_color=get_color('Sea Blue'),
            anchor='w'
        )
        title_label.pack(fill='x', pady=(0, 10))

        subtitle_label = ctk.CTkLabel(
            scroll_frame,
            text='Carga de archivos Excel para actualización de datos',
            font=get_font('body', 12),
            text_color=get_color('Medium Gray'),
            anchor='w'
        )
        subtitle_label.pack(fill='x', pady=(0, 30))

        # === DRAG & DROP AREA ===
        self._create_drop_area(scroll_frame)

        # === INFORMACIÓN DEL ARCHIVO ===
        self._create_file_info(scroll_frame)

        # === BOTONES DE ACCIÓN ===
        self._create_action_buttons(scroll_frame)

        # === PROGRESO ===
        self._create_progress_section(scroll_frame)

    def _create_drop_area(self, parent):
        """Crear área de Drag & Drop"""

        # Frame para Drag & Drop
        self.drop_frame = ctk.CTkFrame(
            parent,
            fg_color=get_color('Light Gray'),
            border_width=2,
            border_color=get_color('Sky Blue'),
            corner_radius=15,
            width=700,
            height=250
        )
        self.drop_frame.pack(pady=30)
        self.drop_frame.pack_propagate(False)

        # Icono y texto
        icon_label = ctk.CTkLabel(
            self.drop_frame,
            text='📁',
            font=('Segoe UI', 72),
            text_color=get_color('Sky Blue')
        )
        icon_label.pack(pady=(40, 10))

        text_label = ctk.CTkLabel(
            self.drop_frame,
            text='Arrastra aquí el archivo Excel\no haz clic para seleccionar',
            font=get_font('heading', 16),
            text_color=get_color('Sea Blue'),
            justify='center'
        )
        text_label.pack(pady=(0, 10))

        formats_label = ctk.CTkLabel(
            self.drop_frame,
            text='Formatos soportados: .xlsx, .xls',
            font=get_font('small', 10),
            text_color=get_color('Medium Gray')
        )
        formats_label.pack()

        # Registrar área para drag & drop si está disponible
        if DND_AVAILABLE:
            try:
                self.drop_frame.drop_target_register(DND_FILES)
                self.drop_frame.dnd_bind('<<Drop>>', self._on_drop_file)
            except:
                print("⚠️  No se pudo registrar Drag & Drop")

        # Click para abrir file dialog
        self.drop_frame.bind('<Button-1>', lambda e: self._select_file())
        icon_label.bind('<Button-1>', lambda e: self._select_file())
        text_label.bind('<Button-1>', lambda e: self._select_file())
        formats_label.bind('<Button-1>', lambda e: self._select_file())

        # Cursor pointer
        self.drop_frame.configure(cursor='hand2')

    def _create_file_info(self, parent):
        """Crear sección de información del archivo"""

        self.info_frame = ctk.CTkFrame(
            parent,
            fg_color=get_color('Surface'),
            border_width=1,
            border_color=get_color('Border'),
            corner_radius=10
        )
        self.info_frame.pack(fill='x', pady=20)

        # Título
        info_title = ctk.CTkLabel(
            self.info_frame,
            text='Información del Archivo',
            font=get_font('heading', 14, 'bold'),
            text_color=get_color('Sea Blue')
        )
        info_title.pack(pady=(15, 10), padx=20, anchor='w')

        # Label de info (se actualiza cuando se carga archivo)
        self.file_info_label = ctk.CTkLabel(
            self.info_frame,
            text='No hay archivo cargado',
            font=get_font('body', 12),
            text_color=get_color('Medium Gray'),
            anchor='w',
            justify='left'
        )
        self.file_info_label.pack(pady=(0, 15), padx=20, anchor='w')

    def _create_action_buttons(self, parent):
        """Crear botones de acción"""

        buttons_frame = ctk.CTkFrame(parent, fg_color='transparent')
        buttons_frame.pack(fill='x', pady=10)

        # Botón Procesar
        btn_config = get_button_config('primary')
        self.btn_process = ctk.CTkButton(
            buttons_frame,
            text='Procesar Archivo',
            **btn_config,
            width=200,
            height=45,
            state='disabled',
            command=self._process_file
        )
        self.btn_process.pack(side='left', padx=10)

        # Botón Limpiar
        btn_config_secondary = get_button_config('secondary')
        self.btn_clear = ctk.CTkButton(
            buttons_frame,
            text='Limpiar',
            **btn_config_secondary,
            width=150,
            height=45,
            state='disabled',
            command=self._clear_file
        )
        self.btn_clear.pack(side='left', padx=10)

    def _create_progress_section(self, parent):
        """Crear sección de progreso"""

        self.progress_frame = ctk.CTkFrame(
            parent,
            fg_color=get_color('Surface'),
            border_width=1,
            border_color=get_color('Border'),
            corner_radius=10
        )
        self.progress_frame.pack(fill='x', pady=20)

        # Título
        progress_title = ctk.CTkLabel(
            self.progress_frame,
            text='Progreso del Procesamiento',
            font=get_font('heading', 14, 'bold'),
            text_color=get_color('Sea Blue')
        )
        progress_title.pack(pady=(15, 10), padx=20, anchor='w')

        # Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=600,
            height=20,
            corner_radius=10,
            fg_color=get_color('Light Gray'),
            progress_color=get_color('Success Green')
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

        # Label de estado
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text='Esperando archivo...',
            font=get_font('body', 12),
            text_color=get_color('Medium Gray')
        )
        self.progress_label.pack(pady=(0, 15))

    def _on_drop_file(self, event):
        """Manejar evento de soltar archivo"""
        file_path = event.data

        # Limpiar path (tkinterdnd2 puede agregar caracteres extra)
        file_path = file_path.strip('{}').strip()

        self._load_file(file_path)

    def _select_file(self):
        """Abrir diálogo para seleccionar archivo"""
        file_path = filedialog.askopenfilename(
            title='Seleccionar archivo Excel',
            filetypes=[
                ('Excel files', '*.xlsx *.xls'),
                ('All files', '*.*')
            ]
        )

        if file_path:
            self._load_file(file_path)

    def _load_file(self, file_path):
        """Cargar archivo seleccionado"""
        import os

        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"El archivo no existe:\n{file_path}")
            return

        # Validar extensión
        if not file_path.lower().endswith(('.xlsx', '.xls')):
            messagebox.showerror(
                "Error",
                "Formato de archivo no soportado.\n\n"
                "Solo se aceptan archivos Excel (.xlsx, .xls)"
            )
            return

        # Guardar archivo actual
        self.current_file = file_path

        # Actualizar UI
        filename = os.path.basename(file_path)
        filesize = os.path.getsize(file_path) / 1024  # KB

        self.file_info_label.configure(
            text=f'📄 Archivo: {filename}\n'
                 f'📊 Tamaño: {filesize:.1f} KB\n'
                 f'📁 Ruta: {file_path}',
            text_color=get_color('Dark Gray')
        )

        # Habilitar botones
        self.btn_process.configure(state='normal')
        self.btn_clear.configure(state='normal')

        # Actualizar progreso
        self.progress_label.configure(
            text=f'Archivo cargado: {filename}',
            text_color=get_color('Success Green')
        )

        messagebox.showinfo(
            "Archivo Cargado",
            f"Archivo cargado exitosamente:\n\n{filename}\n\n"
            "Haz clic en 'Procesar Archivo' para continuar."
        )

    def _clear_file(self):
        """Limpiar archivo cargado"""
        self.current_file = None

        # Resetear UI
        self.file_info_label.configure(
            text='No hay archivo cargado',
            text_color=get_color('Medium Gray')
        )

        self.btn_process.configure(state='disabled')
        self.btn_clear.configure(state='disabled')

        self.progress_bar.set(0)
        self.progress_label.configure(
            text='Esperando archivo...',
            text_color=get_color('Medium Gray')
        )

    def _process_file(self):
        """Procesar archivo cargado"""
        if not self.current_file:
            messagebox.showwarning("Advertencia", "No hay archivo cargado")
            return

        if not self.db:
            messagebox.showerror(
                "Error",
                "No hay conexión a la base de datos.\n"
                "El procesamiento requiere conexión activa."
            )
            return

        # Simulación de procesamiento
        self.progress_label.configure(
            text='Procesando archivo...',
            text_color=get_color('Sky Blue')
        )

        # Simular progreso
        for i in range(11):
            self.progress_bar.set(i / 10)
            self.update()
            import time
            time.sleep(0.1)

        # Completado
        self.progress_bar.set(1.0)
        self.progress_label.configure(
            text='✓ Procesamiento completado exitosamente',
            text_color=get_color('Success Green')
        )

        messagebox.showinfo(
            "Éxito",
            "Archivo procesado exitosamente.\n\n"
            "Funcionalidad completa de procesamiento en desarrollo.\n\n"
            "Se implementará:\n"
            "- Lectura de estructura Excel\n"
            "- Validación de datos\n"
            "- Inserción en base de datos\n"
            "- Reporte de resultados"
        )

        # Limpiar
        self._clear_file()


# Para testing standalone
if __name__ == '__main__':
    root = ctk.CTk()
    root.title("Test Cruce de Datos Hutchison")
    root.geometry("1000x900")

    ctk.set_appearance_mode("light")

    panel = CruceDatosHutchison(root)
    panel.pack(fill='both', expand=True)

    root.mainloop()
