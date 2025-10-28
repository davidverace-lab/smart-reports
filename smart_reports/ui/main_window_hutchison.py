"""
SMART REPORTS - HUTCHISON PORTS
Ventana principal con diseño corporativo completo
Versión 2.0 - Manual de Identidad Visual
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from datetime import datetime
import os
import pandas as pd

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    DRAG_DROP_AVAILABLE = False
    print("⚠️ tkinterdnd2 no disponible. Drag & drop deshabilitado.")

from smart_reports.config.hutchison_identity import get_hutchison_theme, get_font
from smart_reports.database.connection import DatabaseConnection
from smart_reports.services.data_processor import TranscriptProcessor

# Componentes corporativos Hutchison
from smart_reports.ui.components.hutchison_widgets import (
    AngledHeaderFrame,
    AngledDivider,
    HutchisonButton,
    HutchisonLabel,
    LogoFrame,
    MetricCardAngled,
    AngledCard
)
from smart_reports.ui.components.hutchison_sidebar import HutchisonSidebar
from smart_reports.ui.components.hutchison_config_card import HutchisonConfigCard
from smart_reports.ui.dialogs.user_management_dialog import UserManagementDialog


class MainWindow:
    """Ventana principal - Diseño Corporativo Hutchison Ports"""

    def __init__(self, root, username="Usuario"):
        self.root = root
        self.username = username  # Nombre del usuario logueado

        # Tema corporativo
        self.theme = get_hutchison_theme()
        self.root.configure(fg_color=self.theme['background'])

        # Variables de estado
        self.current_file = None
        self.changes_log = []
        self.current_panel = None

        # Conexión a base de datos (opcional)
        self.db = DatabaseConnection()
        self.conn = None
        self.cursor = None
        self.processor = None  # Se inicializará si hay conexión a BD

        try:
            self.conn = self.db.connect()
            self.cursor = self.db.get_cursor()
            # Inicializar processor solo si hay conexión
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

        # Configurar grid del container principal
        self.main_container.grid_rowconfigure(0, weight=0)    # Logo bar (fijo)
        self.main_container.grid_rowconfigure(1, weight=0)    # Welcome header (fijo)
        self.main_container.grid_rowconfigure(2, weight=1)    # Contenido (expandible)
        self.main_container.grid_columnconfigure(0, weight=1)

        # FILA 0: Barra superior con logo
        self._create_top_bar()

        # FILA 1: Header de Bienvenida
        self._create_welcome_header()

        # FILA 2: Container para sidebar + contenido (grid interno)
        content_container = ctk.CTkFrame(
            self.main_container,
            fg_color='transparent'
        )
        content_container.grid(row=2, column=0, sticky='nsew')

        # Configurar grid interno para responsive
        content_container.grid_rowconfigure(0, weight=1)       # Fila de contenido expandible
        content_container.grid_columnconfigure(0, weight=0)    # Sidebar (ancho fijo)
        content_container.grid_columnconfigure(1, weight=1)    # Contenido (expandible)

        # Sidebar corporativo (Sea Blue) - Columna 0
        navigation_callbacks = {
            'dashboard': self.show_dashboard,
            'consultas': self.show_consultas,
            'actualizar': self.show_actualizar,
            'configuracion': self.show_configuracion,
        }

        self.sidebar = HutchisonSidebar(content_container, navigation_callbacks)
        self.sidebar.grid(row=0, column=0, sticky='nsw')

        # Área de contenido - Columna 1
        self.content_area = ctk.CTkFrame(
            content_container,
            fg_color=self.theme['background'],
            corner_radius=0
        )
        self.content_area.grid(row=0, column=1, sticky='nsew')

        # Mostrar dashboard inicial
        self.show_dashboard()
        self.sidebar.set_active('dashboard')

    def _create_top_bar(self):
        """Crear barra superior con logo corporativo"""
        top_bar = ctk.CTkFrame(
            self.main_container,
            fg_color=self.theme['surface'],
            height=80,
            corner_radius=0
        )
        top_bar.grid(row=0, column=0, sticky='ew')
        top_bar.grid_propagate(False)

        # Logo en esquina superior izquierda (obligatorio)
        logo = LogoFrame(top_bar)
        logo.pack(side='left', padx=20, pady=10)

    def _create_welcome_header(self):
        """Crear header de bienvenida con nombre de usuario"""
        # Frame del header
        header_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.theme['primary'],  # Sky Blue
            height=60,
            corner_radius=0
        )
        header_frame.grid(row=1, column=0, sticky='ew')
        header_frame.grid_propagate(False)

        # Texto de bienvenida
        welcome_text = ctk.CTkLabel(
            header_frame,
            text=f'Bienvenido, {self.username}',
            font=get_font('heading', 20, 'bold'),
            text_color=self.theme['text_on_primary'],
            anchor='w'
        )
        welcome_text.pack(side='left', padx=30, pady=15)

        # Información adicional (fecha actual)
        from datetime import datetime
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

    # ==================== DASHBOARD ====================

    def show_dashboard(self):
        """Panel de Dashboard con diseño Hutchison y pestañas con carga perezosa"""
        self.clear_content_area()
        self.current_panel = 'dashboard'

        # Flags para carga perezosa
        if not hasattr(self, '_dashboard_tabs_loaded'):
            self._dashboard_tabs_loaded = {
                'General': False,
                'Dashboards de Ejemplo': False,
                'Resumen TNG': False
            }
            self._tng_comparison_mode = 'Actual'  # Modo de comparación TNG

        # Container principal
        main_frame = ctk.CTkFrame(self.content_area, fg_color='transparent')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header angulado
        header = AngledHeaderFrame(
            main_frame,
            text='Dashboard',
            height=80,
            color=self.theme['primary']
        )
        header.pack(fill='x', pady=(0, 20))

        # TabView con carga perezosa
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

        # Configurar grid para que el contenido sea expandible
        self.tab_view.tab('General').grid_rowconfigure(0, weight=1)
        self.tab_view.tab('General').grid_columnconfigure(0, weight=1)
        self.tab_view.tab('Dashboards de Ejemplo').grid_rowconfigure(0, weight=1)
        self.tab_view.tab('Dashboards de Ejemplo').grid_columnconfigure(0, weight=1)
        self.tab_view.tab('Resumen TNG').grid_rowconfigure(0, weight=1)
        self.tab_view.tab('Resumen TNG').grid_columnconfigure(0, weight=1)

        # Configurar comando para detectar cambio de pestaña
        self.tab_view.configure(command=self._on_dashboard_tab_change)

        # Cargar pestaña General inmediatamente
        self._load_general_tab()

    def _on_dashboard_tab_change(self):
        """Manejar cambio de pestaña con carga perezosa"""
        current_tab = self.tab_view.get()

        # Cargar contenido solo si no ha sido cargado antes
        if current_tab == 'Dashboards de Ejemplo' and not self._dashboard_tabs_loaded['Dashboards de Ejemplo']:
            self._load_ejemplos_tab()
        elif current_tab == 'General' and not self._dashboard_tabs_loaded['General']:
            self._load_general_tab()
        elif current_tab == 'Resumen TNG' and not self._dashboard_tabs_loaded['Resumen TNG']:
            self._load_tng_summary_tab()

    def _load_general_tab(self):
        """Cargar contenido de la pestaña General"""
        if self._dashboard_tabs_loaded['General']:
            return

        tab = self.tab_view.tab('General')

        # Scroll frame dentro de la pestaña
        scroll_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color='transparent'
        )
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Divisor
        divider = AngledDivider(
            scroll_frame,
            height=4,
            color=self.theme['secondary']
        )
        divider.pack(fill='x', pady=(0, 30))

        # Métricas
        self._create_metrics_grid(scroll_frame)

        # Divisor
        divider2 = AngledDivider(
            scroll_frame,
            height=4,
            color=self.theme['accent_orange']
        )
        divider2.pack(fill='x', pady=30)

        # Información adicional
        info_card = AngledCard(
            scroll_frame,
            title='Información del Sistema',
            header_color=self.theme['primary']
        )
        info_card.pack(fill='x', pady=20)

        info_text = HutchisonLabel(
            info_card.content_frame,
            text=(
                "Sistema de Gestión de Capacitaciones\n\n" +
                "Este dashboard muestra métricas en tiempo real del progreso de capacitación " +
                "de todos los usuarios del Instituto Hutchison Ports.\n\n" +
                f"Estado BD: {'✓ Conectado' if self.conn else '✗ Desconectado'}"
            ),
            label_type='body'
        )
        info_text.configure(wraplength=800, justify='left')
        info_text.pack(pady=10)

        # Marcar como cargado
        self._dashboard_tabs_loaded['General'] = True

    def _load_ejemplos_tab(self):
        """Cargar contenido de la pestaña Dashboards de Ejemplo (con gráficos Plotly)"""
        if self._dashboard_tabs_loaded['Dashboards de Ejemplo']:
            return

        tab = self.tab_view.tab('Dashboards de Ejemplo')

        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color='transparent'
        )
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Título
        title_label = HutchisonLabel(
            scroll_frame,
            text='Gráficos de Ejemplo - Visualización de Datos',
            label_type='heading'
        )
        title_label.configure(font=get_font('heading', 20, 'bold'))
        title_label.pack(pady=(10, 20))

        # Crear 3 gráficos de ejemplo con Plotly
        self._create_example_charts(scroll_frame)

        # Marcar como cargado
        self._dashboard_tabs_loaded['Dashboards de Ejemplo'] = True

    def _create_example_charts(self, parent):
        """Crear gráficos de ejemplo con Plotly"""
        try:
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            import tkinter as tk
            from tkinterweb import HtmlFrame

            # Card 1: Gráfico de barras
            card1 = AngledCard(
                parent,
                title='Ejemplo 1: Progreso por Módulo',
                header_color=self.theme['primary']
            )
            card1.pack(fill='x', pady=15)

            fig1 = go.Figure(data=[
                go.Bar(
                    x=['Módulo A', 'Módulo B', 'Módulo C', 'Módulo D', 'Módulo E'],
                    y=[45, 78, 62, 91, 53],
                    marker_color=self.theme['primary']
                )
            ])
            fig1.update_layout(
                title='Porcentaje de Completado por Módulo',
                yaxis_title='Porcentaje (%)',
                height=350
            )

            html1 = fig1.to_html(include_plotlyjs='cdn')
            frame1 = HtmlFrame(card1.content_frame, messages_enabled=False)
            frame1.load_html(html1)
            frame1.pack(fill='both', expand=True, padx=10, pady=10)

            # Card 2: Gráfico de líneas
            card2 = AngledCard(
                parent,
                title='Ejemplo 2: Tendencia de Usuarios Activos',
                header_color=self.theme['secondary']
            )
            card2.pack(fill='x', pady=15)

            fig2 = go.Figure(data=[
                go.Scatter(
                    x=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                    y=[120, 145, 138, 167, 189, 201],
                    mode='lines+markers',
                    line=dict(color=self.theme['secondary'], width=3)
                )
            ])
            fig2.update_layout(
                title='Usuarios Activos Mensuales',
                yaxis_title='Usuarios',
                height=350
            )

            html2 = fig2.to_html(include_plotlyjs='cdn')
            frame2 = HtmlFrame(card2.content_frame, messages_enabled=False)
            frame2.load_html(html2)
            frame2.pack(fill='both', expand=True, padx=10, pady=10)

            # Card 3: Gráfico de pie
            card3 = AngledCard(
                parent,
                title='Ejemplo 3: Distribución por Categoría',
                header_color=self.theme['accent_yellow']
            )
            card3.pack(fill='x', pady=15)

            fig3 = go.Figure(data=[
                go.Pie(
                    labels=['Seguridad', 'Operaciones', 'Logística', 'Calidad', 'Administración'],
                    values=[30, 25, 20, 15, 10],
                    marker=dict(colors=[
                        self.theme['primary'],
                        self.theme['secondary'],
                        self.theme['accent_yellow'],
                        self.theme['accent_orange'],
                        self.theme['accent_green']
                    ])
                )
            ])
            fig3.update_layout(title='Usuarios por Categoría', height=350)

            html3 = fig3.to_html(include_plotlyjs='cdn')
            frame3 = HtmlFrame(card3.content_frame, messages_enabled=False)
            frame3.load_html(html3)
            frame3.pack(fill='both', expand=True, padx=10, pady=10)

        except ImportError as e:
            # Si Plotly o tkinterweb no están disponibles, mostrar mensaje
            error_label = HutchisonLabel(
                parent,
                text=(
                    'Gráficos de Plotly no disponibles.\n\n'
                    'Instala las dependencias:\n'
                    'pip install plotly tkinterweb'
                ),
                label_type='body'
            )
            error_label.configure(text_color='red')
            error_label.pack(pady=50)
        except Exception as e:
            error_label = HutchisonLabel(
                parent,
                text=f'Error al cargar gráficos: {str(e)}',
                label_type='body'
            )
            error_label.configure(text_color='red')
            error_label.pack(pady=50)

    def _load_tng_summary_tab(self):
        """Cargar contenido de la pestaña Resumen Ejecutivo TNG con comparador de periodos"""
        if self._dashboard_tabs_loaded['Resumen TNG']:
            return

        tab = self.tab_view.tab('Resumen TNG')

        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color='transparent'
        )
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Título
        title_label = HutchisonLabel(
            scroll_frame,
            text='Resumen Ejecutivo TNG',
            label_type='heading'
        )
        title_label.configure(font=get_font('heading', 24, 'bold'))
        title_label.pack(pady=(10, 5))

        subtitle_label = HutchisonLabel(
            scroll_frame,
            text='Terminal de Nuevas Generaciones - Métricas de Capacitación',
            label_type='body'
        )
        subtitle_label.configure(font=get_font('body', 12), text_color=self.theme['text_secondary'])
        subtitle_label.pack(pady=(0, 20))

        # Divisor
        divider = AngledDivider(
            scroll_frame,
            height=4,
            color=self.theme['secondary']
        )
        divider.pack(fill='x', pady=(0, 25))

        # SELECTOR DE COMPARACIÓN
        comparison_card = AngledCard(
            scroll_frame,
            title='Comparador de Periodos',
            header_color=self.theme['primary']
        )
        comparison_card.pack(fill='x', pady=15)

        # Frame del selector
        selector_frame = ctk.CTkFrame(comparison_card.content_frame, fg_color='transparent')
        selector_frame.pack(fill='x', pady=15)

        # Label explicativa
        HutchisonLabel(
            selector_frame,
            text='Comparar métricas actuales con:',
            label_type='body'
        ).configure(font=get_font('body', 14, 'bold'))
        HutchisonLabel(
            selector_frame,
            text='Comparar métricas actuales con:',
            label_type='body'
        ).pack(side='left', padx=(10, 15))

        # Segmented Button para comparación
        self.tng_comparison_selector = ctk.CTkSegmentedButton(
            selector_frame,
            values=['Actual', 'vs Semana Ant.', 'vs Mes Ant.', 'vs Trim. Ant.'],
            font=get_font('body', 13),
            fg_color=self.theme['surface'],
            selected_color=self.theme['primary'],
            selected_hover_color=self.theme['secondary'],
            unselected_color=self.theme['border'],
            command=self._on_tng_comparison_change
        )
        self.tng_comparison_selector.set('Actual')
        self.tng_comparison_selector.pack(side='left', padx=10)

        # MÉTRICAS TNG CON COMPARACIÓN
        metrics_card = AngledCard(
            scroll_frame,
            title='KPIs Principales TNG',
            header_color=self.theme['secondary']
        )
        metrics_card.pack(fill='both', expand=True, pady=15)

        # Grid de métricas
        self.tng_metrics_grid = ctk.CTkFrame(metrics_card.content_frame, fg_color='transparent')
        self.tng_metrics_grid.pack(fill='x', pady=15)
        self.tng_metrics_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Crear métricas con datos de ejemplo
        self._create_tng_metrics()

        # LISTA DE DEPARTAMENTOS CLICKEABLE (para drill-down)
        dept_card = AngledCard(
            scroll_frame,
            title='Departamentos TNG (Click para Vista Rápida)',
            header_color=self.theme['accent_yellow']
        )
        dept_card.pack(fill='x', pady=15)

        # Frame de departamentos
        dept_frame = ctk.CTkFrame(dept_card.content_frame, fg_color='transparent')
        dept_frame.pack(fill='x', pady=10)

        # Datos de ejemplo de departamentos TNG
        departments = [
            ('Operaciones TNG', 87, 'green'),
            ('Logística TNG', 73, 'orange'),
            ('Mantenimiento TNG', 92, 'green'),
            ('Seguridad TNG', 65, 'red'),
        ]

        for dept_name, completion, status_color in departments:
            dept_btn = ctk.CTkButton(
                dept_frame,
                text=f'🏢  {dept_name} - Tasa Finalización: {completion}%',
                font=get_font('body', 13),
                fg_color=self.theme['surface'],
                text_color=self.theme['text'],
                hover_color=self.theme['primary'],
                anchor='w',
                height=50,
                border_width=2,
                border_color=self.theme[f'accent_{"green" if status_color == "green" else "orange" if status_color == "orange" else "secondary"}'],
                command=lambda name=dept_name, comp=completion: self._show_department_quick_view(name, comp),
                cursor='hand2'
            )
            dept_btn.pack(fill='x', padx=20, pady=5)

        # Marcar como cargado
        self._dashboard_tabs_loaded['Resumen TNG'] = True

    def _create_tng_metrics(self):
        """Crear métricas TNG con datos de ejemplo"""
        # Limpiar métricas existentes
        for widget in self.tng_metrics_grid.winfo_children():
            widget.destroy()

        # Datos de ejemplo según modo de comparación
        if self._tng_comparison_mode == 'Actual':
            metrics_data = [
                ('Empleados TNG', '245', None, self.theme['primary']),
                ('Tasa Finalización', '78.5%', None, self.theme['secondary']),
                ('Módulos Activos', '18', None, self.theme['accent_yellow']),
                ('Críticos Completados', '92%', None, self.theme['accent_green']),
            ]
        elif self._tng_comparison_mode == 'vs Semana Ant.':
            metrics_data = [
                ('Empleados TNG', '245', '+2.1%', self.theme['primary']),
                ('Tasa Finalización', '78.5%', '+3.5%', self.theme['secondary']),
                ('Módulos Activos', '18', '+1', self.theme['accent_yellow']),
                ('Críticos Completados', '92%', '+4.2%', self.theme['accent_green']),
            ]
        elif self._tng_comparison_mode == 'vs Mes Ant.':
            metrics_data = [
                ('Empleados TNG', '245', '+8.4%', self.theme['primary']),
                ('Tasa Finalización', '78.5%', '-1.2%', self.theme['secondary']),
                ('Módulos Activos', '18', '+3', self.theme['accent_yellow']),
                ('Críticos Completados', '92%', '+7.8%', self.theme['accent_green']),
            ]
        else:  # vs Trim. Ant.
            metrics_data = [
                ('Empleados TNG', '245', '+15.2%', self.theme['primary']),
                ('Tasa Finalización', '78.5%', '+5.9%', self.theme['secondary']),
                ('Módulos Activos', '18', '+5', self.theme['accent_yellow']),
                ('Críticos Completados', '92%', '+12.3%', self.theme['accent_green']),
            ]

        # Crear tarjetas de métricas
        for idx, (title, value, comparison, color) in enumerate(metrics_data):
            metric_frame = ctk.CTkFrame(
                self.tng_metrics_grid,
                fg_color=self.theme['surface'],
                corner_radius=10,
                border_width=2,
                border_color=color
            )
            metric_frame.grid(row=0, column=idx, padx=10, pady=10, sticky='nsew')

            # Contenido
            content_frame = ctk.CTkFrame(metric_frame, fg_color='transparent')
            content_frame.pack(fill='both', expand=True, padx=20, pady=20)

            # Título
            title_label = HutchisonLabel(
                content_frame,
                text=title,
                label_type='body'
            )
            title_label.configure(font=get_font('body', 12), text_color=self.theme['text_secondary'])
            title_label.pack()

            # Valor principal
            value_label = HutchisonLabel(
                content_frame,
                text=value,
                label_type='heading'
            )
            value_label.configure(font=get_font('heading', 32, 'bold'), text_color=color)
            value_label.pack(pady=(8, 0))

            # Comparación (si existe)
            if comparison:
                is_positive = comparison.startswith('+')
                comp_color = '#2ecc71' if is_positive else '#e74c3c'
                comp_icon = '▲' if is_positive else '▼'

                comp_label = HutchisonLabel(
                    content_frame,
                    text=f'{comp_icon} {comparison}',
                    label_type='body'
                )
                comp_label.configure(
                    font=get_font('body', 14, 'bold'),
                    text_color=comp_color
                )
                comp_label.pack(pady=(8, 0))

    def _on_tng_comparison_change(self, value):
        """Manejar cambio en el selector de comparación TNG"""
        self._tng_comparison_mode = value
        # Recrear métricas con nuevos datos de comparación
        self._create_tng_metrics()

    def _show_department_quick_view(self, dept_name, completion_rate):
        """Mostrar Vista Rápida de departamento TNG en ventana emergente (TAREA 3)"""
        # Crear ventana CTkToplevel
        quick_view = ctk.CTkToplevel(self.root)
        quick_view.title(f'Vista Rápida - {dept_name}')
        quick_view.geometry('500x450')

        # Centrar ventana
        quick_view.update_idletasks()
        width = quick_view.winfo_width()
        height = quick_view.winfo_height()
        x = (quick_view.winfo_screenwidth() // 2) - (width // 2)
        y = (quick_view.winfo_screenheight() // 2) - (height // 2)
        quick_view.geometry(f'{width}x{height}+{x}+{y}')

        # Hacer modal
        quick_view.grab_set()
        quick_view.attributes('-topmost', True)

        # Frame principal
        main_frame = ctk.CTkFrame(quick_view, fg_color=self.theme['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header angulado
        header = AngledHeaderFrame(
            main_frame,
            text=f'Vista Rápida: {dept_name}',
            height=70,
            color=self.theme['primary']
        )
        header.pack(fill='x', pady=(0, 20))

        # Scroll frame para contenido
        scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True)

        # KPIs específicos del departamento (datos de ejemplo)
        kpis_data = [
            ('Tasa Finalización', f'{completion_rate}%', self.theme['primary']),
            ('Progreso Módulo Crítico 7', '92%', self.theme['secondary']),
            ('Empleados Activos', '45', self.theme['accent_yellow']),
        ]

        for title, value, color in kpis_data:
            kpi_card = ctk.CTkFrame(
                scroll_frame,
                fg_color=self.theme['surface'],
                corner_radius=10,
                border_width=2,
                border_color=color
            )
            kpi_card.pack(fill='x', pady=10)

            # Contenido del KPI
            kpi_content = ctk.CTkFrame(kpi_card, fg_color='transparent')
            kpi_content.pack(fill='x', padx=20, pady=15)

            # Título
            HutchisonLabel(
                kpi_content,
                text=title,
                label_type='body'
            ).configure(font=get_font('body', 12), text_color=self.theme['text_secondary'])
            HutchisonLabel(
                kpi_content,
                text=title,
                label_type='body'
            ).pack(anchor='w')

            # Valor
            HutchisonLabel(
                kpi_content,
                text=value,
                label_type='heading'
            ).configure(font=get_font('heading', 28, 'bold'), text_color=color)
            HutchisonLabel(
                kpi_content,
                text=value,
                label_type='heading'
            ).pack(anchor='w', pady=(5, 0))

        # Información adicional
        info_label = HutchisonLabel(
            scroll_frame,
            text=(
                f'Información detallada del departamento {dept_name}:\n\n' +
                '• Última actualización: Hoy\n' +
                '• Módulos en progreso: 12\n' +
                '• Empleados con alertas: 3\n' +
                '• Próxima evaluación: 15 días'
            ),
            label_type='body'
        )
        info_label.configure(justify='left', wraplength=400)
        info_label.pack(pady=20)

        # Botón cerrar
        close_btn = ctk.CTkButton(
            main_frame,
            text='Cerrar',
            font=get_font('body', 14, 'bold'),
            fg_color=self.theme['secondary'],
            hover_color=self.theme['primary'],
            height=45,
            command=quick_view.destroy
        )
        close_btn.pack(fill='x', pady=(10, 0))

    def _create_metrics_grid(self, parent):
        """Crear grid de métricas con tarjetas anguladas"""
        metrics_grid = ctk.CTkFrame(parent, fg_color='transparent')
        metrics_grid.pack(fill='x', pady=20)

        metrics_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        if self.conn and self.cursor:
            try:
                # Métricas reales de BD
                self.cursor.execute("SELECT COUNT(*) FROM Instituto_Usuario")
                total_users = self.cursor.fetchone()[0]

                self.cursor.execute("SELECT COUNT(*) FROM Instituto_Modulo")
                total_modules = self.cursor.fetchone()[0]

                self.cursor.execute("""
                    SELECT COUNT(*) FROM Instituto_ProgresoModulo
                    WHERE EstatusModuloUsuario = 'Terminado'
                """)
                completed = self.cursor.fetchone()[0]

                self.cursor.execute("""
                    SELECT
                        COUNT(CASE WHEN EstatusModuloUsuario = 'Terminado' THEN 1 END) * 100.0 /
                        NULLIF(COUNT(*), 0) as Porcentaje
                    FROM Instituto_ProgresoModulo
                """)
                result = self.cursor.fetchone()
                progress = f'{result[0]:.1f}%' if result and result[0] else '0%'

            except Exception as e:
                print(f"Error cargando métricas: {e}")
                # Valores por defecto
                total_users = 0
                total_modules = 0
                completed = 0
                progress = '0%'
        else:
            # Modo sin BD - Datos de demostración
            total_users = 156
            total_modules = 24
            completed = 892
            progress = '73.5%'

        # Tarjeta 1
        metric1 = MetricCardAngled(
            metrics_grid,
            title='Total Usuarios',
            value=f'{total_users:,}',
            subtitle='Usuarios en el sistema',
            color=self.theme['primary']
        )
        metric1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Tarjeta 2
        metric2 = MetricCardAngled(
            metrics_grid,
            title='Módulos',
            value=str(total_modules),
            subtitle='Módulos disponibles',
            color=self.theme['secondary']
        )
        metric2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Tarjeta 3
        metric3 = MetricCardAngled(
            metrics_grid,
            title='Completados',
            value=f'{completed:,}',
            subtitle='Módulos terminados',
            color=self.theme['accent_yellow']
        )
        metric3.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # Tarjeta 4
        metric4 = MetricCardAngled(
            metrics_grid,
            title='Progreso Global',
            value=progress,
            subtitle='Del total',
            color=self.theme['accent_orange']
        )
        metric4.grid(row=0, column=3, padx=10, pady=10, sticky='nsew')

    # ==================== CONSULTAS ====================

    def show_consultas(self):
        """Panel de Consultas con diseño Hutchison"""
        self.clear_content_area()
        self.current_panel = 'consultas'

        scroll_frame = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header angulado
        header = AngledHeaderFrame(
            scroll_frame,
            text='Consultas de Usuarios',
            height=80,
            color=self.theme['secondary']
        )
        header.pack(fill='x', pady=(0, 20))

        if not self.conn:
            # Sin conexión a BD
            self._show_no_db_message(scroll_frame, 'consultas')
            return

        # Card de búsqueda
        search_card = AngledCard(
            scroll_frame,
            title='Búsqueda de Usuarios',
            header_color=self.theme['primary']
        )
        search_card.pack(fill='x', pady=20)

        # Búsqueda por ID
        search_frame = ctk.CTkFrame(search_card.content_frame, fg_color='transparent')
        search_frame.pack(fill='x', pady=10)

        HutchisonLabel(
            search_frame,
            text='🔍  Buscar por User ID:',
            label_type='heading'
        ).pack(side='left', padx=(0, 15))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text='Ingrese ID de usuario...',
            font=get_font('body', 14),
            width=300,
            height=40
        )
        self.search_entry.pack(side='left', padx=5)

        HutchisonButton(
            search_frame,
            text='Buscar',
            button_type='primary',
            width=120,
            command=self.search_user
        ).pack(side='left', padx=10)

        # Resultado de búsqueda
        self.search_result_frame = ctk.CTkFrame(
            search_card.content_frame,
            fg_color=self.theme['surface'],
            corner_radius=10
        )
        self.search_result_frame.pack(fill='both', expand=True, pady=(20, 0))

        self.search_result_label = HutchisonLabel(
            self.search_result_frame,
            text='Ingrese un User ID y haga clic en Buscar',
            label_type='body'
        )
        self.search_result_label.pack(pady=30)

        # Card de tabla de usuarios (con tksheet)
        table_card = AngledCard(
            scroll_frame,
            title='Todos los Usuarios (Tabla Interactiva)',
            header_color=self.theme['secondary']
        )
        table_card.pack(fill='both', expand=True, pady=20)

        # Botón para cargar tabla
        load_btn_frame = ctk.CTkFrame(table_card.content_frame, fg_color='transparent')
        load_btn_frame.pack(fill='x', pady=(10, 20))

        HutchisonButton(
            load_btn_frame,
            text='Cargar Todos los Usuarios',
            button_type='secondary',
            command=self._load_users_table
        ).pack(pady=10)

        # Container para la tabla
        self.table_container = ctk.CTkFrame(
            table_card.content_frame,
            fg_color=self.theme['background'],
            corner_radius=10,
            height=400
        )
        self.table_container.pack(fill='both', expand=True, padx=10, pady=10)
        self.table_container.pack_propagate(False)

    def _load_users_table(self):
        """Cargar tabla de usuarios con tksheet"""
        if not self.conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            # Importar tksheet
            from tksheet import Sheet
            import tkinter as tk

            # Limpiar container
            for widget in self.table_container.winfo_children():
                widget.destroy()

            # Obtener datos de usuarios
            self.cursor.execute("""
                SELECT
                    u.UserId,
                    u.Nombre,
                    u.Email,
                    un.NombreUnidad
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un
                    ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                ORDER BY u.UserId
            """)

            rows = self.cursor.fetchall()

            # Crear Sheet
            self.users_sheet = Sheet(
                self.table_container,
                data=[[row[0], row[1] or '', row[2] or '', row[3] or ''] for row in rows],
                headers=['User ID', 'Nombre', 'Email', 'Unidad de Negocio'],
                theme='light blue',
                height=380,
                width=900
            )

            # Configurar colores corporativos Hutchison
            self.users_sheet.change_theme(
                theme='light blue',
                redraw=False
            )

            # Personalizar colores
            self.users_sheet.set_options(
                header_bg=self.theme['secondary'],  # Sea Blue
                header_fg=self.theme['text_on_primary'],  # White
                index_bg=self.theme['surface'],
                index_fg=self.theme['text'],
                table_bg=self.theme['background'],
                table_fg=self.theme['text'],
                table_selected_cells_bg=self.theme['primary'],  # Sky Blue
                table_selected_cells_fg=self.theme['text_on_primary']
            )

            # Habilitar funcionalidades
            self.users_sheet.enable_bindings(
                'single_select',
                'row_select',
                'column_width_resize',
                'arrowkeys',
                'right_click_popup_menu',
                'rc_select',
                'copy',
                'select_all'
            )

            # Menú contextual personalizado
            self.users_sheet.popup_menu_add_command(
                'Eliminar fila seleccionada',
                self._delete_selected_row
            )

            self.users_sheet.pack(fill='both', expand=True)

            messagebox.showinfo(
                "Éxito",
                f"Se cargaron {len(rows)} usuarios en la tabla.\n\n" +
                "Funcionalidades disponibles:\n" +
                "• Click derecho para menú contextual\n" +
                "• Seleccionar filas\n" +
                "• Copiar datos (Ctrl+C)\n" +
                "• Redimensionar columnas"
            )

        except ImportError:
            # Si tksheet no está instalado
            error_label = HutchisonLabel(
                self.table_container,
                text=(
                    'La librería tksheet no está instalada.\n\n'
                    'Instálala con:\n'
                    'pip install tksheet'
                ),
                label_type='body'
            )
            error_label.configure(text_color='red')
            error_label.pack(expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar tabla:\n{str(e)}")

    def _delete_selected_row(self):
        """Eliminar fila seleccionada de la tabla"""
        if not hasattr(self, 'users_sheet'):
            return

        selected = self.users_sheet.get_currently_selected()

        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una fila primero")
            return

        row = selected.row if hasattr(selected, 'row') else selected[0]

        # Confirmar eliminación
        confirm = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar la fila seleccionada de la tabla?\n\n" +
            "(Esto solo la quita de la vista, no de la base de datos)"
        )

        if confirm:
            self.users_sheet.delete_row(row)
            messagebox.showinfo("Éxito", "Fila eliminada de la tabla")

    def search_user(self):
        """Buscar usuario por ID"""
        user_id = self.search_entry.get().strip()

        if not user_id:
            messagebox.showwarning("Advertencia", "Ingrese un User ID")
            return

        if not self.conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            self.cursor.execute("""
                SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                WHERE u.UserId = ?
            """, (user_id,))

            result = self.cursor.fetchone()

            # Limpiar resultado anterior
            for widget in self.search_result_frame.winfo_children():
                widget.destroy()

            if result:
                # Mostrar resultado
                result_container = ctk.CTkFrame(
                    self.search_result_frame,
                    fg_color='transparent'
                )
                result_container.pack(fill='both', expand=True, padx=30, pady=20)

                HutchisonLabel(
                    result_container,
                    text='✓ Usuario Encontrado',
                    label_type='heading'
                ).configure(text_color=self.theme['secondary'])
                HutchisonLabel(
                    result_container,
                    text='✓ Usuario Encontrado',
                    label_type='heading'
                ).pack(pady=(0, 20))

                info_text = f"""
