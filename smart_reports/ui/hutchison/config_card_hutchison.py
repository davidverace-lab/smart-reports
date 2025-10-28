"""
ConfigCard Hutchison - CORRECCIÓN CRÍTICA
Tarjeta de configuración con botón VISIBLE dentro de la card
"""

import customtkinter as ctk
from smart_reports.config.settings_hutchison import (
    get_color,
    get_font,
    get_button_config
)


class ConfigCardHutchison(ctk.CTkFrame):
    """
    Tarjeta de configuración con diseño corporativo

    CORRECCIÓN CRÍTICA: Botón debe estar DENTRO del frame con grid()
    """

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
            fg_color=get_color('White'),
            corner_radius=15,
            border_width=1,
            border_color=get_color('Border'),
            **kwargs
        )

        self.command = command
        self.button_color = button_color or get_color('Sky Blue')

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
            font=get_font('heading', 18, 'bold'),
            text_color=get_color('Sea Blue')
        )
        title_label.grid(row=1, column=0, pady=(0, 10), sticky='n')

        # === DESCRIPCIÓN ===
        desc_label = ctk.CTkLabel(
            self,
            text=description,
            font=get_font('body', 12),
            text_color=get_color('Medium Gray'),
            wraplength=250,
            justify='center'
        )
        desc_label.grid(row=2, column=0, pady=(0, 20), padx=20, sticky='n')

        # === BOTÓN - ESTO ES CRÍTICO ===
        # Debe estar en row=3 para que aparezca DENTRO de la card
        action_button = ctk.CTkButton(
            self,
            text=button_text,
            font=get_font('heading_medium', 14, 'bold'),
            fg_color=self.button_color,
            hover_color=get_color('Sea Blue'),
            text_color=get_color('White'),
            width=200,
            height=40,
            corner_radius=10,
            command=self._on_click
        )
        action_button.grid(row=3, column=0, pady=(0, 30), sticky='n')

        # Efecto hover en borde
        self.bind('<Enter>', lambda e: self.configure(border_color=self.button_color))
        self.bind('<Leave>', lambda e: self.configure(border_color=get_color('Border')))

    def _on_click(self):
        """Ejecutar comando al hacer clic"""
        if self.command:
            self.command()


# Para testing
if __name__ == '__main__':
    root = ctk.CTk()
    root.title("Test ConfigCard")
    root.geometry("800x600")

    ctk.set_appearance_mode("light")

    # Frame de prueba
    test_frame = ctk.CTkFrame(root, fg_color='#F5F5F5')
    test_frame.pack(fill='both', expand=True, padx=20, pady=20)

    test_frame.grid_columnconfigure((0, 1), weight=1)

    # Card 1
    card1 = ConfigCardHutchison(
        test_frame,
        icon='👥',
        title='Gestionar Usuarios',
        description='Agregar, editar o eliminar usuarios del sistema',
        button_text='Gestionar',
        button_color='#009BDE',
        command=lambda: print('Card 1 clicked')
    )
    card1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    # Card 2
    card2 = ConfigCardHutchison(
        test_frame,
        icon='💾',
        title='Respaldar BD',
        description='Crear copia de seguridad de todos los datos',
        button_text='Respaldar',
        button_color='#28A745',
        command=lambda: print('Card 2 clicked')
    )
    card2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    root.mainloop()
