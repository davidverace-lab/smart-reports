"""
Panel de Resumen Ejecutivo TNG
Terminal de Nuevas Generaciones - Métricas y Comparación de Periodos
"""
import customtkinter as ctk
from smart_reports.config.identity import get_hutchison_theme, get_font
from smart_reports.ui.components.widgets import (
    AngledCard,
    AngledDivider,
    HutchisonLabel
)
from smart_reports.ui.dialogs.department_quick_view import DepartmentQuickView


class TNGSummaryPanel:
    """Panel de Resumen Ejecutivo TNG con comparador de periodos"""

    def __init__(self, parent, theme, root):
        """
        Args:
            parent: Widget padre (tab del dashboard)
            theme: Tema corporativo Hutchison
            root: Ventana raíz (para diálogos modales)
        """
        self.parent = parent
        self.theme = theme
        self.root = root
        self.comparison_mode = 'Actual'
        self.tng_metrics_grid = None
        self.tng_comparison_selector = None

    def show(self):
        """Mostrar panel de resumen TNG"""
        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            self.parent,
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
        label = HutchisonLabel(
            selector_frame,
            text='Comparar métricas actuales con:',
            label_type='body'
        )
        label.configure(font=get_font('body', 14, 'bold'))
        label.pack(side='left', padx=(10, 15))

        # Segmented Button para comparación
        self.tng_comparison_selector = ctk.CTkSegmentedButton(
            selector_frame,
            values=['Actual', 'vs Semana Ant.', 'vs Mes Ant.', 'vs Trim. Ant.'],
            font=get_font('body', 13),
            fg_color=self.theme['surface'],
            selected_color=self.theme['primary'],
            selected_hover_color=self.theme['secondary'],
            unselected_color=self.theme['border'],
            command=self._on_comparison_change
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
        self._create_metrics()

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
            # Determinar color del borde según status
            if status_color == 'green':
                border_color = self.theme['accent_green']
            elif status_color == 'orange':
                border_color = self.theme['accent_orange']
            else:
                border_color = self.theme['secondary']

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
                border_color=border_color,
                command=lambda name=dept_name, comp=completion: self._show_department_quick_view(name, comp),
                cursor='hand2'
            )
            dept_btn.pack(fill='x', padx=20, pady=5)

    def _create_metrics(self):
        """Crear métricas TNG con datos de ejemplo según modo de comparación"""
        # Limpiar métricas existentes
        for widget in self.tng_metrics_grid.winfo_children():
            widget.destroy()

        # Datos de ejemplo según modo de comparación
        if self.comparison_mode == 'Actual':
            metrics_data = [
                ('Empleados TNG', '245', None, self.theme['primary']),
                ('Tasa Finalización', '78.5%', None, self.theme['secondary']),
                ('Módulos Activos', '18', None, self.theme['accent_yellow']),
                ('Críticos Completados', '92%', None, self.theme['accent_green']),
            ]
        elif self.comparison_mode == 'vs Semana Ant.':
            metrics_data = [
                ('Empleados TNG', '245', '+2.1%', self.theme['primary']),
                ('Tasa Finalización', '78.5%', '+3.5%', self.theme['secondary']),
                ('Módulos Activos', '18', '+1', self.theme['accent_yellow']),
                ('Críticos Completados', '92%', '+4.2%', self.theme['accent_green']),
            ]
        elif self.comparison_mode == 'vs Mes Ant.':
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

    def _on_comparison_change(self, value):
        """Manejar cambio en el selector de comparación"""
        self.comparison_mode = value
        # Recrear métricas con nuevos datos de comparación
        self._create_metrics()

    def _show_department_quick_view(self, dept_name, completion_rate):
        """Mostrar Vista Rápida de departamento TNG en ventana emergente"""
        quick_view = DepartmentQuickView(self.root, dept_name, completion_rate)
