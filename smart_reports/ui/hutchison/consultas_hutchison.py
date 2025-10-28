"""
Panel Consultas Hutchison
Panel de consultas con tksheet y filtros avanzados
"""

import customtkinter as ctk
from tkinter import messagebox
from smart_reports.config.settings_hutchison import (
    get_color,
    get_font,
    get_button_config
)


class ConsultasHutchison(ctk.CTkFrame):
    """
    Panel de consultas con:
    - Búsqueda por User ID
    - Consulta por Unidad de Negocio
    - Consultas rápidas
    - Filtros avanzados
    - Tabla tksheet interactiva
    """

    def __init__(self, parent, db=None):
        """
        Args:
            parent: Widget padre
            db: Conexión a base de datos
        """
        super().__init__(parent, fg_color=get_color('White'))

        self.db = db
        self.cursor = db.get_cursor() if db else None
        self.sheet = None
        self.filtros_frame = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_interface()

    def _create_interface(self):
        """Crear interfaz del panel"""

        # Scroll frame principal
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent',
            corner_radius=0
        )
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # === TÍTULO ===
        title_label = ctk.CTkLabel(
            scroll_frame,
            text='🔍 Consultas de Usuarios',
            font=get_font('title', 28, 'bold'),
            text_color=get_color('Sea Blue'),
            anchor='w'
        )
        title_label.pack(fill='x', pady=(0, 30))

        # === BÚSQUEDA POR USER ID ===
        self._create_search_by_id(scroll_frame)

        # === CONSULTA POR UNIDAD ===
        self._create_search_by_unit(scroll_frame)

        # === CONSULTAS RÁPIDAS ===
        self._create_quick_queries(scroll_frame)

        # === TABLA DE RESULTADOS ===
        self._create_results_table(scroll_frame)

    def _create_search_by_id(self, parent):
        """Crear sección de búsqueda por User ID"""
        search_frame = ctk.CTkFrame(
            parent,
            fg_color=get_color('Surface'),
            border_width=1,
            border_color=get_color('Border'),
            corner_radius=10
        )
        search_frame.pack(fill='x', pady=10)

        # Container interno
        container = ctk.CTkFrame(search_frame, fg_color='transparent')
        container.pack(fill='x', padx=20, pady=20)

        # Label
        label = ctk.CTkLabel(
            container,
            text='🔍  Buscar Usuario por ID:',
            font=get_font('heading', 14, 'bold'),
            text_color=get_color('Sea Blue')
        )
        label.pack(side='left', padx=(0, 15))

        # Entry
        self.search_entry = ctk.CTkEntry(
            container,
            placeholder_text='Ingrese User ID...',
            font=get_font('body', 12),
            width=300,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=get_color('Border')
        )
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_by_id())

        # Botón
        btn_config = get_button_config('primary')
        btn_search = ctk.CTkButton(
            container,
            text='Buscar',
            **btn_config,
            width=120,
            height=40,
            command=self.search_by_id
        )
        btn_search.pack(side='left', padx=10)

    def _create_search_by_unit(self, parent):
        """Crear sección de búsqueda por unidad"""
        unit_frame = ctk.CTkFrame(
            parent,
            fg_color=get_color('Surface'),
            border_width=1,
            border_color=get_color('Border'),
            corner_radius=10
        )
        unit_frame.pack(fill='x', pady=10)

        container = ctk.CTkFrame(unit_frame, fg_color='transparent')
        container.pack(fill='x', padx=20, pady=20)

        # Label
        label = ctk.CTkLabel(
            container,
            text='🏢  Consultar por Unidad:',
            font=get_font('heading', 14, 'bold'),
            text_color=get_color('Sea Blue')
        )
        label.pack(side='left', padx=(0, 15))

        # Dropdown
        self.unit_dropdown = ctk.CTkOptionMenu(
            container,
            values=['Todas', 'Operaciones TNG', 'Logística TNG', 'Mantenimiento TNG', 'Seguridad TNG'],
            font=get_font('body', 12),
            width=300,
            height=40,
            corner_radius=8,
            fg_color=get_color('White'),
            button_color=get_color('Sky Blue'),
            button_hover_color=get_color('Sea Blue')
        )
        self.unit_dropdown.pack(side='left', padx=5)
        self.unit_dropdown.set('Todas')

        # Botón
        btn_config = get_button_config('primary')
        btn_unit = ctk.CTkButton(
            container,
            text='Consultar',
            **btn_config,
            width=120,
            height=40,
            command=self.search_by_unit
        )
        btn_unit.pack(side='left', padx=10)

    def _create_quick_queries(self, parent):
        """Crear sección de consultas rápidas"""
        quick_frame = ctk.CTkFrame(
            parent,
            fg_color=get_color('Surface'),
            border_width=1,
            border_color=get_color('Border'),
            corner_radius=10
        )
        quick_frame.pack(fill='x', pady=10)

        container = ctk.CTkFrame(quick_frame, fg_color='transparent')
        container.pack(fill='x', padx=20, pady=20)

        # Label
        label = ctk.CTkLabel(
            container,
            text='⚡  Consultas Rápidas:',
            font=get_font('heading', 14, 'bold'),
            text_color=get_color('Sea Blue')
        )
        label.pack(side='left', padx=(0, 15))

        # Botones rápidos
        quick_buttons = [
            ('Todos los Usuarios', self.query_all_users, 'primary'),
            ('Usuarios Activos', self.query_active_users, 'success'),
            ('Mostrar Filtros', self.toggle_filters, 'secondary'),
        ]

        for text, command, btn_type in quick_buttons:
            btn_config = get_button_config(btn_type)
            btn = ctk.CTkButton(
                container,
                text=text,
                **btn_config,
                width=150,
                height=35,
                command=command
            )
            btn.pack(side='left', padx=5)

    def _create_results_table(self, parent):
        """Crear tabla de resultados con tksheet"""

        # Frame para tabla
        table_frame = ctk.CTkFrame(
            parent,
            fg_color=get_color('Surface'),
            border_width=1,
            border_color=get_color('Border'),
            corner_radius=10
        )
        table_frame.pack(fill='both', expand=True, pady=20)

        # Título
        title_label = ctk.CTkLabel(
            table_frame,
            text='📊 Resultados',
            font=get_font('heading', 16, 'bold'),
            text_color=get_color('Sea Blue')
        )
        title_label.pack(pady=(15, 10), padx=20, anchor='w')

        # Container para tksheet
        self.table_container = ctk.CTkFrame(
            table_frame,
            fg_color=get_color('White'),
            corner_radius=5
        )
        self.table_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Mensaje inicial
        self.placeholder_label = ctk.CTkLabel(
            self.table_container,
            text='Seleccione una consulta para ver los resultados',
            font=get_font('body', 14),
            text_color=get_color('Medium Gray')
        )
        self.placeholder_label.pack(expand=True, pady=50)

    def _create_sheet(self):
        """Crear tabla tksheet"""
        try:
            from tksheet import Sheet

            # Limpiar placeholder
            if self.placeholder_label:
                self.placeholder_label.destroy()
                self.placeholder_label = None

            # Destruir sheet anterior si existe
            if self.sheet:
                self.sheet.destroy()

            # Crear nueva sheet
            self.sheet = Sheet(
                self.table_container,
                headers=['User ID', 'Nombre', 'Email', 'Unidad', 'Total Módulos', 'Completados'],
                header_bg=get_color('Sky Blue'),
                header_fg='white',
                header_font=('Montserrat', 11, 'bold'),
                table_bg='white',
                table_fg=get_color('Dark Gray'),
                table_font=('Arial', 10),
                index_bg=get_color('Light Gray'),
                index_fg=get_color('Sea Blue'),
                frame_bg=get_color('Border'),
                popup_menu_bg='white',
                popup_menu_fg=get_color('Dark Gray'),
                outline_color=get_color('Border'),
                table_selected_cells_bg=get_color('Sky Blue'),
                table_selected_cells_fg='white'
            )

            # Habilitar funcionalidades
            self.sheet.enable_bindings(
                'single_select',
                'row_select',
                'column_width_resize',
                'arrowkeys',
                'right_click_popup_menu',
                'rc_select',
                'copy',
                'select_all'
            )

            self.sheet.pack(fill='both', expand=True)

            return True

        except ImportError:
            messagebox.showerror(
                "Error",
                "La librería tksheet no está instalada.\n\n"
                "Instala con: pip install tksheet"
            )
            return False

    def search_by_id(self):
        """Buscar usuario por ID"""
        user_id = self.search_entry.get().strip()

        if not user_id:
            messagebox.showwarning("Advertencia", "Ingrese un User ID")
            return

        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            self.cursor.execute("""
                SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad,
                       COUNT(DISTINCT p.IdModulo) as TotalModulos,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as Completados
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                LEFT JOIN Instituto_ProgresoModulo p ON u.UserId = p.UserId
                WHERE u.UserId = ?
                GROUP BY u.UserId, u.Nombre, u.Email, un.NombreUnidad
            """, (user_id,))

            result = self.cursor.fetchall()

            if result:
                self._update_table(result)
            else:
                messagebox.showinfo("No encontrado", f"No se encontró el usuario: {user_id}")

        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda:\n{str(e)}")

    def search_by_unit(self):
        """Buscar usuarios por unidad"""
        unit = self.unit_dropdown.get()

        if not self.cursor:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            if unit == 'Todas':
                self.query_all_users()
            else:
                self.cursor.execute("""
                    SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad,
                           COUNT(DISTINCT p.IdModulo) as TotalModulos,
                           SUM(CASE WHEN p.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as Completados
                    FROM Instituto_Usuario u
                    LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                    LEFT JOIN Instituto_ProgresoModulo p ON u.UserId = p.UserId
                    WHERE un.NombreUnidad = ?
                    GROUP BY u.UserId, u.Nombre, u.Email, un.NombreUnidad
                    ORDER BY u.Nombre
                """, (unit,))

                result = self.cursor.fetchall()
                self._update_table(result)

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def query_all_users(self):
        """Consultar todos los usuarios"""
        if not self.cursor:
            # Datos de demostración
            demo_data = [
                ('U001', 'Juan Pérez', 'juan.perez@hutchison.com', 'Operaciones TNG', 14, 12),
                ('U002', 'María García', 'maria.garcia@hutchison.com', 'Logística TNG', 14, 10),
                ('U003', 'Carlos López', 'carlos.lopez@hutchison.com', 'Mantenimiento TNG', 14, 14),
            ]
            self._update_table(demo_data)
            return

        try:
            self.cursor.execute("""
                SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad,
                       COUNT(DISTINCT p.IdModulo) as TotalModulos,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as Completados
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                LEFT JOIN Instituto_ProgresoModulo p ON u.UserId = p.UserId
                GROUP BY u.UserId, u.Nombre, u.Email, un.NombreUnidad
                ORDER BY u.Nombre
            """)

            result = self.cursor.fetchall()
            self._update_table(result)

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def query_active_users(self):
        """Consultar solo usuarios activos"""
        if not self.cursor:
            messagebox.showinfo("Info", "Requiere conexión a base de datos")
            return

        try:
            self.cursor.execute("""
                SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad,
                       COUNT(DISTINCT p.IdModulo) as TotalModulos,
                       SUM(CASE WHEN p.EstatusModuloUsuario = 'Completado' THEN 1 ELSE 0 END) as Completados
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                LEFT JOIN Instituto_ProgresoModulo p ON u.UserId = p.UserId
                WHERE u.Activo = 1
                GROUP BY u.UserId, u.Nombre, u.Email, un.NombreUnidad
                ORDER BY u.Nombre
            """)

            result = self.cursor.fetchall()
            self._update_table(result)

        except Exception as e:
            messagebox.showerror("Error", f"Error en consulta:\n{str(e)}")

    def toggle_filters(self):
        """Mostrar/ocultar filtros avanzados"""
        messagebox.showinfo(
            "Filtros Avanzados",
            "Funcionalidad de filtros avanzados en desarrollo.\n\n"
            "Incluirá filtros por:\n"
            "- División\n"
            "- Fecha de registro\n"
            "- Progreso de capacitación"
        )

    def _update_table(self, data):
        """Actualizar tabla con datos"""
        if not self._create_sheet():
            return

        if data:
            self.sheet.set_sheet_data(data)
            self.sheet.set_all_cell_sizes_to_text()
            messagebox.showinfo(
                "Éxito",
                f"Se cargaron {len(data)} registros.\n\n"
                "Funcionalidades disponibles:\n"
                "• Click derecho para menú contextual\n"
                "• Seleccionar filas\n"
                "• Copiar datos (Ctrl+C)\n"
                "• Redimensionar columnas"
            )
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron datos")


# Para testing standalone
if __name__ == '__main__':
    root = ctk.CTk()
    root.title("Test Consultas Hutchison")
    root.geometry("1200x800")

    ctk.set_appearance_mode("light")

    panel = ConsultasHutchison(root)
    panel.pack(fill='both', expand=True)

    root.mainloop()
