"""
Main Window Hutchison - Ventana Principal con Diseño Corporativo
Layout: Header + Sidebar + Content Area
"""

import customtkinter as ctk
from tkinter import messagebox
from smart_reports.config.settings_hutchison import (
    PRIMARY_COLORS,
    FONTS_HUTCHISON,
    SIDEBAR_CONFIG,
    HEADER_CONFIG,
    get_color,
    get_font
)
from smart_reports.database.connection import DatabaseConnection


class MainWindowHutchison(ctk.CTkFrame):
    """
    Ventana principal con diseño corporativo Hutchison

    Layout:
    ┌────────────────────────────────────────┐
    │         HEADER (Bienvenida)            │
    ├────────┬───────────────────────────────┤
    │ SIDE   │                               │
    │ BAR    │     CONTENT AREA              │
    │        │                               │
    └────────┴───────────────────────────────┘
    """

    def __init__(self, parent, username="Usuario"):
        """
        Args:
            parent: Widget padre (root)
            username: Nombre del usuario actual
        """
        super().__init__(parent, fg_color=get_color('White'))

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
            fg_color=get_color('White'),
            corner_radius=0
        )
        self.content_area.grid(row=1, column=1, sticky='nsew')
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

    def _create_header(self):
        """Crear header con bienvenida y título"""

        header = ctk.CTkFrame(
            self,
            fg_color=get_color('White'),
            height=HEADER_CONFIG['height'],
            corner_radius=0
        )
        header.grid(row=0, column=0, columnspan=2, sticky='ew')
        header.grid_propagate(False)

        # Borde inferior
        border = ctk.CTkFrame(
            header,
            fg_color=get_color('Border'),
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
            font=get_font('heading', 16),
            text_color=get_color('Sea Blue'),
            anchor='w'
        )
        welcome_label.pack(side='left')

        # Título (derecha)
        title_label = ctk.CTkLabel(
            header_content,
            text='SMART REPORTS - INSTITUTO HP',
            font=get_font('heading', 16, 'bold'),
            text_color=get_color('Sea Blue'),
            anchor='e'
        )
        title_label.pack(side='right')

    def _create_sidebar(self):
        """Crear sidebar con navegación"""

        self.sidebar = ctk.CTkFrame(
            self,
            fg_color=get_color('Light Gray'),
            width=SIDEBAR_CONFIG['width'],
            corner_radius=0
        )
        self.sidebar.grid(row=1, column=0, sticky='ns')
        self.sidebar.grid_propagate(False)

        # Borde derecho
        border = ctk.CTkFrame(
            self.sidebar,
            fg_color=get_color('Border'),
            width=1
        )
        border.pack(side='right', fill='y')

        # Botones de navegación
        self.nav_buttons = {}

        nav_items = [
            ('📊', 'Dashboard', self.show_dashboard),
            ('🔍', 'Consultas', self.show_consultas),
            ('🔄', 'Cruce de Datos', self.show_cruce_datos),
            ('⚙️', 'Configuración', self.show_configuracion),
        ]

        for icon, text, command in nav_items:
            self._create_nav_button(icon, text, command)

    def _create_nav_button(self, icon, text, command):
        """Crear botón de navegación"""

        btn = ctk.CTkButton(
            self.sidebar,
            text=f'{icon}  {text}',
            font=SIDEBAR_CONFIG['button_font'],
            fg_color=SIDEBAR_CONFIG['button_fg_color'],
            hover_color=SIDEBAR_CONFIG['button_hover_color'],
            text_color=SIDEBAR_CONFIG['button_text_color'],
            height=SIDEBAR_CONFIG['button_height'],
            anchor='w',
            corner_radius=0,
            command=lambda: self._on_nav_click(text, command)
        )
        btn.pack(fill='x', padx=0, pady=1)
        self.nav_buttons[text] = btn

    def _on_nav_click(self, button_name, command):
        """Manejar clic en navegación"""

        # Resetear todos los botones
        for name, btn in self.nav_buttons.items():
            if name == button_name:
                # Botón activo
                btn.configure(
                    fg_color=SIDEBAR_CONFIG['button_active_fg_color'],
                    text_color=SIDEBAR_CONFIG['button_active_text_color']
                )
            else:
                # Botón inactivo
                btn.configure(
                    fg_color=SIDEBAR_CONFIG['button_fg_color'],
                    text_color=SIDEBAR_CONFIG['button_text_color']
                )

        # Ejecutar comando
        command()

    def _clear_content(self):
        """Limpiar área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        """Mostrar panel Dashboard"""
        self._clear_content()

        # Importar aquí para evitar circular imports
        from smart_reports.ui.hutchison.dashboard_hutchison import DashboardHutchison

        panel = DashboardHutchison(self.content_area, self.db)
        panel.grid(row=0, column=0, sticky='nsew')
        self.current_panel = panel

    def show_consultas(self):
        """Mostrar panel Consultas"""
        self._clear_content()

        from smart_reports.ui.hutchison.consultas_hutchison import ConsultasHutchison

        panel = ConsultasHutchison(self.content_area, self.db)
        panel.grid(row=0, column=0, sticky='nsew')
        self.current_panel = panel

    def show_cruce_datos(self):
        """Mostrar panel Cruce de Datos"""
        self._clear_content()

        from smart_reports.ui.hutchison.cruce_datos_hutchison import CruceDatosHutchison

        panel = CruceDatosHutchison(self.content_area, self.db)
        panel.grid(row=0, column=0, sticky='nsew')
        self.current_panel = panel

    def show_configuracion(self):
        """Mostrar panel Configuración"""
        self._clear_content()

        from smart_reports.ui.hutchison.configuracion_hutchison import ConfiguracionHutchison

        panel = ConfiguracionHutchison(self.content_area, self.db)
        panel.grid(row=0, column=0, sticky='nsew')
        self.current_panel = panel


# Para testing standalone
if __name__ == '__main__':
    root = ctk.CTk()
    root.title("Test Main Window Hutchison")
    root.geometry("1400x900")

    ctk.set_appearance_mode("light")

    main_win = MainWindowHutchison(root, "Administrador")

    root.mainloop()
