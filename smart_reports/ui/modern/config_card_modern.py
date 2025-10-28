"""
ConfigCard Modern - Diseño Oscuro
Tarjeta de configuración con botón VISIBLE (versión oscura)
"""

import customtkinter as ctk
from smart_reports.config.settings_modern import (
    get_color_modern,
    get_font_modern
)


class ConfigCardModern(ctk.CTkFrame):
    """ConfigCard con diseño oscuro"""

    def __init__(self, parent, icon, title, description, button_text,
                 button_color=None, command=None, **kwargs):
        """
        Args:
            parent: Widget padre
            icon: Emoji/icono
            title: Título
            description: Descripción
            button_text: Texto del botón
            button_color: Color del botón (opcional)
            command: Callback del botón
        """
        super().__init__(
            parent,
            fg_color=get_color_modern('surface'),
            corner_radius=15,
            border_width=1,
            border_color=get_color_modern('border'),
            **kwargs
        )

        self.command = command
        self.button_color = button_color or get_color_modern('accent_primary')

        # Configurar grid interno
        self.grid_columnconfigure(0, weight=1)

        # === ICONO ===
        icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=('Segoe UI', 48),
            text_color=self.button_color
        )
        icon_label.grid(row=0, column=0, pady=(30, 10), sticky='n')

        # === TÍTULO ===
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=get_font_modern('heading', 18, 'bold'),
            text_color=get_color_modern('text_primary')
        )
        title_label.grid(row=1, column=0, pady=(0, 10), sticky='n')

        # === DESCRIPCIÓN ===
        desc_label = ctk.CTkLabel(
            self,
            text=description,
            font=get_font_modern('body', 12),
            text_color=get_color_modern('text_secondary'),
            wraplength=250,
            justify='center'
        )
        desc_label.grid(row=2, column=0, pady=(0, 20), padx=20, sticky='n')

        # === BOTÓN ===
        action_button = ctk.CTkButton(
            self,
            text=button_text,
            font=get_font_modern('heading_medium', 14, 'bold'),
            fg_color=self.button_color,
            hover_color=get_color_modern('accent_secondary'),
            text_color='#ffffff',
            width=200,
            height=40,
            corner_radius=10,
            command=self._on_click
        )
        action_button.grid(row=3, column=0, pady=(0, 30), sticky='n')

        # Efecto hover en borde
        self.bind('<Enter>', lambda e: self.configure(border_color=self.button_color))
        self.bind('<Leave>', lambda e: self.configure(border_color=get_color_modern('border')))

    def _on_click(self):
        """Ejecutar comando al hacer clic"""
        if self.command:
            self.command()
