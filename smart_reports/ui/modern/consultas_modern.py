"""
Panel Consultas Modern - Diseño Oscuro
Consultas con tksheet en modo oscuro
"""

import customtkinter as ctk
from tkinter import messagebox
from smart_reports.config.settings_modern import get_color_modern, get_font_modern, get_button_config_modern


class ConsultasModern(ctk.CTkFrame):
    """Panel de consultas con diseño oscuro"""

    def __init__(self, parent, db=None):
        super().__init__(parent, fg_color=get_color_modern('background'))
        self.db = db
        self.cursor = db.get_cursor() if db else None
        self.sheet = None
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_interface()

    def _create_interface(self):
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color='transparent', corner_radius=0)
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(scroll_frame, text='🔍 Consultas de Usuarios',
                                   font=get_font_modern('title', 28, 'bold'),
                                   text_color=get_color_modern('text_primary'), anchor='w')
        title_label.pack(fill='x', pady=(0, 30))

        # Búsqueda por ID
        self._create_search_section(scroll_frame)
        
        # Tabla
        self._create_results_table(scroll_frame)

    def _create_search_section(self, parent):
        search_frame = ctk.CTkFrame(parent, fg_color=get_color_modern('surface'), border_width=1,
                                   border_color=get_color_modern('border'), corner_radius=10)
        search_frame.pack(fill='x', pady=10)

        container = ctk.CTkFrame(search_frame, fg_color='transparent')
        container.pack(fill='x', padx=20, pady=20)

        label = ctk.CTkLabel(container, text='🔍  Buscar Usuario por ID:',
                            font=get_font_modern('heading', 14, 'bold'),
                            text_color=get_color_modern('text_primary'))
        label.pack(side='left', padx=(0, 15))

        self.search_entry = ctk.CTkEntry(container, placeholder_text='Ingrese User ID...',
                                        font=get_font_modern('body', 12), width=300, height=40,
                                        corner_radius=8, border_width=1, border_color=get_color_modern('border'),
                                        fg_color=get_color_modern('surface_light'))
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_by_id())

        btn_config = get_button_config_modern('primary')
        btn_search = ctk.CTkButton(container, text='Buscar', **btn_config, width=120, height=40,
                                  command=self.search_by_id)
        btn_search.pack(side='left', padx=10)

    def _create_results_table(self, parent):
        table_frame = ctk.CTkFrame(parent, fg_color=get_color_modern('surface'), border_width=1,
                                  border_color=get_color_modern('border'), corner_radius=10)
        table_frame.pack(fill='both', expand=True, pady=20)

        title_label = ctk.CTkLabel(table_frame, text='📊 Resultados',
                                   font=get_font_modern('heading', 16, 'bold'),
                                   text_color=get_color_modern('text_primary'))
        title_label.pack(pady=(15, 10), padx=20, anchor='w')

        self.table_container = ctk.CTkFrame(table_frame, fg_color=get_color_modern('surface_light'), corner_radius=5)
        self.table_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        self.placeholder_label = ctk.CTkLabel(self.table_container, text='Seleccione una consulta para ver los resultados',
                                             font=get_font_modern('body', 14), text_color=get_color_modern('text_secondary'))
        self.placeholder_label.pack(expand=True, pady=50)

    def search_by_id(self):
        user_id = self.search_entry.get().strip()
        if not user_id:
            messagebox.showwarning("Advertencia", "Ingrese un User ID")
            return
        
        # Demo data
        demo_data = [('U001', 'Juan Pérez', 'juan.perez@hutchison.com', 'Operaciones TNG', 14, 12)]
        self._update_table(demo_data)

    def _update_table(self, data):
        try:
            from tksheet import Sheet
            if self.placeholder_label:
                self.placeholder_label.destroy()
                self.placeholder_label = None
            if self.sheet:
                self.sheet.destroy()

            self.sheet = Sheet(self.table_container,
                             headers=['User ID', 'Nombre', 'Email', 'Unidad', 'Total Módulos', 'Completados'],
                             header_bg=get_color_modern('accent_primary'), header_fg='white',
                             header_font=('Montserrat', 11, 'bold'),
                             table_bg=get_color_modern('surface'), table_fg=get_color_modern('text_primary'),
                             table_font=('Arial', 10),
                             index_bg=get_color_modern('surface_light'), index_fg=get_color_modern('text_secondary'),
                             table_selected_cells_bg=get_color_modern('accent_primary'),
                             table_selected_cells_fg='white')
            
            self.sheet.enable_bindings('single_select', 'row_select', 'column_width_resize', 'arrowkeys',
                                      'right_click_popup_menu', 'rc_select', 'copy', 'select_all')
            self.sheet.pack(fill='both', expand=True)
            self.sheet.set_sheet_data(data)
            
            messagebox.showinfo("Éxito", f"Se cargaron {len(data)} registros.")
        except ImportError:
            messagebox.showerror("Error", "tksheet no está instalado.\nInstala con: pip install tksheet")
