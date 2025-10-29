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

        # TabView con diseño MEJORADO (CRÍTICO: tabs más grandes y visibles)
        self.tabview = ctk.CTkTabview(
            main_container,
            fg_color=get_color_modern('surface'),
            segmented_button_fg_color=get_color_modern('surface_dark'),
            segmented_button_selected_color=get_color_modern('Sky Blue'),  # Corporativo
            segmented_button_selected_hover_color=get_color_modern('Sea Blue'),  # Corporativo
            segmented_button_unselected_color=get_color_modern('surface_dark'),
            segmented_button_unselected_hover_color=get_color_modern('surface_hover'),
            text_color='white',  # Texto blanco en tab activa
            text_color_disabled=get_color_modern('text_secondary'),  # Texto gris en tabs inactivas
            corner_radius=10,
            height=45  # Altura mínima para tabs más grandes
        )
        self.tabview.grid(row=1, column=0, sticky='nsew')

        self.tabview.add('General')
        self.tabview.add('Progreso por Módulo')
        self.tabview.add('Dashboards de Ejemplo')

        # CRÍTICO: Aumentar tamaño de fuente de tabs a 13px Bold Montserrat
        try:
            self.tabview._segmented_button.configure(
                font=('Montserrat', 13, 'bold'),
                height=45  # Altura de botones de tabs
            )
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
        """Tab General: métricas generales según captura (3 cards + 2 charts)"""
        tab = self.tabview.tab('General')
        scroll_frame = ctk.CTkScrollableFrame(tab, fg_color='transparent')
        scroll_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # ═══════════════════════════════════════════════════
        # ROW 1: Grid de métricas (3 CARDS según captura)
        # ═══════════════════════════════════════════════════
        metrics_container = ctk.CTkFrame(scroll_frame, fg_color='transparent')
        metrics_container.pack(fill='x', pady=(0, 20))
        metrics_container.grid_columnconfigure((0, 1, 2), weight=1)

        # Obtener datos
        if self.cursor:
            try:
                # Total usuarios
                self.cursor.execute("SELECT COUNT(*) FROM Instituto_Usuario")
                total_users = self.cursor.fetchone()[0]

                # Total módulos activos y total
                self.cursor.execute("SELECT COUNT(*) FROM Instituto_Modulo WHERE Activo = 1")
                active_modules = self.cursor.fetchone()[0]
                self.cursor.execute("SELECT COUNT(*) FROM Instituto_Modulo")
                total_modules = self.cursor.fetchone()[0]

                # Tasa de completado
                self.cursor.execute("""
                    SELECT
                        COUNT(CASE WHEN EstatusModuloUsuario = 'Completado' THEN 1 END) * 100.0 /
                        NULLIF(COUNT(*), 0) as Porcentaje
                    FROM Instituto_ProgresoModulo
                """)
                result = self.cursor.fetchone()
                completion_rate = f'{result[0]:.1f}%' if result and result[0] else '0.0%'

            except Exception as e:
                print(f"Error cargando métricas: {e}")
                total_users = 0
                active_modules = 0
                total_modules = 14
                completion_rate = '0.0%'
        else:
            # Datos de demostración
            total_users = 1525
            active_modules = 0
            total_modules = 14
            completion_rate = '0.0%'

        # Crear 3 cards de métricas según captura
        metrics_data = [
            ('👥', 'Total de Usuarios', f'{total_users:,}', 'Sky Blue'),
            ('📚', 'Módulos Activos', f'{active_modules}/{total_modules}', 'accent_green'),
            ('✅', 'Tasa de Completado', completion_rate, 'accent_orange'),
        ]

        for idx, (icon, title, value, color_name) in enumerate(metrics_data):
            self._create_metric_card_with_icon(
                metrics_container,
                icon,
                title,
                value,
                color_name,
                row=0,
                col=idx
            )

        # ═══════════════════════════════════════════════════
        # ROW 2: Gráficos (2 charts lado a lado)
        # ═══════════════════════════════════════════════════
        charts_container = ctk.CTkFrame(scroll_frame, fg_color='transparent')
        charts_container.pack(fill='both', expand=True, pady=(0, 20))
        charts_container.grid_columnconfigure((0, 1), weight=1)
        charts_container.grid_rowconfigure(0, weight=1)

        # Chart 1: Usuarios por Unidad de Negocio (Barras Horizontales)
        chart1 = self._create_chart_barh(charts_container)
        chart1.grid(row=0, column=0, padx=(0, 10), sticky='nsew')

        # Chart 2: Distribución Porcentual (Donut)
        chart2 = self._create_chart_donut(charts_container)
        chart2.grid(row=0, column=1, padx=(10, 0), sticky='nsew')

    def _create_metric_card_with_icon(self, parent, icon, title, value, color_name, row, col):
        """Crear card de métrica con icono según diseño de captura - Versión Modern"""
        color = get_color_modern(color_name)

        card = ctk.CTkFrame(
            parent,
            fg_color=get_color_modern('surface_card'),
            border_width=2,
            border_color=get_color_modern('border'),
            corner_radius=12,
            height=160
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        card.grid_propagate(False)

        # Container interior
        inner = ctk.CTkFrame(card, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=20, pady=20)

        # Icono grande
        icon_label = ctk.CTkLabel(
            inner,
            text=icon,
            font=('Arial', 40),
            text_color=color
        )
        icon_label.pack(pady=(10, 5))

        # Título
        title_label = ctk.CTkLabel(
            inner,
            text=title,
            font=('Arial', 11),
            text_color=get_color_modern('text_secondary')
        )
        title_label.pack(pady=(0, 5))

        # Valor grande
        value_label = ctk.CTkLabel(
            inner,
            text=value,
            font=('Montserrat', 28, 'bold'),
            text_color=get_color_modern('text_primary')
        )
        value_label.pack(pady=(0, 10))

    def _create_chart_barh(self, parent):
        """Crear gráfico de barras horizontales: Usuarios por Unidad - Versión Modern"""
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color=get_color_modern('surface_card'),
            border_width=1,
            border_color=get_color_modern('border'),
            corner_radius=12
        )

        # Título del chart
        title = ctk.CTkLabel(
            chart_frame,
            text='📊  Usuarios por Unidad de Negocio',
            font=('Montserrat', 14, 'bold'),
            text_color=get_color_modern('text_primary'),
            anchor='w'
        )
        title.pack(pady=(20, 15), padx=20, anchor='w')

        # Obtener datos
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT
                        un.NombreUnidad,
                        COUNT(u.UserId) as TotalUsuarios
                    FROM Instituto_UnidadDeNegocio un
                    LEFT JOIN Instituto_Usuario u ON un.IdUnidad = u.IdUnidadDeNegocio
                    GROUP BY un.NombreUnidad
                    ORDER BY TotalUsuarios DESC
                """)
                data = self.cursor.fetchall()
                units = [row[0] for row in data]
                counts = [row[1] for row in data]
            except:
                units = ['CCI', 'SANCHEZ', 'DENNIS', 'HPMX']
                counts = [450, 380, 320, 375]
        else:
            units = ['CCI', 'SANCHEZ', 'DENNIS', 'HPMX']
            counts = [450, 380, 320, 375]

        # Crear canvas para barras simples
        canvas_container = ctk.CTkFrame(chart_frame, fg_color='transparent')
        canvas_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Barras horizontales simples con CTk
        max_count = max(counts) if counts else 1
        colors = [
            get_color_modern('Sky Blue'),
            get_color_modern('accent_green'),
            get_color_modern('accent_orange'),
            get_color_modern('accent_purple')
        ]

        for idx, (unit, count) in enumerate(zip(units, counts)):
            # Frame para cada barra
            bar_frame = ctk.CTkFrame(canvas_container, fg_color='transparent')
            bar_frame.pack(fill='x', pady=8)

            # Label de unidad
            unit_label = ctk.CTkLabel(
                bar_frame,
                text=unit,
                font=('Arial', 11),
                text_color=get_color_modern('text_primary'),
                width=100,
                anchor='w'
            )
            unit_label.pack(side='left', padx=(0, 10))

            # Barra de progreso
            bar_width = int((count / max_count) * 400) if max_count > 0 else 0
            color = colors[idx % len(colors)]

            bar = ctk.CTkFrame(
                bar_frame,
                fg_color=color,
                width=bar_width,
                height=30,
                corner_radius=6
            )
            bar.pack(side='left', padx=(0, 10))
            bar.pack_propagate(False)

            # Valor dentro de la barra
            value_label = ctk.CTkLabel(
                bar,
                text=str(count),
                font=('Montserrat', 11, 'bold'),
                text_color='white'
            )
            value_label.place(relx=0.5, rely=0.5, anchor='center')

        return chart_frame

    def _create_chart_donut(self, parent):
        """Crear gráfico tipo donut: Distribución Porcentual - Versión Modern"""
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color=get_color_modern('surface_card'),
            border_width=1,
            border_color=get_color_modern('border'),
            corner_radius=12
        )

        # Título del chart
        title = ctk.CTkLabel(
            chart_frame,
            text='📈  Distribución Porcentual',
            font=('Montserrat', 14, 'bold'),
            text_color=get_color_modern('text_primary'),
            anchor='w'
        )
        title.pack(pady=(20, 15), padx=20, anchor='w')

        # Obtener datos de progreso
        if self.cursor:
            try:
                self.cursor.execute("""
                    SELECT
                        EstatusModuloUsuario,
                        COUNT(*) as Total
                    FROM Instituto_ProgresoModulo
                    GROUP BY EstatusModuloUsuario
                """)
                data = self.cursor.fetchall()
                statuses = [row[0] for row in data]
                counts = [row[1] for row in data]
            except:
                statuses = ['Completado', 'En Progreso', 'Registrado']
                counts = [450, 320, 155]
        else:
            statuses = ['Completado', 'En Progreso', 'Registrado']
            counts = [450, 320, 155]

        # Calcular porcentajes
        total = sum(counts) if counts else 1
        percentages = [(c / total) * 100 for c in counts]

        # Container para el gráfico
        canvas_container = ctk.CTkFrame(chart_frame, fg_color='transparent')
        canvas_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Simular donut con barras de progreso circulares (versión simplificada)
        colors = [
            get_color_modern('accent_green'),
            get_color_modern('Sky Blue'),
            get_color_modern('accent_orange')
        ]

        # Leyenda con percentajes
        legend_frame = ctk.CTkFrame(canvas_container, fg_color='transparent')
        legend_frame.pack(expand=True)

        for idx, (status, percentage, count) in enumerate(zip(statuses, percentages, counts)):
            item_frame = ctk.CTkFrame(legend_frame, fg_color='transparent')
            item_frame.pack(pady=10, anchor='w')

            # Color indicator
            color_box = ctk.CTkFrame(
                item_frame,
                fg_color=colors[idx % len(colors)],
                width=20,
                height=20,
                corner_radius=4
            )
            color_box.pack(side='left', padx=(20, 10))
            color_box.pack_propagate(False)

            # Label con status
            status_label = ctk.CTkLabel(
                item_frame,
                text=status,
                font=('Arial', 11),
                text_color=get_color_modern('text_primary'),
                width=120,
                anchor='w'
            )
            status_label.pack(side='left', padx=(0, 10))

            # Porcentaje
            percent_label = ctk.CTkLabel(
                item_frame,
                text=f'{percentage:.1f}%',
                font=('Montserrat', 13, 'bold'),
                text_color=colors[idx % len(colors)],
                width=80,
                anchor='e'
            )
            percent_label.pack(side='left', padx=(0, 10))

            # Count
            count_label = ctk.CTkLabel(
                item_frame,
                text=f'({count})',
                font=('Arial', 10),
                text_color=get_color_modern('text_secondary')
            )
            count_label.pack(side='left')

        return chart_frame

    def _create_placeholder(self, tab_name, text):
        tab = self.tabview.tab(tab_name)
        placeholder = ctk.CTkFrame(tab, fg_color=get_color_modern('surface'), border_width=1,
                                  border_color=get_color_modern('border'), corner_radius=10, height=400)
        placeholder.pack(fill='both', expand=True, pady=20, padx=10)
        
        label = ctk.CTkLabel(placeholder, text=f'{text}\n(Implementación en desarrollo)',
                            font=get_font_modern('heading', 16), text_color=get_color_modern('text_secondary'))
        label.place(relx=0.5, rely=0.5, anchor='center')
