"""
Demo del Diseño Corporativo Hutchison Ports
Muestra la aplicación del manual de identidad visual
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import customtkinter as ctk
from smart_reports.config.hutchison_identity import get_hutchison_theme, get_font
from smart_reports.ui.components.hutchison_widgets import (
    AngledHeaderFrame,
    AngledDivider,
    HutchisonButton,
    HutchisonLabel,
    LogoFrame,
    MetricCardAngled
)
from smart_reports.ui.components.hutchison_sidebar import HutchisonSidebar
from smart_reports.ui.components.hutchison_config_card import HutchisonConfigCard


class HutchisonDemo(ctk.CTk):
    """Aplicación de demostración con diseño Hutchison Ports"""

    def __init__(self):
        super().__init__()

        self.theme = get_hutchison_theme()

        # Configurar ventana principal
        self.title("Smart Reports - Hutchison Ports")
        self.geometry("1400x900")
        self.configure(fg_color=self.theme['background'])

        # Crear contenedor principal
        self.main_container = ctk.CTkFrame(
            self,
            fg_color=self.theme['background'],
            corner_radius=0
        )
        self.main_container.pack(fill='both', expand=True)

        # Barra superior con logo
        self._create_top_bar()

        # Contenedor con sidebar y contenido
        content_container = ctk.CTkFrame(
            self.main_container,
            fg_color='transparent'
        )
        content_container.pack(fill='both', expand=True)

        # Sidebar (Sea Blue con texto blanco)
        navigation_callbacks = {
            'dashboard': self.show_dashboard,
            'consultas': self.show_consultas,
            'actualizar': self.show_actualizar,
            'configuracion': self.show_configuracion
        }

        self.sidebar = HutchisonSidebar(content_container, navigation_callbacks)
        self.sidebar.pack(side='left', fill='y')

        # Área de contenido
        self.content_area = ctk.CTkFrame(
            content_container,
            fg_color=self.theme['background'],
            corner_radius=0
        )
        self.content_area.pack(side='left', fill='both', expand=True)

        # Mostrar panel de configuración por defecto
        self.show_configuracion()
        self.sidebar.set_active('configuracion')

    def _create_top_bar(self):
        """Crear barra superior con logo corporativo"""
        top_bar = ctk.CTkFrame(
            self.main_container,
            fg_color=self.theme['surface'],
            height=80,
            corner_radius=0
        )
        top_bar.pack(fill='x', padx=0, pady=0)
        top_bar.pack_propagate(False)

        # Logo en esquina superior izquierda
        logo = LogoFrame(top_bar)
        logo.pack(side='left', padx=20, pady=10)

        # Separador (línea Sky Blue)
        separator = ctk.CTkFrame(
            self.main_container,
            height=3,
            fg_color=self.theme['primary']
        )
        separator.pack(fill='x')

    def clear_content_area(self):
        """Limpiar área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        """Mostrar panel de dashboard"""
        self.clear_content_area()

        # Header angulado
        header = AngledHeaderFrame(
            self.content_area,
            text='Dashboard',
            height=80,
            color=self.theme['primary']
        )
        header.pack(fill='x', padx=20, pady=(20, 0))

        # Scroll frame para contenido
        scroll_frame = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Grid de métricas
        metrics_grid = ctk.CTkFrame(scroll_frame, fg_color='transparent')
        metrics_grid.pack(fill='x', pady=20)

        metrics_grid.grid_columnconfigure((0, 1, 2), weight=1)

        # Tarjetas métricas con diseño angulado
        metric1 = MetricCardAngled(
            metrics_grid,
            title='Total Usuarios',
            value='1,234',
            subtitle='Usuarios activos en el sistema',
            color=self.theme['primary']
        )
        metric1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        metric2 = MetricCardAngled(
            metrics_grid,
            title='Módulos Completados',
            value='856',
            subtitle='Módulos finalizados este mes',
            color=self.theme['secondary']
        )
        metric2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        metric3 = MetricCardAngled(
            metrics_grid,
            title='Progreso Global',
            value='78%',
            subtitle='Completado del total',
            color=self.theme['accent_orange']
        )
        metric3.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # Divisor angulado
        divider = AngledDivider(
            scroll_frame,
            height=4,
            color=self.theme['secondary']
        )
        divider.pack(fill='x', pady=30)

        # Información adicional
        info_label = HutchisonLabel(
            scroll_frame,
            text='Este es el panel de dashboard con el nuevo diseño corporativo de Hutchison Ports.\nTodos los elementos utilizan los colores, tipografías y formas anguladas del manual de identidad.',
            label_type='body'
        )
        info_label.configure(justify='left')
        info_label.pack(fill='x', pady=20)

    def show_consultas(self):
        """Mostrar panel de consultas"""
        self.clear_content_area()

        header = AngledHeaderFrame(
            self.content_area,
            text='Consultas de Usuarios',
            height=80,
            color=self.theme['secondary']
        )
        header.pack(fill='x', padx=20, pady=(20, 20))

        info_label = HutchisonLabel(
            self.content_area,
            text='Panel de Consultas\n(En desarrollo con diseño Hutchison Ports)',
            label_type='heading'
        )
        info_label.pack(pady=100)

    def show_actualizar(self):
        """Mostrar panel de actualización"""
        self.clear_content_area()

        header = AngledHeaderFrame(
            self.content_area,
            text='Actualizar Datos',
            height=80,
            color=self.theme['accent_orange']
        )
        header.pack(fill='x', padx=20, pady=(20, 20))

        info_label = HutchisonLabel(
            self.content_area,
            text='Panel de Actualización\n(En desarrollo con diseño Hutchison Ports)',
            label_type='heading'
        )
        info_label.pack(pady=100)

    def show_configuracion(self):
        """Mostrar panel de configuración"""
        self.clear_content_area()

        # Header angulado
        header = AngledHeaderFrame(
            self.content_area,
            text='Configuración',
            height=80,
            color=self.theme['primary']
        )
        header.pack(fill='x', padx=20, pady=(20, 0))

        # Frame para contenido
        content_frame = ctk.CTkFrame(
            self.content_area,
            fg_color='transparent'
        )
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Divisor angulado
        divider = AngledDivider(
            content_frame,
            height=4,
            color=self.theme['secondary']
        )
        divider.pack(fill='x', pady=(0, 30))

        # Grid 2x2 para las tarjetas
        grid_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
        grid_frame.pack(fill='both', expand=True)

        grid_frame.grid_columnconfigure((0, 1), weight=1)
        grid_frame.grid_rowconfigure((0, 1), weight=1)

        # Card 1: Gestionar Usuarios (Ports Sky Blue)
        card1 = HutchisonConfigCard(
            grid_frame,
            icon='👥',
            title='Gestionar Usuarios',
            description='Agregar nuevos usuarios o editar información de usuarios existentes',
            button_text='Gestionar',
            button_color=self.theme['primary'],
            command=lambda: print("Gestionar Usuarios clickeado")
        )
        card1.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')

        # Card 2: Respaldar BD (Ports Aqua Green)
        card2 = HutchisonConfigCard(
            grid_frame,
            icon='💾',
            title='Respaldar Base de Datos',
            description='Crear un respaldo de seguridad de la base de datos actual',
            button_text='Respaldar',
            button_color=self.theme['secondary'],
            command=lambda: print("Respaldar BD clickeado")
        )
        card2.grid(row=0, column=1, padx=15, pady=15, sticky='nsew')

        # Card 3: Acerca de (Ports Sunray Yellow)
        card3 = HutchisonConfigCard(
            grid_frame,
            icon='ℹ️',
            title='Acerca de',
            description='Información sobre Smart Reports y versión del software',
            button_text='Ver Info',
            button_color=self.theme['accent_yellow'],
            command=lambda: print("Acerca de clickeado")
        )
        card3.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')

        # Card 4: Configuración BD (Ports Sunset Orange)
        card4 = HutchisonConfigCard(
            grid_frame,
            icon='🔧',
            title='Configuración BD',
            description='Cambiar configuración de base de datos',
            button_text='Cambiar',
            button_color=self.theme['accent_orange'],
            command=lambda: print("Configuración BD clickeado")
        )
        card4.grid(row=1, column=1, padx=15, pady=15, sticky='nsew')


def main():
    """Ejecutar demo"""
    print("\n" + "="*80)
    print("DEMO - DISEÑO CORPORATIVO HUTCHISON PORTS")
    print("="*80)
    print("\nCaracterísticas del diseño:")
    print("✓ Paleta de colores corporativa (Sky Blue, Aqua Green, etc.)")
    print("✓ Tipografía Montserrat (títulos) y Arial (texto)")
    print("✓ Formas anguladas con Dynamic Angle de 30.3°")
    print("✓ Sidebar Sea Blue (#002E6D) con texto blanco")
    print("✓ Logo corporativo en esquina superior izquierda")
    print("✓ Alineación de texto a la izquierda")
    print("\nNavega por los diferentes paneles para ver el diseño aplicado.")
    print("="*80 + "\n")

    app = HutchisonDemo()
    app.mainloop()


if __name__ == '__main__':
    main()
