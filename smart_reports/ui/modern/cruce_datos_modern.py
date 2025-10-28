"""
Panel Cruce de Datos Modern - Diseño Oscuro
Drag & Drop con diseño oscuro
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from smart_reports.config.settings_modern import get_color_modern, get_font_modern, get_button_config_modern

try:
    from tkinterdnd2 import DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class CruceDatosModern(ctk.CTkFrame):
    """Panel de Cruce de Datos con diseño oscuro"""

    def __init__(self, parent, db=None):
        super().__init__(parent, fg_color=get_color_modern('background'))
        self.db = db
        self.current_file = None
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_interface()

    def _create_interface(self):
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color='transparent', corner_radius=0)
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(scroll_frame, text='🔄 Cruce de Datos',
                                   font=get_font_modern('title', 28, 'bold'),
                                   text_color=get_color_modern('text_primary'), anchor='w')
        title_label.pack(fill='x', pady=(0, 10))

        subtitle_label = ctk.CTkLabel(scroll_frame, text='Carga de archivos Excel para actualización de datos',
                                      font=get_font_modern('body', 12),
                                      text_color=get_color_modern('text_secondary'), anchor='w')
        subtitle_label.pack(fill='x', pady=(0, 30))

        # Drop area
        self._create_drop_area(scroll_frame)
        
        # File info
        self._create_file_info(scroll_frame)
        
        # Action buttons
        self._create_action_buttons(scroll_frame)
        
        # Progress
        self._create_progress_section(scroll_frame)

    def _create_drop_area(self, parent):
        self.drop_frame = ctk.CTkFrame(parent, fg_color=get_color_modern('surface'), border_width=2,
                                      border_color=get_color_modern('accent_primary'), corner_radius=15,
                                      width=700, height=250)
        self.drop_frame.pack(pady=30)
        self.drop_frame.pack_propagate(False)

        icon_label = ctk.CTkLabel(self.drop_frame, text='📁', font=('Segoe UI', 72),
                                  text_color=get_color_modern('accent_primary'))
        icon_label.pack(pady=(40, 10))

        text_label = ctk.CTkLabel(self.drop_frame, text='Arrastra aquí el archivo Excel\no haz clic para seleccionar',
                                 font=get_font_modern('heading', 16), text_color=get_color_modern('text_primary'),
                                 justify='center')
        text_label.pack(pady=(0, 10))

        formats_label = ctk.CTkLabel(self.drop_frame, text='Formatos soportados: .xlsx, .xls',
                                     font=get_font_modern('small', 10), text_color=get_color_modern('text_secondary'))
        formats_label.pack()

        if DND_AVAILABLE:
            try:
                self.drop_frame.drop_target_register(DND_FILES)
                self.drop_frame.dnd_bind('<<Drop>>', self._on_drop_file)
            except:
                pass

        self.drop_frame.bind('<Button-1>', lambda e: self._select_file())
        icon_label.bind('<Button-1>', lambda e: self._select_file())
        text_label.bind('<Button-1>', lambda e: self._select_file())
        self.drop_frame.configure(cursor='hand2')

    def _create_file_info(self, parent):
        self.info_frame = ctk.CTkFrame(parent, fg_color=get_color_modern('surface'), border_width=1,
                                      border_color=get_color_modern('border'), corner_radius=10)
        self.info_frame.pack(fill='x', pady=20)

        info_title = ctk.CTkLabel(self.info_frame, text='Información del Archivo',
                                 font=get_font_modern('heading', 14, 'bold'),
                                 text_color=get_color_modern('text_primary'))
        info_title.pack(pady=(15, 10), padx=20, anchor='w')

        self.file_info_label = ctk.CTkLabel(self.info_frame, text='No hay archivo cargado',
                                           font=get_font_modern('body', 12),
                                           text_color=get_color_modern('text_secondary'), anchor='w', justify='left')
        self.file_info_label.pack(pady=(0, 15), padx=20, anchor='w')

    def _create_action_buttons(self, parent):
        buttons_frame = ctk.CTkFrame(parent, fg_color='transparent')
        buttons_frame.pack(fill='x', pady=10)

        btn_config = get_button_config_modern('primary')
        self.btn_process = ctk.CTkButton(buttons_frame, text='Procesar Archivo', **btn_config,
                                        width=200, height=45, state='disabled', command=self._process_file)
        self.btn_process.pack(side='left', padx=10)

        btn_config_secondary = get_button_config_modern('secondary')
        self.btn_clear = ctk.CTkButton(buttons_frame, text='Limpiar', **btn_config_secondary,
                                      width=150, height=45, state='disabled', command=self._clear_file)
        self.btn_clear.pack(side='left', padx=10)

    def _create_progress_section(self, parent):
        self.progress_frame = ctk.CTkFrame(parent, fg_color=get_color_modern('surface'), border_width=1,
                                          border_color=get_color_modern('border'), corner_radius=10)
        self.progress_frame.pack(fill='x', pady=20)

        progress_title = ctk.CTkLabel(self.progress_frame, text='Progreso del Procesamiento',
                                      font=get_font_modern('heading', 14, 'bold'),
                                      text_color=get_color_modern('text_primary'))
        progress_title.pack(pady=(15, 10), padx=20, anchor='w')

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=600, height=20, corner_radius=10,
                                              fg_color=get_color_modern('surface_light'),
                                              progress_color=get_color_modern('accent_green'))
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(self.progress_frame, text='Esperando archivo...',
                                          font=get_font_modern('body', 12),
                                          text_color=get_color_modern('text_secondary'))
        self.progress_label.pack(pady=(0, 15))

    def _on_drop_file(self, event):
        file_path = event.data.strip('{}').strip()
        self._load_file(file_path)

    def _select_file(self):
        file_path = filedialog.askopenfilename(title='Seleccionar archivo Excel',
                                              filetypes=[('Excel files', '*.xlsx *.xls'), ('All files', '*.*')])
        if file_path:
            self._load_file(file_path)

    def _load_file(self, file_path):
        import os
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"El archivo no existe:\n{file_path}")
            return
        
        if not file_path.lower().endswith(('.xlsx', '.xls')):
            messagebox.showerror("Error", "Formato no soportado.\nSolo .xlsx, .xls")
            return
        
        self.current_file = file_path
        filename = os.path.basename(file_path)
        filesize = os.path.getsize(file_path) / 1024
        
        self.file_info_label.configure(text=f'📄 Archivo: {filename}\n📊 Tamaño: {filesize:.1f} KB\n📁 Ruta: {file_path}',
                                       text_color=get_color_modern('text_primary'))
        self.btn_process.configure(state='normal')
        self.btn_clear.configure(state='normal')
        self.progress_label.configure(text=f'Archivo cargado: {filename}',
                                     text_color=get_color_modern('accent_green'))
        
        messagebox.showinfo("Archivo Cargado", f"Archivo cargado exitosamente:\n\n{filename}")

    def _clear_file(self):
        self.current_file = None
        self.file_info_label.configure(text='No hay archivo cargado', text_color=get_color_modern('text_secondary'))
        self.btn_process.configure(state='disabled')
        self.btn_clear.configure(state='disabled')
        self.progress_bar.set(0)
        self.progress_label.configure(text='Esperando archivo...', text_color=get_color_modern('text_secondary'))

    def _process_file(self):
        if not self.current_file:
            messagebox.showwarning("Advertencia", "No hay archivo cargado")
            return
        
        messagebox.showinfo("Procesamiento", "Funcionalidad de procesamiento en desarrollo.")
        self._clear_file()