User ID: {result[0]}
Nombre: {result[1] or 'N/A'}
Email: {result[2] or 'N/A'}
Unidad: {result[3] or 'N/A'}
                """.strip()

                HutchisonLabel(
                    result_container,
                    text=info_text,
                    label_type='body'
                ).configure(justify='left')
                HutchisonLabel(
                    result_container,
                    text=info_text,
                    label_type='body'
                ).pack()

            else:
                HutchisonLabel(
                    self.search_result_frame,
                    text=f'✗ No se encontró el usuario: {user_id}',
                    label_type='heading'
                ).configure(text_color='#ff6b6b')
                HutchisonLabel(
                    self.search_result_frame,
                    text=f'✗ No se encontró el usuario: {user_id}',
                    label_type='heading'
                ).pack(pady=30)

        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar:\n{str(e)}")

    # ==================== ACTUALIZAR DATOS ====================

    def show_actualizar(self):
        """Panel de Actualizar con diseño Hutchison"""
        self.clear_content_area()
        self.current_panel = 'actualizar'

        scroll_frame = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header angulado
        header = AngledHeaderFrame(
            scroll_frame,
            text='Actualizar Datos',
            height=80,
            color=self.theme['accent_orange']
        )
        header.pack(fill='x', pady=(0, 20))

        # Card principal
        update_card = AngledCard(
            scroll_frame,
            title='Cargar Archivo Excel',
            header_color=self.theme['primary']
        )
        update_card.pack(fill='x', pady=20)

        # Drop zone
        drop_zone = ctk.CTkFrame(
            update_card.content_frame,
            fg_color=self.theme['surface'],
            corner_radius=15,
            border_width=3,
            border_color=self.theme['primary'],
            height=180
        )
        drop_zone.pack(fill='x', pady=20)
        drop_zone.pack_propagate(False)

        drop_icon = HutchisonLabel(
            drop_zone,
            text='📁',
            label_type='title'
        )
        drop_icon.configure(font=get_font('heading', 64))
        drop_icon.pack(pady=(30, 10))

        if DRAG_DROP_AVAILABLE:
            drop_text = HutchisonLabel(
                drop_zone,
                text='Arrastra archivo Excel aquí',
                label_type='heading'
            )
            drop_text.pack()

            drop_subtext = HutchisonLabel(
                drop_zone,
                text='o usa el botón de abajo',
                label_type='caption'
            )
            drop_subtext.pack(pady=5)

            # Configurar drag & drop
            try:
                drop_zone.drop_target_register(DND_FILES)
                drop_zone.dnd_bind('<<Drop>>', self._on_file_drop)
                drop_zone.dnd_bind('<<DragEnter>>',
                    lambda e: drop_zone.configure(border_color=self.theme['secondary']))
                drop_zone.dnd_bind('<<DragLeave>>',
                    lambda e: drop_zone.configure(border_color=self.theme['primary']))
            except:
                pass
        else:
            drop_text = HutchisonLabel(
                drop_zone,
                text='Usar botón para seleccionar archivo',
                label_type='heading'
            )
            drop_text.pack()

        # Botón seleccionar
        HutchisonButton(
            update_card.content_frame,
            text='📂  Seleccionar Archivo Excel',
            button_type='primary',
            command=self.select_file
        ).pack(pady=20)

        # Información del archivo
        self.file_info_frame = ctk.CTkFrame(
            update_card.content_frame,
            fg_color=self.theme['surface'],
            corner_radius=10
        )
        self.file_info_frame.pack(fill='x', pady=10)

        self.file_info_label = HutchisonLabel(
            self.file_info_frame,
            text='Ningún archivo seleccionado',
            label_type='body'
        )
        self.file_info_label.pack(pady=20)

    def select_file(self):
        """Seleccionar archivo Excel"""
        file_path = filedialog.askopenfilename(
            title='Seleccionar archivo Excel',
            filetypes=[
                ('Excel files', '*.xlsx *.xls'),
                ('CSV files', '*.csv'),
                ('All files', '*.*')
            ]
        )

        if file_path:
            self._load_file(file_path)

    def _on_file_drop(self, event):
        """Manejar drag & drop"""
        file_path = event.data.strip('{}')

        if not file_path.lower().endswith(('.xlsx', '.xls', '.csv')):
            messagebox.showerror("Archivo Inválido",
                f"Por favor selecciona un archivo Excel o CSV.\n\n" +
                f"Archivo: {os.path.basename(file_path)}")
            return

        self._load_file(file_path)

    def _load_file(self, file_path):
        """Cargar y procesar archivo"""
        try:
            self.current_file = file_path

            # Leer archivo
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            # Actualizar UI
            for widget in self.file_info_frame.winfo_children():
                widget.destroy()

            info_container = ctk.CTkFrame(self.file_info_frame, fg_color='transparent')
            info_container.pack(fill='both', expand=True, padx=20, pady=20)

            HutchisonLabel(
                info_container,
                text='✓ Archivo Cargado',
                label_type='heading'
            ).configure(text_color=self.theme['secondary'])
            HutchisonLabel(
                info_container,
                text='✓ Archivo Cargado',
                label_type='heading'
            ).pack(pady=(0, 10))

            info_text = f"""
