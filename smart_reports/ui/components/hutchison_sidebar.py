"""
Sidebar Corporativo Hutchison Ports
Sidebar con identidad visual de Hutchison Ports (Sea Blue con texto blanco)
"""

import customtkinter as ctk
from smart_reports.config.hutchison_identity import (
    HUTCHISON_COLORS,
    get_hutchison_theme,
    get_font
)
from smart_reports.ui.components.hutchison_widgets import HutchisonLabel


class HutchisonSidebar(ctk.CTkFrame):
    """
    Sidebar corporativo con colores y tipografía de Hutchison Ports
    Fondo: Ports Sea Blue (#002E6D)
    Texto: Blanco
    """

    def __init__(self, parent, navigation_callbacks, **kwargs):
        """
        Args:
            parent: Widget padre
            navigation_callbacks: Dict con {nombre: callback_function}
        """
        self.theme = get_hutchison_theme()
        self.navigation_callbacks = navigation_callbacks
        self.nav_buttons = []
        self.active_button = None

        # Sidebar con fondo Sea Blue
        super().__init__(
            parent,
            width=240,
            fg_color=self.theme['sidebar_bg'],
            corner_radius=0,
            **kwargs
        )

        # Logo/Header
        self._create_header()

        # Navegación
        self._create_navigation()

        # Footer con versión
        self._create_footer()

    def _create_header(self):
        """Crear header con logo corporativo"""
        logo_frame = ctk.CTkFrame(
            self,
            fg_color='transparent',
            height=120
        )
        logo_frame.pack(fill='x', padx=20, pady=(25, 20))
        logo_frame.pack_propagate(False)

        # Logo "HUTCHISON PORTS" (usando Montserrat Bold)
        logo_label = ctk.CTkLabel(
            logo_frame,
            text='HUTCHISON\nPORTS',
            font=get_font('heading', 20, 'bold'),
            text_color=self.theme['sidebar_text'],
            justify='left',
            anchor='w'
        )
        logo_label.pack(anchor='w', pady=(5, 8))

        # Subtítulo "Smart Reports"
        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text='Smart Reports',
            font=get_font('body', 12, 'normal'),
            text_color=self.theme['sidebar_text_secondary'],
            justify='left',
            anchor='w'
        )
        subtitle_label.pack(anchor='w')

        # Línea separadora (Sky Blue clara)
        separator = ctk.CTkFrame(
            self,
            height=2,
            fg_color=self.theme['primary']
        )
        separator.pack(fill='x', padx=20, pady=(0, 20))

    def _create_navigation(self):
        """Crear botones de navegación"""
        nav_items = [
            ('📊', 'Dashboard', 'dashboard'),
            ('🔍', 'Consultas', 'consultas'),
            ('📤', 'Actualizar Datos', 'actualizar'),
            ('⚙️', 'Configuración', 'configuracion'),
        ]

        for icon, text, key in nav_items:
            if key in self.navigation_callbacks:
                btn = ctk.CTkButton(
                    self,
                    text=f'{icon}  {text}',
                    font=get_font('body', 14, 'normal'),
                    fg_color='transparent',
                    text_color=self.theme['sidebar_text_secondary'],
                    hover_color=self.theme['sidebar_hover'],
                    anchor='w',
                    height=55,
                    corner_radius=8,
                    command=lambda k=key: self._on_nav_click(k)
                )
                btn.pack(fill='x', padx=12, pady=4)
                self.nav_buttons.append((key, btn))

    def _create_footer(self):
        """Crear footer con información de versión"""
        # Spacer para empujar footer al fondo
        spacer = ctk.CTkFrame(self, fg_color='transparent')
        spacer.pack(fill='both', expand=True)

        # Línea separadora superior
        separator_top = ctk.CTkFrame(
            self,
            height=2,
            fg_color=self.theme['primary']
        )
        separator_top.pack(fill='x', padx=20, pady=(10, 15))

        # Footer
        footer = ctk.CTkFrame(
            self,
            fg_color='transparent',
            height=70
        )
        footer.pack(side='bottom', fill='x', padx=20, pady=(0, 20))
        footer.pack_propagate(False)

        # Versión
        version_label = ctk.CTkLabel(
            footer,
            text='Versión 2.0',
            font=get_font('body', 10, 'bold'),
            text_color=self.theme['sidebar_text']
        )
        version_label.pack(anchor='w', pady=(5, 2))

        # Copyright
        copyright_label = ctk.CTkLabel(
            footer,
            text='© 2025 Hutchison Ports',
            font=get_font('body', 9, 'normal'),
            text_color=self.theme['sidebar_text_secondary']
        )
        copyright_label.pack(anchor='w')

        # Marca
        brand_label = ctk.CTkLabel(
            footer,
            text='Instituto HP',
            font=get_font('body', 9, 'normal'),
            text_color=self.theme['sidebar_text_secondary']
        )
        brand_label.pack(anchor='w')

    def _on_nav_click(self, key):
        """Manejar click en navegación"""
        # Actualizar estilos de botones
        for btn_key, btn in self.nav_buttons:
            if btn_key == key:
                # Botón activo: fondo más claro y texto blanco
                btn.configure(
                    fg_color=self.theme['sidebar_hover'],
                    text_color=self.theme['sidebar_text']
                )
                self.active_button = btn
            else:
                # Botón inactivo: transparente con texto gris claro
                btn.configure(
                    fg_color='transparent',
                    text_color=self.theme['sidebar_text_secondary']
                )

        # Ejecutar callback
        if key in self.navigation_callbacks:
            self.navigation_callbacks[key]()

    def set_active(self, key):
        """Establecer botón activo programáticamente"""
        self._on_nav_click(key)


__all__ = ['HutchisonSidebar']
