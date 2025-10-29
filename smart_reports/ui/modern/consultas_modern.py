"""
Panel Consultas Modern - Implementación Completa
Versión oscura con colores Modern y funcionalidad completa
"""

import customtkinter as ctk
from tkinter import messagebox
from smart_reports.config.settings_modern import (
    get_color_modern,
    get_font_modern
)


class ConsultasModern(ctk.CTkFrame):
    """Panel de consultas completo - Versión Modern"""

    def __init__(self, parent, db=None):
        super().__init__(parent, fg_color=get_color_modern('background'))
        self.db = db
        self.cursor = db.get_cursor() if db else None
        self.sheet = None
        self.advanced_filters_frame = None
        self.show_filters_var = ctk.BooleanVar(value=False)
        self.results_count_label = None
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_interface()

    def _create_interface(self):
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color='transparent')
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        
        title_label = ctk.CTkLabel(scroll_frame, text='Consultas de Usuarios',
                                   font=('Montserrat', 24, 'bold'),
                                   text_color=get_color_modern('text_primary'), anchor='w')
        title_label.pack(fill='x', pady=(0, 20))
        
        self._create_search_by_id(scroll_frame)
        self._create_search_by_unit(scroll_frame)
        self._create_advanced_filters_toggle(scroll_frame)
        self._create_quick_queries(scroll_frame)
        self._create_results_table(scroll_frame)

    def _create_search_by_id(self, parent):
        frame = ctk.CTkFrame(parent, fg_color=get_color_modern('surface_card'),
                            border_width=1, border_color=get_color_modern('border'), corner_radius=10)
        frame.pack(fill='x', pady=(0, 15), padx=5)
        inner = ctk.CTkFrame(frame, fg_color='transparent')
        inner.pack(fill='x', padx=20, pady=15)
        
        label = ctk.CTkLabel(inner, text='🔍  Buscar Usuario por ID:',
                            font=('Montserrat', 13, 'bold'),
                            text_color=get_color_modern('text_primary'))
        label.pack(side='left', padx=(0, 15))
        
        self.id_entry = ctk.CTkEntry(inner, placeholder_text='Ingrese ID de usuario...',
                                     width=300, height=38, font=('Arial', 11),
                                     border_width=1, border_color=get_color_modern('border'),
                                     fg_color=get_color_modern('surface'),
                                     text_color=get_color_modern('text_primary'))
        self.id_entry.pack(side='left', padx=(0, 10))
        self.id_entry.bind('<Return>', lambda e: self.buscar_por_id())
        
        btn_buscar = ctk.CTkButton(inner, text='Buscar', width=120, height=38,
                                   font=('Arial', 11, 'bold'),
                                   fg_color=get_color_modern('Sky Blue'),
                                   hover_color=get_color_modern('Sea Blue'),
                                   text_color='white', corner_radius=8,
                                   command=self.buscar_por_id)
        btn_buscar.pack(side='left')

    def _create_search_by_unit(self, parent):
        frame = ctk.CTkFrame(parent, fg_color=get_color_modern('surface_card'),
                            border_width=1, border_color=get_color_modern('border'), corner_radius=10)
        frame.pack(fill='x', pady=(0, 15), padx=5)
        inner = ctk.CTkFrame(frame, fg_color='transparent')
        inner.pack(fill='x', padx=20, pady=15)
        
        label = ctk.CTkLabel(inner, text='🏢  Consultar por Unidad de Negocio:',
                            font=('Montserrat', 13, 'bold'),
                            text_color=get_color_modern('text_primary'))
        label.pack(side='left', padx=(0, 15))
        
        unidades = self.cargar_unidades()
        self.unit_menu = ctk.CTkOptionMenu(inner, values=unidades, width=250, height=38,
                                           font=('Arial', 11),
                                           fg_color=get_color_modern('surface'),
                                           button_color=get_color_modern('Sky Blue'),
                                           button_hover_color=get_color_modern('Sea Blue'),
                                           text_color=get_color_modern('text_primary'))
        self.unit_menu.pack(side='left', padx=(0, 10))
        
        btn_consultar = ctk.CTkButton(inner, text='Consultar', width=120, height=38,
                                      font=('Arial', 11, 'bold'),
                                      fg_color='#00d4aa', hover_color='#00b894',
                                      text_color='white', corner_radius=8,
                                      command=self.consultar_por_unidad)
        btn_consultar.pack(side='left')

    def _create_advanced_filters_toggle(self, parent):
        frame = ctk.CTkFrame(parent, fg_color=get_color_modern('surface_card'),
                            border_width=1, border_color=get_color_modern('border'), corner_radius=10)
        frame.pack(fill='x', pady=(0, 15), padx=5)
        inner = ctk.CTkFrame(frame, fg_color='transparent')
        inner.pack(fill='x', padx=20, pady=15)
        
        checkbox = ctk.CTkCheckBox(inner, text='☑️  Mostrar Filtros Avanzados',
                                   variable=self.show_filters_var,
                                   font=('Montserrat', 13, 'bold'),
                                   command=self.toggle_advanced_filters,
                                   fg_color=get_color_modern('Sky Blue'),
                                   hover_color=get_color_modern('Sea Blue'),
                                   text_color=get_color_modern('text_primary'),
                                   border_width=2, border_color=get_color_modern('border'))
        checkbox.pack(side='left')
        self.filters_parent = parent

    def toggle_advanced_filters(self):
        if self.show_filters_var.get():
            if not self.advanced_filters_frame:
                self._create_advanced_filters_content()
            self.advanced_filters_frame.pack(fill='x', pady=(0, 15), padx=5,
                                            before=self.filters_parent.winfo_children()[-3])
        else:
            if self.advanced_filters_frame:
                self.advanced_filters_frame.pack_forget()

    def _create_advanced_filters_content(self):
        self.advanced_filters_frame = ctk.CTkFrame(self.filters_parent,
                                                    fg_color=get_color_modern('surface_light'),
                                                    border_width=2,
                                                    border_color=get_color_modern('Sky Blue'),
                                                    corner_radius=10)
        title = ctk.CTkLabel(self.advanced_filters_frame, text='🔧  Filtros Avanzados',
                            font=('Montserrat', 13, 'bold'),
                            text_color=get_color_modern('text_primary'))
        title.pack(pady=(15, 10), padx=20, anchor='w')
        
        filters_container = ctk.CTkFrame(self.advanced_filters_frame, fg_color='transparent')
        filters_container.pack(fill='x', padx=20, pady=(0, 15))
        
        ctk.CTkLabel(filters_container, text='División:', font=('Arial', 11, 'bold'),
                    text_color=get_color_modern('text_primary')).grid(row=0, column=0, padx=(0, 10), sticky='w')
        self.division_filter = ctk.CTkOptionMenu(filters_container,
                                                 values=['Todas', 'OPERACIONES', 'RRHH', 'TI', 'COMERCIAL', 'FINANZAS'],
                                                 width=150, height=35, font=('Arial', 10),
                                                 fg_color=get_color_modern('surface'),
                                                 button_color=get_color_modern('Sky Blue'),
                                                 button_hover_color=get_color_modern('Sea Blue'))
        self.division_filter.grid(row=0, column=1, padx=(0, 20))
        self.division_filter.set('Todas')
        
        ctk.CTkLabel(filters_container, text='Estatus:', font=('Arial', 11, 'bold'),
                    text_color=get_color_modern('text_primary')).grid(row=0, column=2, padx=(0, 10), sticky='w')
        self.status_filter = ctk.CTkOptionMenu(filters_container,
                                               values=['Todos', 'Activo', 'Inactivo'],
                                               width=150, height=35, font=('Arial', 10),
                                               fg_color=get_color_modern('surface'),
                                               button_color=get_color_modern('Sky Blue'),
                                               button_hover_color=get_color_modern('Sea Blue'))
        self.status_filter.grid(row=0, column=3, padx=(0, 20))
        self.status_filter.set('Todos')
        
        btn_apply = ctk.CTkButton(filters_container, text='✓  Aplicar Filtros',
                                  width=140, height=35, font=('Arial', 11, 'bold'),
                                  fg_color=get_color_modern('accent_green'),
                                  hover_color='#1E8449', text_color='white',
                                  corner_radius=8, command=self.aplicar_filtros_avanzados)
        btn_apply.grid(row=0, column=4, padx=(20, 0))

    def _create_quick_queries(self, parent):
        frame = ctk.CTkFrame(parent, fg_color=get_color_modern('surface_card'),
                            border_width=1, border_color=get_color_modern('border'), corner_radius=10)
        frame.pack(fill='x', pady=(0, 15), padx=5)
        inner = ctk.CTkFrame(frame, fg_color='transparent')
        inner.pack(fill='x', padx=20, pady=15)
        
        ctk.CTkLabel(inner, text='⚡  Consultas Rápidas:',
                    font=('Montserrat', 13, 'bold'),
                    text_color=get_color_modern('text_primary')).pack(side='left', padx=(0, 20))
        
        ctk.CTkButton(inner, text='📋  Todos los Usuarios', width=180, height=40,
                     font=('Arial', 11, 'bold'), fg_color='#ff9f43', hover_color='#ee8630',
                     text_color='white', corner_radius=8, command=self.consultar_todos).pack(side='left', padx=(0, 10))
        
        ctk.CTkButton(inner, text='💾  Ver Datos de Ejemplo', width=200, height=40,
                     font=('Arial', 11, 'bold'), fg_color='#10d876', hover_color='#0ec46d',
                     text_color='white', corner_radius=8, command=self.mostrar_datos_ejemplo).pack(side='left')

    def _create_results_table(self, parent):
        results_frame = ctk.CTkFrame(parent, fg_color=get_color_modern('surface_card'),
                                     border_width=1, border_color=get_color_modern('border'), corner_radius=10)
        results_frame.pack(fill='both', expand=True, pady=(0, 20), padx=5)
        
        header = ctk.CTkFrame(results_frame, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(15, 10))
        ctk.CTkLabel(header, text='📊  Resultados', font=('Montserrat', 14, 'bold'),
                    text_color=get_color_modern('text_primary')).pack(side='left')
        self.results_count_label = ctk.CTkLabel(header, text='0 registros', font=('Arial', 10),
                                                text_color=get_color_modern('text_secondary'))
        self.results_count_label.pack(side='right')
        
        self.table_container = ctk.CTkFrame(results_frame, fg_color='transparent')
        self.table_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        self._init_tksheet()

    def _init_tksheet(self):
        try:
            from tksheet import Sheet
            self.sheet = Sheet(self.table_container,
                             headers=['User ID', 'Nombre', 'Email', 'Unidad', 'División',
                                     'Total Módulos', 'Completados', 'En Progreso', 'Registrados'],
                             header_bg=get_color_modern('Sky Blue'), header_fg='white',
                             header_font=('Montserrat', 11, 'bold'),
                             table_bg=get_color_modern('surface'), table_fg=get_color_modern('text_primary'),
                             table_font=('Arial', 10),
                             index_bg=get_color_modern('surface_dark'), index_fg=get_color_modern('text_secondary'),
                             outline_color=get_color_modern('border'),
                             table_selected_cells_bg=get_color_modern('Sky Blue'),
                             table_selected_cells_fg='white', height=400, width=1200)
            self.sheet.enable_bindings(("single_select", "row_select", "column_width_resize",
                                       "arrowkeys", "right_click_popup_menu", "rc_select", "copy"))
            self.sheet.pack(fill='both', expand=True)
            for col, width in enumerate([80, 200, 220, 120, 120, 110, 110, 110, 110]):
                self.sheet.column_width(column=col, width=width)
        except ImportError:
            ctk.CTkLabel(self.table_container,
                        text='⚠️  La librería tksheet no está instalada.\n\nInstala con: pip install tksheet',
                        font=('Arial', 12), text_color=get_color_modern('accent_red')).pack(pady=50)

    def cargar_unidades(self):
        if not self.cursor:
            return ['CCI', 'SANCHEZ', 'DENNIS', 'HPMX']
        try:
            self.cursor.execute("SELECT DISTINCT NombreUnidad FROM Instituto_UnidadDeNegocio ORDER BY NombreUnidad")
            unidades = [row[0] for row in self.cursor.fetchall()]
            return unidades if unidades else ['CCI', 'SANCHEZ', 'DENNIS', 'HPMX']
        except:
            return ['CCI', 'SANCHEZ', 'DENNIS', 'HPMX']

    def buscar_por_id(self):
        user_id = self.id_entry.get().strip()
        if not user_id:
            messagebox.showwarning('Atención', 'Ingrese un ID de usuario')
            return
        if not self.cursor:
            messagebox.showerror('Error', 'No hay conexión a la base de datos')
            return
        try:
            self.cursor.execute("""
                SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad, u.Division,
                       COUNT(DISTINCT p.IdModulo) as TotalModulos,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as Completados,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'En progreso' THEN 1 ELSE 0 END) as EnProgreso,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'Registrado' THEN 1 ELSE 0 END) as Registrados
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidad
                LEFT JOIN Instituto_ProgresoModulo p ON u.UserId = p.UserId
                WHERE u.UserId = ?
                GROUP BY u.UserId, u.Nombre, u.Email, un.NombreUnidad, u.Division
            """, (user_id,))
            results = self.cursor.fetchall()
            if results:
                self.mostrar_resultados(results)
            else:
                messagebox.showinfo('No encontrado', f'No se encontró el usuario: {user_id}')
        except Exception as e:
            messagebox.showerror('Error', f'Error al buscar: {str(e)}')

    def consultar_por_unidad(self):
        unidad = self.unit_menu.get()
        if not self.cursor:
            messagebox.showerror('Error', 'No hay conexión a la base de datos')
            return
        try:
            self.cursor.execute("""
                SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad, u.Division,
                       COUNT(DISTINCT p.IdModulo) as TotalModulos,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as Completados,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'En progreso' THEN 1 ELSE 0 END) as EnProgreso,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'Registrado' THEN 1 ELSE 0 END) as Registrados
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidad
                LEFT JOIN Instituto_ProgresoModulo p ON u.UserId = p.UserId
                WHERE un.NombreUnidad = ?
                GROUP BY u.UserId, u.Nombre, u.Email, un.NombreUnidad, u.Division
                ORDER BY u.Nombre
            """, (unidad,))
            results = self.cursor.fetchall()
            self.mostrar_resultados(results)
        except Exception as e:
            messagebox.showerror('Error', f'Error al consultar: {str(e)}')

    def consultar_todos(self):
        if not self.cursor:
            messagebox.showerror('Error', 'No hay conexión a la base de datos')
            self.mostrar_datos_ejemplo()
            return
        try:
            self.cursor.execute("""
                SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad, u.Division,
                       COUNT(DISTINCT p.IdModulo) as TotalModulos,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as Completados,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'En progreso' THEN 1 ELSE 0 END) as EnProgreso,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'Registrado' THEN 1 ELSE 0 END) as Registrados
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidad
                LEFT JOIN Instituto_ProgresoModulo p ON u.UserId = p.UserId
                GROUP BY u.UserId, u.Nombre, u.Email, un.NombreUnidad, u.Division
                ORDER BY u.Nombre
                LIMIT 100
            """)
            results = self.cursor.fetchall()
            self.mostrar_resultados(results)
        except Exception as e:
            messagebox.showerror('Error', f'Error al consultar: {str(e)}')

    def mostrar_datos_ejemplo(self):
        datos_ejemplo = [
            ('T123', 'Juan Pérez', 'juan.perez@hp.com', 'HPMX', 'OPERACIONES', 8, 5, 2, 1),
            ('T456', 'María González', 'maria.gonzalez@hp.com', 'SANCHEZ', 'RRHH', 8, 7, 1, 0),
            ('T789', 'Carlos Ramírez', 'carlos.ramirez@hp.com', 'DENNIS', 'TI', 8, 3, 4, 1),
            ('T234', 'Ana Martínez', 'ana.martinez@hp.com', 'CCI', 'COMERCIAL', 8, 8, 0, 0),
            ('T567', 'Luis Fernández', 'luis.fernandez@hp.com', 'HPMX', 'FINANZAS', 8, 2, 5, 1),
        ]
        self.mostrar_resultados(datos_ejemplo)

    def aplicar_filtros_avanzados(self):
        division = self.division_filter.get()
        if not self.cursor:
            messagebox.showinfo('Info', 'Requiere conexión a base de datos')
            return
        where_clauses = []
        params = []
        if division != 'Todas':
            where_clauses.append("u.Division = ?")
            params.append(division)
        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
        try:
            self.cursor.execute(f"""
                SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad, u.Division,
                       COUNT(DISTINCT p.IdModulo) as TotalModulos,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as Completados,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'En progreso' THEN 1 ELSE 0 END) as EnProgreso,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'Registrado' THEN 1 ELSE 0 END) as Registrados
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidad
                LEFT JOIN Instituto_ProgresoModulo p ON u.UserId = p.UserId
                WHERE {where_sql}
                GROUP BY u.UserId, u.Nombre, u.Email, un.NombreUnidad, u.Division
                ORDER BY u.Nombre
            """, tuple(params))
            results = self.cursor.fetchall()
            self.mostrar_resultados(results)
        except Exception as e:
            messagebox.showerror('Error', f'Error al aplicar filtros: {str(e)}')

    def mostrar_resultados(self, data):
        if not self.sheet:
            return
        self.sheet.set_sheet_data([[]])
        if not data:
            self.results_count_label.configure(text='0 registros')
            messagebox.showinfo('Sin resultados', 'No se encontraron datos')
            return
        processed_data = []
        for row in data:
            processed_row = list(row)
            for i in range(5, 9):
                if processed_row[i] is None:
                    processed_row[i] = 0
            processed_data.append(processed_row)
        self.sheet.set_sheet_data(processed_data)
        self.results_count_label.configure(text=f'{len(data)} registros')
        for i in range(len(processed_data)):
            if i % 2 == 0:
                self.sheet.highlight_rows(i, bg=get_color_modern('surface_dark'),
                                         fg=get_color_modern('text_primary'))