Archivo: {os.path.basename(file_path)}
Registros: {len(df):,}
Columnas: {len(df.columns)}
            """.strip()

            HutchisonLabel(
                info_container,
                text=info_text,
                label_type='body'
            ).pack()

            # Botón procesar
            if self.conn:
                HutchisonButton(
                    info_container,
                    text='⚙️  Procesar Datos',
                    button_type='secondary',
                    command=lambda: self._process_file(df)
                ).pack(pady=(20, 0))
            else:
                HutchisonLabel(
                    info_container,
                    text='\n⚠️ Requiere conexión a BD para procesar',
                    label_type='caption'
                ).configure(text_color='#ff6b6b')
                HutchisonLabel(
                    info_container,
                    text='\n⚠️ Requiere conexión a BD para procesar',
                    label_type='caption'
                ).pack()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivo:\n{str(e)}")

    def _process_file(self, df):
        """Procesar datos del archivo"""
        if not self.conn:
            messagebox.showerror("Error", "Requiere conexión a base de datos")
            return

        if not self.processor:
            messagebox.showerror("Error", "Procesador no disponible sin conexión a BD")
            return

        try:
            # Procesar con el TranscriptProcessor
            changes = self.processor.process_transcript(df, self.cursor, self.conn)
            self.changes_log = changes

            messagebox.showinfo("Éxito",
                f"Datos procesados correctamente.\n\n" +
                f"Cambios realizados: {len(changes)}")

            # Refrescar dashboard si está visible
            if self.current_panel == 'dashboard':
                self.show_dashboard()

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar:\n{str(e)}")

    # ==================== CONFIGURACIÓN ====================

    def show_configuracion(self):
        """Panel de Configuración con diseño Hutchison"""
        self.clear_content_area()
        self.current_panel = 'configuracion'

        main_frame = ctk.CTkFrame(self.content_area, fg_color='transparent')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header angulado
        header = AngledHeaderFrame(
            main_frame,
            text='Configuración',
            height=80,
            color=self.theme['primary']
        )
        header.pack(fill='x', pady=(0, 20))

        # Divisor
        divider = AngledDivider(
            main_frame,
            height=4,
            color=self.theme['secondary']
        )
        divider.pack(fill='x', pady=(0, 30))

        # Grid 2x2
        grid_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        grid_frame.pack(fill='both', expand=True)

        grid_frame.grid_columnconfigure((0, 1), weight=1)
        grid_frame.grid_rowconfigure((0, 1), weight=1)

        # Tarjetas
        HutchisonConfigCard(
            grid_frame,
            icon='👥',
            title='Gestionar Usuarios',
            description='Agregar nuevos usuarios o editar información existente',
            button_text='Gestionar',
            button_color=self.theme['primary'],
            command=self.show_user_management
        ).grid(row=0, column=0, padx=15, pady=15, sticky='nsew')

        HutchisonConfigCard(
            grid_frame,
            icon='💾',
            title='Respaldar Base de Datos',
            description='Crear un respaldo de seguridad de la BD',
            button_text='Respaldar',
            button_color=self.theme['secondary'],
            command=self.backup_database
        ).grid(row=0, column=1, padx=15, pady=15, sticky='nsew')

        HutchisonConfigCard(
            grid_frame,
            icon='ℹ️',
            title='Acerca de',
            description='Información sobre Smart Reports v2.0',
            button_text='Ver Info',
            button_color=self.theme['accent_yellow'],
            command=self.show_about
        ).grid(row=1, column=0, padx=15, pady=15, sticky='nsew')

        HutchisonConfigCard(
            grid_frame,
            icon='🔧',
            title='Configuración BD',
            description='Configurar conexión a base de datos',
            button_text='Configurar',
            button_color=self.theme['accent_orange'],
            command=self.show_database_config
        ).grid(row=1, column=1, padx=15, pady=15, sticky='nsew')

    def show_user_management(self):
        """Mostrar gestión de usuarios"""
        if not self.conn:
            messagebox.showerror("Error",
                "Requiere conexión a la base de datos.\n\n" +
                "Configura la conexión en smart_reports/config/settings.py")
            return

        dialog = UserManagementDialog(self.root, self.conn)
        self.root.wait_window(dialog)

        if dialog.result in ['created', 'updated'] and self.current_panel == 'dashboard':
            self.show_dashboard()

    def backup_database(self):
        """Respaldar base de datos"""
        from smart_reports.config.settings import DB_TYPE

        if DB_TYPE == 'sqlserver':
            messagebox.showinfo("Respaldo SQL Server",
                "Para respaldar SQL Server:\n\n" +
                "1. SQL Server Management Studio\n" +
                "2. Click derecho → Tasks → Back Up\n\n" +
                "O ejecuta:\n" +
                "BACKUP DATABASE [nombre] TO DISK = 'ruta.bak'")
        else:
            messagebox.showinfo("Respaldo MySQL",
                "Para respaldar MySQL:\n\n" +
                "mysqldump -u root -p [database] > backup.sql")

    def show_about(self):
        """Mostrar información"""
        messagebox.showinfo("Acerca de",
            "SMART REPORTS V2.0\n" +
            "DISEÑO CORPORATIVO HUTCHISON PORTS\n\n" +
            "Sistema de Gestión de Capacitaciones\n" +
            "Instituto Hutchison Ports\n\n" +
            "© 2025 - Todos los derechos reservados\n\n" +
            "Diseño según Manual de Identidad Visual HP")

    def show_database_config(self):
        """Mostrar configuración de BD"""
        from smart_reports.config.settings import DB_TYPE

        current = "SQL Server" if DB_TYPE == 'sqlserver' else "MySQL"
        status = "✓ Conectado" if self.conn else "✗ Desconectado"

        messagebox.showinfo("Configuración BD",
            f"Base de datos actual: {current}\n" +
            f"Estado: {status}\n\n" +
            "Para cambiar:\n" +
            "1. Edita: smart_reports/config/settings.py\n" +
            "2. Modifica DB_TYPE y configuración\n" +
            "3. Reinicia la aplicación")

    def _show_no_db_message(self, parent, panel_name):
        """Mostrar mensaje cuando no hay BD"""
        message_frame = ctk.CTkFrame(parent, fg_color='transparent')
        message_frame.pack(fill='both', expand=True, pady=50)

        HutchisonLabel(
            message_frame,
            text='⚠️ Sin Conexión a Base de Datos',
            label_type='title'
        ).configure(text_color='#ff6b6b')
        HutchisonLabel(
            message_frame,
            text='⚠️ Sin Conexión a Base de Datos',
            label_type='title'
        ).pack(pady=(0, 20))

        HutchisonLabel(
            message_frame,
            text=f'El panel de {panel_name} requiere conexión a la base de datos.\n\n' +
                 'Configura la conexión en:\n' +
                 'smart_reports/config/settings.py',
            label_type='body'
        ).pack()


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("SMART REPORTS - HUTCHISON PORTS")
    print("Diseño Corporativo v2.0")
    print("="*70 + "\n")

    # Crear root con soporte DnD si está disponible
    if DRAG_DROP_AVAILABLE:
        try:
            root = TkinterDnD.Tk()
            root.configure(bg='#FFFFFF')
        except:
            root = ctk.CTk()
    else:
        root = ctk.CTk()

    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
