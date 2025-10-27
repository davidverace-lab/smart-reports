"""
ConfigCard con diseño corporativo Hutchison Ports
Tarjeta de configuración con borde angulado y colores corporativos
"""

import customtkinter as ctk
from smart_reports.config.hutchison_identity import (
    get_hutchison_theme,
    get_font,
    darken_color
)
from smart_reports.ui.components.hutchison_widgets import (
    HutchisonButton,
    HutchisonLabel
)


class HutchisonConfigCard(ctk.CTkFrame):
    """
    Tarjeta de configuración con diseño Hutchison Ports
    """

    def __init__(self, parent, icon, title, description, button_text,
                 button_color=None, command=None, **kwargs):
        """
        Args:
            parent: Widget padre
            icon: Emoji o icono a mostrar
            title: Título de la opción
            description: Descripción de la funcionalidad
            button_text: Texto del botón
            button_color: Color del botón (por defecto Ports Sky Blue)
            command: Función a ejecutar al hacer clic
        """
        self.theme = get_hutchison_theme()
        self.command = command
        self.button_color = button_color or self.theme['primary']

        super().__init__(
            parent,
            fg_color=self.theme['surface'],
            corner_radius=0,
            border_width=2,
            border_color=self.theme['border'],
            **kwargs
        )

        # Container principal con padding
        main_container = ctk.CTkFrame(self, fg_color='transparent')
        main_container.pack(fill='both', expand=True, padx=30, pady=30)

        # Icono con color corporativo
        icon_label = ctk.CTkLabel(
            main_container,
            text=icon,
            font=get_font('heading', 52, 'regular'),
            text_color=self.button_color,
            anchor='center'
        )
        icon_label.pack(pady=(0, 15))

        # Título (Montserrat Bold)
        title_label = HutchisonLabel(
            main_container,
            text=title,
            label_type='heading'
        )
        title_label.configure(
            font=get_font('heading', 18, 'bold'),
            text_color=self.theme['text'],
            anchor='center',
            justify='center'
        )
        title_label.pack(pady=(0, 12))

        # Descripción (Arial Regular)
        if description:
            desc_label = HutchisonLabel(
                main_container,
                text=description,
                label_type='body'
            )
            desc_label.configure(
                font=get_font('body', 12, 'regular'),
                text_color=self.theme['text_secondary'],
                anchor='center',
                justify='center',
                wraplength=280
            )
            desc_label.pack(pady=(0, 25))

        # Spacer para empujar el botón al fondo
        spacer = ctk.CTkFrame(main_container, fg_color='transparent')
        spacer.pack(fill='both', expand=True)

        # Botón de acción (corporativo)
        self.action_btn = ctk.CTkButton(
            main_container,
            text=button_text,
            font=get_font('body', 14, 'bold'),
            fg_color=self.button_color,
            hover_color=darken_color(self.button_color, 0.15),
            text_color=self.theme['text_on_primary'],
            corner_radius=5,
            height=50,
            border_width=0,
            command=self._on_button_click,
            cursor='hand2'
        )
        self.action_btn.pack(fill='x', pady=(10, 0))

        # Efecto hover en el borde de la tarjeta
        self.bind('<Enter>', lambda e: self.configure(border_color=self.button_color))
        self.bind('<Leave>', lambda e: self.configure(border_color=self.theme['border']))

    def _on_button_click(self):
        """Ejecutar comando del botón"""
        if self.command:
            self.command()


__all__ = ['HutchisonConfigCard']
