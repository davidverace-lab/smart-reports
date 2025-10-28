"""
SMART REPORTS - HUTCHISON PORTS
Ventana principal simplificada - Usa paneles modulares
Versión 2.0 - Arquitectura Limpia
"""
import customtkinter as ctk
from tkinter import messagebox

from smart_reports.config.identity import get_hutchison_theme, get_font
from smart_reports.database.connection import DatabaseConnection
from smart_reports.services.data_processor import TranscriptProcessor

# Componentes
from smart_reports.ui.components.sidebar import HutchisonSidebar
from smart_reports.ui.components.widgets import AngledHeaderFrame

# Paneles modulares
from smart_reports.ui.panels.dashboard import DashboardPanel
from smart_reports.ui.panels.dashboard_ejemplos import DashboardEjemplosPanel
from smart_reports.ui.panels.tng_summary import TNGSummaryPanel
from smart_reports.ui.panels.consultas import ConsultasPanel


class MainWindow:
    """Ventana principal - Coordinador de paneles"""

    def __init__(self, root, username="Usuario"):
        self.root = root
        self.username = username
        self.theme = get_hutchison_theme()
        self.root.configure(fg_color=self.theme['background'])

        # Estado
        self.current_panel = None
        self.current_file = None

        # Base de datos
        self.db = DatabaseConnection()
        self.conn = None
        self.cursor = None
        self.processor = None

        try:
            self.conn = self.db.connect()
            self.cursor = self.db.get_cursor()
            self.processor = TranscriptProcessor(self.conn)
            print("✓ Conectado a la base de datos")
        except Exception as e:
            print(f"⚠️ No hay conexión a BD: {e}")
            print("   La aplicación funcionará en modo offline")

        # Crear interfaz
        self._create_interface()

    def _create_interface(self):
        """Crear interfaz principal con layout responsive (grid)"""
        # Container principal
        self.main_container = ctk.CTkFrame(
            self.root,
            fg_color=self.theme['background'],
            corner_radius=0
        )
        self.main_container.pack(fill='both', expand=True)

        # Configurar grid
        self.main_container.grid_rowconfigure(0, weight=0)    # Logo bar
        self.main_container.grid_rowconfigure(1, weight=0)    # Welcome header
        self.main_container.grid_rowconfigure(2, weight=1)    # Contenido
        self.main_container.grid_columnconfigure(0, weight=1)

        # FILA 0: Barra superior con logo
        self._create_top_bar()

        # FILA 1: Header de Bienvenida
        self._create_welcome_header()

        # FILA 2: Container para sidebar + contenido
        content_container = ctk.CTkFrame(
            self.main_container,
            fg_color='transparent'
        )
        content_container.grid(row=2, column=0, sticky='nsew')

        # Configurar grid interno para responsive
        content_container.grid_rowconfigure(0, weight=1)
        content_container.grid_columnconfigure(0, weight=0)    # Sidebar
        content_container.grid_columnconfigure(1, weight=1)    # Contenido

        # Sidebar corporativo
        navigation_callbacks = {
            'dashboard': self.show_dashboard,
            'consultas': self.show_consultas,
            'actualizar': self.show_actualizar,
            'configuracion': self.show_configuracion,
        }

        self.sidebar = HutchisonSidebar(content_container, navigation_callbacks)
        self.sidebar.grid(row=0, column=0, sticky='nsw')

        # Área de contenido
        self.content_area = ctk.CTkFrame(
            content_container,
            fg_color=self.theme['background'],
            corner_radius=0
        )
        self.content_area.grid(row=0, column=1, sticky='nsew')

        # Configurar grid del content_area
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        # Mostrar dashboard inicial
        self.show_dashboard()
        self.sidebar.set_active('dashboard')

    def _create_top_bar(self):
        """Crear barra superior con logo"""
        from smart_reports.ui.components.widgets import LogoFrame

        top_bar = ctk.CTkFrame(
            self.main_container,
            fg_color=self.theme['surface'],
            height=80,
            corner_radius=0
        )
        top_bar.grid(row=0, column=0, sticky='ew')
        top_bar.grid_propagate(False)

        logo = LogoFrame(top_bar)
        logo.pack(side='left', padx=20, pady=10)

    def _create_welcome_header(self):
        """Crear header de bienvenida"""
        from datetime import datetime

        header_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.theme['primary'],
            height=60,
            corner_radius=0
        )
        header_frame.grid(row=1, column=0, sticky='ew')
        header_frame.grid_propagate(False)

        welcome_text = ctk.CTkLabel(
            header_frame,
            text=f'Bienvenido, {self.username}',
            font=get_font('heading', 20, 'bold'),
            text_color=self.theme['text_on_primary'],
            anchor='w'
        )
        welcome_text.pack(side='left', padx=30, pady=15)

        date_text = datetime.now().strftime('%d de %B, %Y')
        date_label = ctk.CTkLabel(
            header_frame,
            text=date_text,
            font=get_font('body', 12),
            text_color=self.theme['text_on_primary'],
            anchor='e'
        )
        date_label.pack(side='right', padx=30, pady=15)

    def clear_content_area(self):
        """Limpiar área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # ==================== PANELES ====================

    def show_dashboard(self):
        """Mostrar Dashboard con pestañas"""
        self.clear_content_area()
        self.current_panel = 'dashboard'

        # Flags para carga perezosa
        if not hasattr(self, '_dashboard_tabs_loaded'):
            self._dashboard_tabs_loaded = {
                'General': False,
                'Dashboards de Ejemplo': False,
                'Resumen TNG': False
            }

        # Container principal
        main_frame = ctk.CTkFrame(self.content_area, fg_color='transparent')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header
        header = AngledHeaderFrame(
            main_frame,
            text='Dashboard',
            height=80,
            color=self.theme['primary']
        )
        header.pack(fill='x', pady=(0, 20))

        # TabView
        self.tab_view = ctk.CTkTabview(
            main_frame,
            fg_color=self.theme['surface'],
            segmented_button_fg_color=self.theme['primary'],
            segmented_button_selected_color=self.theme['secondary'],
            segmented_button_unselected_color=self.theme['primary'],
            text_color=self.theme['text_on_primary']
        )
        self.tab_view.pack(fill='both', expand=True)

        # Crear pestañas
        self.tab_view.add('General')
        self.tab_view.add('Dashboards de Ejemplo')
        self.tab_view.add('Resumen TNG')

        # Configurar grid
        for tab_name in ['General', 'Dashboards de Ejemplo', 'Resumen TNG']:
            self.tab_view.tab(tab_name).grid_rowconfigure(0, weight=1)
            self.tab_view.tab(tab_name).grid_columnconfigure(0, weight=1)

        # Comando para carga perezosa
        self.tab_view.configure(command=self._on_dashboard_tab_change)

        # Cargar pestaña General
        self._load_general_tab()

    def _on_dashboard_tab_change(self):
        """Manejar cambio de pestaña con carga perezosa"""
        current_tab = self.tab_view.get()

        if current_tab == 'General' and not self._dashboard_tabs_loaded['General']:
            self._load_general_tab()
        elif current_tab == 'Dashboards de Ejemplo' and not self._dashboard_tabs_loaded['Dashboards de Ejemplo']:
            self._load_ejemplos_tab()
        elif current_tab == 'Resumen TNG' and not self._dashboard_tabs_loaded['Resumen TNG']:
            self._load_tng_tab()

    def _load_general_tab(self):
        """Cargar pestaña General usando DashboardPanel"""
        if self._dashboard_tabs_loaded['General']:
            return

        tab = self.tab_view.tab('General')
        panel = DashboardPanel(tab, self.theme, self.conn, self.cursor)
        panel.show()

        self._dashboard_tabs_loaded['General'] = True

    def _load_ejemplos_tab(self):
        """Cargar pestaña Ejemplos usando DashboardEjemplosPanel"""
        if self._dashboard_tabs_loaded['Dashboards de Ejemplo']:
            return

        tab = self.tab_view.tab('Dashboards de Ejemplo')
        panel = DashboardEjemplosPanel(tab, self.theme)
        panel.show()

        self._dashboard_tabs_loaded['Dashboards de Ejemplo'] = True

    def _load_tng_tab(self):
        """Cargar pestaña TNG usando TNGSummaryPanel"""
        if self._dashboard_tabs_loaded['Resumen TNG']:
            return

        tab = self.tab_view.tab('Resumen TNG')
        panel = TNGSummaryPanel(tab, self.theme, self.root)
        panel.show()

        self._dashboard_tabs_loaded['Resumen TNG'] = True

    def show_consultas(self):
        """Mostrar panel de Consultas"""
        self.clear_content_area()
        self.current_panel = 'consultas'

        scroll_frame = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Usar ConsultasPanel
        panel = ConsultasPanel(scroll_frame, self.theme, self.conn, self.cursor)
        panel.show()

    def show_actualizar(self):
        """Mostrar panel de Actualizar (simplificado por ahora)"""
        self.clear_content_area()
        self.current_panel = 'actualizar'

        from smart_reports.ui.components.widgets import HutchisonLabel

        label = HutchisonLabel(
            self.content_area,
            text='Panel Actualizar Datos\n\n(Funcionalidad de carga de archivos)',
            label_type='heading'
        )
        label.pack(expand=True)

    def show_configuracion(self):
        """Mostrar panel de Configuración (simplificado por ahora)"""
        self.clear_content_area()
        self.current_panel = 'configuracion'

        from smart_reports.ui.components.widgets import HutchisonLabel

        label = HutchisonLabel(
            self.content_area,
            text='Panel Configuración\n\n(Tarjetas de configuración)',
            label_type='heading'
        )
        label.pack(expand=True)
