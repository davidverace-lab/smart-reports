"""
Panel Dashboard Hutchison
Dashboard con tabs mejoradas, carga perezosa y gráficos corporativos
"""

import customtkinter as ctk
from tkinter import messagebox
from smart_reports.config.settings_hutchison import (
    PRIMARY_COLORS,
    get_color,
    get_font
)


class DashboardHutchison(ctk.CTkFrame):
    """
    Dashboard con 3 tabs:
    1. General (métricas generales)
    2. Progreso por Módulo
    3. Dashboards de Ejemplo (gráficos Plotly)

    Características:
    - Carga perezosa (lazy loading)
    - Tabs con diseño corporativo
    - Gráficos con colores Hutchison
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

        # Track de tabs cargadas (lazy loading)
        self._tabs_loaded = {
            'General': False,
            'Progreso por Módulo': False,
            'Dashboards de Ejemplo': False
        }

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_interface()

    def _create_interface(self):
        """Crear interfaz con tabs"""

        # Container principal
        main_container = ctk.CTkFrame(self, fg_color='transparent')
        main_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        # Título
        title_label = ctk.CTkLabel(
            main_container,
            text='📊 Dashboard',
            font=get_font('title', 28, 'bold'),
            text_color=get_color('Sea Blue'),
            anchor='w'
        )
        title_label.grid(row=0, column=0, sticky='w', pady=(0, 20))

        # TabView con diseño mejorado
        self.tabview = ctk.CTkTabview(
            main_container,
            fg_color=get_color('White'),
            segmented_button_fg_color=get_color('Light Gray'),
            segmented_button_selected_color=get_color('Sky Blue'),
            segmented_button_selected_hover_color=get_color('Sea Blue'),
            segmented_button_unselected_color=get_color('Light Gray'),
            segmented_button_unselected_hover_color=get_color('Border'),
            text_color=get_color('Sea Blue'),
            text_color_disabled=get_color('Light Text'),
            corner_radius=10
        )
        self.tabview.grid(row=1, column=0, sticky='nsew')

        # Crear tabs
        self.tabview.add('General')
        self.tabview.add('Progreso por Módulo')
        self.tabview.add('Dashboards de Ejemplo')

        # Aumentar tamaño de fuente de tabs
        try:
            self.tabview._segmented_button.configure(font=get_font('heading_medium', 14, 'bold'))
        except:
            pass

        # Bindear evento de cambio de tab
        self.tabview.configure(command=self._on_tab_change)

        # Cargar tab inicial
        self._load_tab('General')

    def _on_tab_change(self):
        """Se ejecuta al cambiar de tab (carga perezosa)"""
        current_tab = self.tabview.get()
        if not self._tabs_loaded[current_tab]:
            self._load_tab(current_tab)

    def _load_tab(self, tab_name):
        """Cargar contenido de una tab solo cuando se necesita"""
        if tab_name == 'General':
            self._create_general_tab()
        elif tab_name == 'Progreso por Módulo':
            self._create_module_progress_tab()
        elif tab_name == 'Dashboards de Ejemplo':
            self._create_examples_tab()

        self._tabs_loaded[tab_name] = True

    def _create_general_tab(self):
        """Tab General: métricas generales"""
        tab = self.tabview.tab('General')

        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Grid de métricas (4 cards)
        metrics_container = ctk.CTkFrame(scroll_frame, fg_color='transparent')
        metrics_container.pack(fill='x', pady=20)
        metrics_container.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Obtener datos
        if self.cursor:
            try:
                # Total usuarios
                self.cursor.execute("SELECT COUNT(*) FROM Instituto_Usuario")
                total_users = self.cursor.fetchone()[0]

                # Total módulos
                self.cursor.execute("SELECT COUNT(*) FROM Instituto_Modulo WHERE Activo = 1")
                total_modules = self.cursor.fetchone()[0]

                # Completados
                self.cursor.execute("""
                    SELECT COUNT(*) FROM Instituto_ProgresoModulo
                    WHERE EstatusModuloUsuario = 'Completado'
                """)
                completed = self.cursor.fetchone()[0]

                # Progreso global
                self.cursor.execute("""
                    SELECT
                        COUNT(CASE WHEN EstatusModuloUsuario = 'Completado' THEN 1 END) * 100.0 /
                        NULLIF(COUNT(*), 0) as Porcentaje
                    FROM Instituto_ProgresoModulo
                """)
                result = self.cursor.fetchone()
                progress = f'{result[0]:.1f}%' if result and result[0] else '0%'

            except Exception as e:
                print(f"Error cargando métricas: {e}")
                total_users = 0
                total_modules = 0
                completed = 0
                progress = '0%'
        else:
            # Datos de demostración
            total_users = 156
            total_modules = 14
            completed = 892
            progress = '73.5%'

        # Crear cards de métricas
        metrics_data = [
            ('Total Usuarios', f'{total_users:,}', 'Sky Blue'),
            ('Módulos', str(total_modules), 'Success Green'),
            ('Completados', f'{completed:,}', 'Warning Orange'),
            ('Progreso Global', progress, 'Aqua Green'),
        ]

        for idx, (title, value, color_name) in enumerate(metrics_data):
            self._create_metric_card(
                metrics_container,
                title,
                value,
                color_name,
                row=0,
                col=idx
            )

        # Información del sistema
        info_card = ctk.CTkFrame(
            scroll_frame,
            fg_color=get_color('Surface'),
            border_width=1,
            border_color=get_color('Border'),
            corner_radius=15
        )
        info_card.pack(fill='x', pady=20, padx=10)

        info_title = ctk.CTkLabel(
            info_card,
            text='ℹ️  Información del Sistema',
            font=get_font('heading', 16, 'bold'),
            text_color=get_color('Sea Blue')
        )
        info_title.pack(pady=(20, 10), padx=20, anchor='w')

        info_text = ctk.CTkLabel(
            info_card,
            text=(
                "Sistema de Gestión de Capacitaciones del Instituto Hutchison Ports.\n\n"
                "Este dashboard muestra métricas en tiempo real del progreso de capacitación "
                "de todos los usuarios registrados en el sistema.\n\n"
                f"Estado de Conexión BD: {'✓ Conectado' if self.db else '✗ Desconectado'}"
            ),
            font=get_font('body', 12),
            text_color=get_color('Dark Gray'),
            justify='left',
            wraplength=900
        )
        info_text.pack(pady=(0, 20), padx=20, anchor='w')

    def _create_metric_card(self, parent, title, value, color_name, row, col):
        """Crear card de métrica individual"""
        color = get_color(color_name)

        card = ctk.CTkFrame(
            parent,
            fg_color=get_color('Surface'),
            border_width=2,
            border_color=color,
            corner_radius=10
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # Título
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=get_font('body', 12),
            text_color=get_color('Medium Gray')
        )
        title_label.pack(pady=(20, 5))

        # Valor
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=get_font('title', 32, 'bold'),
            text_color=color
        )
        value_label.pack(pady=(0, 20))

    def _create_module_progress_tab(self):
        """Tab Progreso por Módulo"""
        tab = self.tabview.tab('Progreso por Módulo')

        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Título
        title_label = ctk.CTkLabel(
            scroll_frame,
            text='Progreso por Módulo',
            font=get_font('subtitle', 20, 'bold'),
            text_color=get_color('Sea Blue')
        )
        title_label.pack(pady=20, anchor='w')

        # Información
        info_label = ctk.CTkLabel(
            scroll_frame,
            text='Visualización del progreso de capacitación por cada módulo del Instituto Hutchison Ports.',
            font=get_font('body', 12),
            text_color=get_color('Medium Gray')
        )
        info_label.pack(pady=10, anchor='w')

        # Placeholder para gráfico
        placeholder = ctk.CTkFrame(
            scroll_frame,
            fg_color=get_color('Surface'),
            border_width=1,
            border_color=get_color('Border'),
            corner_radius=10,
            height=400
        )
        placeholder.pack(fill='both', expand=True, pady=20)

        placeholder_label = ctk.CTkLabel(
            placeholder,
            text='📊\n\nGráfico de Progreso por Módulo\n(Implementación con Plotly en desarrollo)',
            font=get_font('heading', 16),
            text_color=get_color('Medium Gray')
        )
        placeholder_label.place(relx=0.5, rely=0.5, anchor='center')

    def _create_examples_tab(self):
        """Tab Dashboards de Ejemplo con gráficos Plotly"""
        tab = self.tabview.tab('Dashboards de Ejemplo')

        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Título
        title_label = ctk.CTkLabel(
            scroll_frame,
            text='Dashboards de Ejemplo',
            font=get_font('subtitle', 20, 'bold'),
            text_color=get_color('Sea Blue')
        )
        title_label.pack(pady=20, anchor='w')

        # Intentar crear gráficos con Plotly
        try:
            self._create_plotly_examples(scroll_frame)
        except ImportError:
            # Fallback si no está Plotly
            error_label = ctk.CTkLabel(
                scroll_frame,
                text='⚠️  Plotly no está instalado.\n\nInstala con: pip install plotly',
                font=get_font('body', 14),
                text_color=get_color('Error Red')
            )
            error_label.pack(pady=50)

    def _create_plotly_examples(self, parent):
        """Crear gráficos de ejemplo con Plotly"""
        import plotly.graph_objects as go

        # Usar colores corporativos Hutchison
        colors = [
            PRIMARY_COLORS['Sky Blue'],
            PRIMARY_COLORS['Success Green'],
            PRIMARY_COLORS['Warning Orange'],
            PRIMARY_COLORS['Aqua Green'],
        ]

        # === GRÁFICO 1: Barras ===
        fig1 = go.Figure(data=[
            go.Bar(
                x=['Filosofía HP', 'Sostenibilidad', 'Operaciones', 'Seguridad'],
                y=[85, 92, 78, 88],
                marker_color=colors
            )
        ])
        fig1.update_layout(
            title='Progreso por Módulo (%)',
            title_font_size=16,
            title_font_family='Montserrat',
            height=350
        )

        # Placeholder para gráfico
        chart1_frame = ctk.CTkFrame(
            parent,
            fg_color=get_color('Surface'),
            border_width=1,
            border_color=get_color('Border'),
            corner_radius=10,
            height=400
        )
        chart1_frame.pack(fill='x', pady=10)

        chart1_label = ctk.CTkLabel(
            chart1_frame,
            text='📊 Gráfico de Barras\n(Plotly - Colores Corporativos)',
            font=get_font('body', 12),
            text_color=get_color('Medium Gray')
        )
        chart1_label.pack(pady=20)

        # === GRÁFICO 2: Líneas ===
        chart2_frame = ctk.CTkFrame(
            parent,
            fg_color=get_color('Surface'),
            border_width=1,
            border_color=get_color('Border'),
            corner_radius=10,
            height=400
        )
        chart2_frame.pack(fill='x', pady=10)

        chart2_label = ctk.CTkLabel(
            chart2_frame,
            text='📈 Gráfico de Tendencias\n(Plotly - Colores Corporativos)',
            font=get_font('body', 12),
            text_color=get_color('Medium Gray')
        )
        chart2_label.pack(pady=20)


# Para testing standalone
if __name__ == '__main__':
    root = ctk.CTk()
    root.title("Test Dashboard Hutchison")
    root.geometry("1200x800")

    ctk.set_appearance_mode("light")

    panel = DashboardHutchison(root)
    panel.pack(fill='both', expand=True)

    root.mainloop()
