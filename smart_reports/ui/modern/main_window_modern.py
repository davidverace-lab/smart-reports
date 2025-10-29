"""
Main Window Modern - Ventana Principal con Diseño Oscuro
Layout: Header + Sidebar Corporativa + Content Area (diseño oscuro)
"""

import customtkinter as ctk
from tkinter import messagebox
from smart_reports.config.settings_modern import (
    PRIMARY_COLORS_MODERN,
    FONTS_MODERN,
    SIDEBAR_CONFIG_MODERN,
    HEADER_CONFIG_MODERN,
    get_color_modern,
    get_font_modern
)
from smart_reports.database.connection import DatabaseConnection
from smart_reports.ui.modern.sidebar_modern import SidebarModern


class MainWindowModern(ctk.CTkFrame):
    """
    Ventana principal con diseño oscuro

    Layout idéntico a Hutchison pero con colores oscuros
    """

    def __init__(self, parent, username="Usuario"):
        """
        Args:
            parent: Widget padre (root)
            username: Nombre del usuario actual
        """
        super().__init__(parent, fg_color=get_color_modern('background'))

        self.parent = parent
        self.username = username
        self.current_panel = None

        # Conexión a base de datos
        try:
            self.db = DatabaseConnection()
            self.conn = self.db.connect()
            self.cursor = self.db.get_cursor()
        except Exception as e:
            print(f"⚠️  No se pudo conectar a la base de datos: {e}")
            self.db = None
            self.conn = None
            self.cursor = None

        self.pack(fill='both', expand=True)

        # Crear interfaz
        self._create_layout()

        # Mostrar dashboard por defecto
        self.show_dashboard()

    def _create_layout(self):
        """Crear layout principal: Header + Sidebar + Content"""

        # Configurar grid principal
        self.grid_rowconfigure(0, weight=0)  # Header fijo
        self.grid_rowconfigure(1, weight=1)  # Contenido expandible
        self.grid_columnconfigure(0, weight=0)  # Sidebar fijo
        self.grid_columnconfigure(1, weight=1)  # Content expandible

        # === HEADER ===
        self._create_header()

        # === SIDEBAR ===
        self._create_sidebar()

        # === CONTENT AREA ===
        self.content_area = ctk.CTkFrame(
            self,
            fg_color=get_color_modern('background'),
            corner_radius=0
        )
        self.content_area.grid(row=1, column=1, sticky='nsew')
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

    def _create_header(self):
        """Crear header con bienvenida y título"""

        header = ctk.CTkFrame(
            self,
            fg_color=get_color_modern('surface'),
            height=HEADER_CONFIG_MODERN['height'],
            corner_radius=0
        )
        header.grid(row=0, column=0, columnspan=2, sticky='ew')
        header.grid_propagate(False)

        # Borde inferior
        border = ctk.CTkFrame(
            header,
            fg_color=get_color_modern('border'),
            height=1
        )
        border.pack(side='bottom', fill='x')

        # Container interno con padding
        header_content = ctk.CTkFrame(header, fg_color='transparent')
        header_content.pack(fill='both', expand=True, padx=20, pady=10)

        # Bienvenida (izquierda)
        welcome_label = ctk.CTkLabel(
            header_content,
            text=f'Bienvenido, {self.username}',
            font=get_font_modern('heading', 16),
            text_color=get_color_modern('text_primary'),
            anchor='w'
        )
        welcome_label.pack(side='left')

        # Título (derecha)
        title_label = ctk.CTkLabel(
            header_content,
            text='SMART REPORTS - INSTITUTO HP',
            font=get_font_modern('heading', 16, 'bold'),
            text_color=get_color_modern('accent_primary'),  # Sky Blue
            anchor='e'
        )
        title_label.pack(side='right')

    def _create_sidebar(self):
        """Crear sidebar corporativa con navegación"""

        # Usar la nueva sidebar corporativa oscura
        self.sidebar = SidebarModern(self, self.switch_panel)
        self.sidebar.grid(row=1, column=0, sticky='ns')  # CRÍTICO: solo 'ns' no 'nsew'

    def switch_panel(self, panel_id):
        """
        Cambiar entre paneles según el ID

        Args:
            panel_id: Identificador del panel ('dashboard', 'consultas', 'actualizar', 'configuracion')
        """
        if panel_id == 'dashboard':
            self.show_dashboard()
        elif panel_id == 'consultas':
            self.show_consultas()
        elif panel_id == 'actualizar':
            self.show_cruce_datos()
        elif panel_id == 'configuracion':
            self.show_configuracion()

    def _clear_content(self):
        """Limpiar área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        """Mostrar panel Dashboard"""
        self._clear_content()

        from smart_reports.ui.modern.dashboard_modern import DashboardModern

        panel = DashboardModern(self.content_area, self.db)
        panel.grid(row=0, column=0, sticky='nsew')
        self.current_panel = panel

    def show_consultas(self):
        """Mostrar panel Consultas"""
        self._clear_content()

        from smart_reports.ui.modern.consultas_modern import ConsultasModern

        panel = ConsultasModern(self.content_area, self.db)
        panel.grid(row=0, column=0, sticky='nsew')
        self.current_panel = panel

    def show_cruce_datos(self):
        """Mostrar panel Cruce de Datos"""
        self._clear_content()

        from smart_reports.ui.modern.cruce_datos_modern import CruceDatosModern

        panel = CruceDatosModern(self.content_area, self.db)
        panel.grid(row=0, column=0, sticky='nsew')
        self.current_panel = panel

    def show_configuracion(self):
        """Mostrar panel Configuración"""
        self._clear_content()

        from smart_reports.ui.modern.configuracion_modern import ConfiguracionModern

        panel = ConfiguracionModern(self.content_area, self.db)
        panel.grid(row=0, column=0, sticky='nsew')
        self.current_panel = panel


# Para testing standalone
if __name__ == '__main__':
    root = ctk.CTk()
    root.title("Test Main Window Modern")
    root.geometry("1400x900")

    ctk.set_appearance_mode("dark")

    main_win = MainWindowModern(root, "Administrador")

    root.mainloop()
