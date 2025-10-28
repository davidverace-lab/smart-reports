"""
Panel Dashboard Modern - Diseño Oscuro
Idéntico a Hutchison pero con colores oscuros
"""

import customtkinter as ctk
from smart_reports.config.settings_modern import (
    PRIMARY_COLORS_MODERN, get_color_modern, get_font_modern
)


class DashboardModern(ctk.CTkFrame):
    """Dashboard con diseño oscuro y tipografía corporativa"""

    def __init__(self, parent, db=None):
        super().__init__(parent, fg_color=get_color_modern('background'))
        self.db = db
        self.cursor = db.get_cursor() if db else None
        self._tabs_loaded = {'General': False, 'Progreso por Módulo': False, 'Dashboards de Ejemplo': False}
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_interface()

    def _create_interface(self):
        main_container = ctk.CTkFrame(self, fg_color='transparent')
        main_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        # Título
        title_label = ctk.CTkLabel(
            main_container, text='📊 Dashboard',
            font=get_font_modern('title', 28, 'bold'),
            text_color=get_color_modern('text_primary'), anchor='w'
        )
        title_label.grid(row=0, column=0, sticky='w', pady=(0, 20))

        # TabView oscuro
        self.tabview = ctk.CTkTabview(
            main_container,
            fg_color=get_color_modern('surface'),
            segmented_button_fg_color=get_color_modern('surface_light'),
            segmented_button_selected_color=get_color_modern('accent_primary'),
            segmented_button_selected_hover_color=get_color_modern('accent_secondary'),
            segmented_button_unselected_color=get_color_modern('surface_light'),
            segmented_button_unselected_hover_color=get_color_modern('surface_hover'),
            text_color=get_color_modern('text_primary'),
            corner_radius=10
        )
        self.tabview.grid(row=1, column=0, sticky='nsew')

        self.tabview.add('General')
        self.tabview.add('Progreso por Módulo')
        self.tabview.add('Dashboards de Ejemplo')

        try:
            self.tabview._segmented_button.configure(font=get_font_modern('heading_medium', 14, 'bold'))
        except:
            pass

        self.tabview.configure(command=self._on_tab_change)
        self._load_tab('General')

    def _on_tab_change(self):
        current_tab = self.tabview.get()
        if not self._tabs_loaded[current_tab]:
            self._load_tab(current_tab)

    def _load_tab(self, tab_name):
        if tab_name == 'General':
            self._create_general_tab()
        elif tab_name == 'Progreso por Módulo':
            self._create_placeholder(tab_name, '📊 Progreso por Módulo')
        elif tab_name == 'Dashboards de Ejemplo':
            self._create_placeholder(tab_name, '📈 Dashboards de Ejemplo')
        self._tabs_loaded[tab_name] = True

    def _create_general_tab(self):
        tab = self.tabview.tab('General')
        scroll_frame = ctk.CTkScrollableFrame(tab, fg_color='transparent')
        scroll_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Métricas
        metrics_container = ctk.CTkFrame(scroll_frame, fg_color='transparent')
        metrics_container.pack(fill='x', pady=20)
        metrics_container.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Obtener datos
        if self.cursor:
            try:
                self.cursor.execute("SELECT COUNT(*) FROM Instituto_Usuario")
                total_users = self.cursor.fetchone()[0]
                self.cursor.execute("SELECT COUNT(*) FROM Instituto_Modulo WHERE Activo = 1")
                total_modules = self.cursor.fetchone()[0]
                self.cursor.execute("SELECT COUNT(*) FROM Instituto_ProgresoModulo WHERE EstatusModuloUsuario = 'Completado'")
                completed = self.cursor.fetchone()[0]
                progress = '73.5%'
            except:
                total_users, total_modules, completed, progress = 0, 0, 0, '0%'
        else:
            total_users, total_modules, completed, progress = 156, 14, 892, '73.5%'

        metrics_data = [
            ('Total Usuarios', f'{total_users:,}', 'accent_primary'),
            ('Módulos', str(total_modules), 'accent_green'),
            ('Completados', f'{completed:,}', 'accent_orange'),
            ('Progreso Global', progress, 'accent_aqua'),
        ]

        for idx, (title, value, color_name) in enumerate(metrics_data):
            self._create_metric_card(metrics_container, title, value, color_name, 0, idx)

        # Info
        info_card = ctk.CTkFrame(scroll_frame, fg_color=get_color_modern('surface'), border_width=1,
                                 border_color=get_color_modern('border'), corner_radius=15)
        info_card.pack(fill='x', pady=20, padx=10)

        info_title = ctk.CTkLabel(info_card, text='ℹ️  Información del Sistema',
                                  font=get_font_modern('heading', 16, 'bold'),
                                  text_color=get_color_modern('text_primary'))
        info_title.pack(pady=(20, 10), padx=20, anchor='w')

        info_text = ctk.CTkLabel(info_card,
            text=f"Sistema de Gestión de Capacitaciones del Instituto Hutchison Ports.\n\nEstado de Conexión BD: {'✓ Conectado' if self.db else '✗ Desconectado'}",
            font=get_font_modern('body', 12), text_color=get_color_modern('text_secondary'),
            justify='left', wraplength=900)
        info_text.pack(pady=(0, 20), padx=20, anchor='w')

    def _create_metric_card(self, parent, title, value, color_name, row, col):
        color = get_color_modern(color_name)
        card = ctk.CTkFrame(parent, fg_color=get_color_modern('surface'), border_width=2,
                           border_color=color, corner_radius=10)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        title_label = ctk.CTkLabel(card, text=title, font=get_font_modern('body', 12),
                                   text_color=get_color_modern('text_secondary'))
        title_label.pack(pady=(20, 5))

        value_label = ctk.CTkLabel(card, text=value, font=get_font_modern('title', 32, 'bold'), text_color=color)
        value_label.pack(pady=(0, 20))

    def _create_placeholder(self, tab_name, text):
        tab = self.tabview.tab(tab_name)
        placeholder = ctk.CTkFrame(tab, fg_color=get_color_modern('surface'), border_width=1,
                                  border_color=get_color_modern('border'), corner_radius=10, height=400)
        placeholder.pack(fill='both', expand=True, pady=20, padx=10)
        
        label = ctk.CTkLabel(placeholder, text=f'{text}\n(Implementación en desarrollo)',
                            font=get_font_modern('heading', 16), text_color=get_color_modern('text_secondary'))
        label.place(relx=0.5, rely=0.5, anchor='center')
