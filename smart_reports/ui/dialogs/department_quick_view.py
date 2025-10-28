"""
Vista Rápida de Departamento TNG
Ventana modal con KPIs específicos del departamento
"""
import customtkinter as ctk
from smart_reports.config.identity import get_hutchison_theme, get_font
from smart_reports.ui.components.widgets import (
    AngledHeaderFrame,
    HutchisonLabel
)


class DepartmentQuickView(ctk.CTkToplevel):
    """Ventana emergente con vista rápida de departamento TNG"""

    def __init__(self, parent, dept_name, completion_rate):
        """
        Args:
            parent: Ventana padre
            dept_name: Nombre del departamento
            completion_rate: Tasa de finalización del departamento
        """
        super().__init__(parent)

        self.dept_name = dept_name
        self.completion_rate = completion_rate
        self.theme = get_hutchison_theme()

        # Configurar ventana
        self.title(f'Vista Rápida - {dept_name}')
        self.geometry('500x450')

        # Centrar ventana
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        # Hacer modal
        self.grab_set()
        self.attributes('-topmost', True)

        # Crear interfaz
        self._create_interface()

    def _create_interface(self):
        """Crear interfaz de la ventana"""
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color=self.theme['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header angulado
        header = AngledHeaderFrame(
            main_frame,
            text=f'Vista Rápida: {self.dept_name}',
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
            ('Tasa Finalización', f'{self.completion_rate}%', self.theme['primary']),
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
            title_label = HutchisonLabel(
                kpi_content,
                text=title,
                label_type='body'
            )
            title_label.configure(font=get_font('body', 12), text_color=self.theme['text_secondary'])
            title_label.pack(anchor='w')

            # Valor
            value_label = HutchisonLabel(
                kpi_content,
                text=value,
                label_type='heading'
            )
            value_label.configure(font=get_font('heading', 28, 'bold'), text_color=color)
            value_label.pack(anchor='w', pady=(5, 0))

        # Información adicional
        info_label = HutchisonLabel(
            scroll_frame,
            text=(
                f'Información detallada del departamento {self.dept_name}:\n\n' +
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
            command=self.destroy
        )
        close_btn.pack(fill='x', pady=(10, 0))
