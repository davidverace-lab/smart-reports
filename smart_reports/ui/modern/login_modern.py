"""
Login Modern - Diseño Oscuro con Tipografía Corporativa
Pantalla de acceso con diseño oscuro legacy pero tipografía Hutchison
"""

import customtkinter as ctk
from tkinter import messagebox
from smart_reports.config.settings_modern import (
    PRIMARY_COLORS_MODERN,
    FONTS_MODERN,
    get_color_modern,
    get_font_modern,
    get_button_config_modern
)


class LoginModern(ctk.CTkFrame):
    """
    Pantalla de login con diseño oscuro

    Características:
    - Diseño oscuro elegante
    - Tipografía corporativa Hutchison (Montserrat + Arial)
    - Botones con colores corporativos (Sky Blue)
    - Login de demostración: admin / 1234
    """

    def __init__(self, parent, on_login_success):
        """
        Args:
            parent: Widget padre
            on_login_success: Callback function(username) cuando login es exitoso
        """
        super().__init__(parent, fg_color=get_color_modern('background'))

        self.on_login_success = on_login_success

        # Configurar grid del frame principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_login_interface()

    def _create_login_interface(self):
        """Crear interfaz de login centrada"""

        # Container central
        center_frame = ctk.CTkFrame(
            self,
            fg_color=get_color_modern('background')
        )
        center_frame.grid(row=0, column=0)

        # Card de login (oscuro)
        login_card = ctk.CTkFrame(
            center_frame,
            fg_color=get_color_modern('surface'),
            border_width=1,
            border_color=get_color_modern('border'),
            corner_radius=15,
            width=500,
            height=600
        )
        login_card.pack(padx=40, pady=40)
        login_card.pack_propagate(False)

        # === LOGO PLACEHOLDER ===
        logo_label = ctk.CTkLabel(
            login_card,
            text='🏢',
            font=('Segoe UI', 72),
            text_color=get_color_modern('accent_primary')  # Sky Blue
        )
        logo_label.pack(pady=(40, 10))

        # Texto del logo
        logo_text = ctk.CTkLabel(
            login_card,
            text='HUTCHISON PORTS',
            font=get_font_modern('heading', 18, 'bold'),
            text_color=get_color_modern('text_primary')
        )
        logo_text.pack(pady=(0, 30))

        # === TÍTULO ===
        title_label = ctk.CTkLabel(
            login_card,
            text='Acceso al Sistema',
            font=get_font_modern('title', 28, 'bold'),
            text_color=get_color_modern('text_primary')
        )
        title_label.pack(pady=(0, 40))

        # === CAMPO USUARIO ===
        user_label = ctk.CTkLabel(
            login_card,
            text='Usuario',
            font=get_font_modern('heading_medium', 14),
            text_color=get_color_modern('text_primary'),
            anchor='w'
        )
        user_label.pack(pady=(0, 5), padx=80, fill='x')

        self.user_entry = ctk.CTkEntry(
            login_card,
            placeholder_text='Ingrese su usuario',
            font=get_font_modern('body', 12),
            width=300,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=get_color_modern('border'),
            fg_color=get_color_modern('surface_light'),
            text_color=get_color_modern('text_primary')
        )
        self.user_entry.pack(pady=(0, 20), padx=80)

        # === CAMPO CONTRASEÑA ===
        pass_label = ctk.CTkLabel(
            login_card,
            text='Contraseña',
            font=get_font_modern('heading_medium', 14),
            text_color=get_color_modern('text_primary'),
            anchor='w'
        )
        pass_label.pack(pady=(0, 5), padx=80, fill='x')

        self.pass_entry = ctk.CTkEntry(
            login_card,
            placeholder_text='Ingrese su contraseña',
            show='●',
            font=get_font_modern('body', 12),
            width=300,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=get_color_modern('border'),
            fg_color=get_color_modern('surface_light'),
            text_color=get_color_modern('text_primary')
        )
        self.pass_entry.pack(pady=(0, 30), padx=80)

        # Bind Enter key
        self.pass_entry.bind('<Return>', lambda e: self._handle_login())

        # === BOTÓN ACCEDER (Sky Blue corporativo) ===
        btn_config = get_button_config_modern('primary')
        login_button = ctk.CTkButton(
            login_card,
            text='Acceder',
            **btn_config,
            width=200,
            height=45,
            command=self._handle_login
        )
        login_button.pack(pady=(0, 20))

        # === TEXTO INFORMATIVO ===
        info_label = ctk.CTkLabel(
            login_card,
            text='Demo: Usuario: admin | Contraseña: 1234',
            font=get_font_modern('small', 10),
            text_color=get_color_modern('text_secondary')
        )
        info_label.pack(pady=(20, 0))

    def _handle_login(self):
        """Manejar el evento de login"""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        # Validaciones básicas
        if not username:
            messagebox.showerror(
                "Error de Validación",
                "Por favor ingrese su usuario"
            )
            return

        if not password:
            messagebox.showerror(
                "Error de Validación",
                "Por favor ingrese su contraseña"
            )
            return

        # Validación hardcoded para demo
        if username.lower() == 'admin' and password == '1234':
            # Login exitoso
            self.pack_forget()
            self.on_login_success(username.title())
        else:
            messagebox.showerror(
                "Error de Acceso",
                "Usuario o contraseña incorrectos.\n\n"
                "Demo: usuario=admin, contraseña=1234"
            )
            self.pass_entry.delete(0, 'end')


# Para testing standalone
if __name__ == '__main__':
    def test_callback(user):
        print(f"Login exitoso: {user}")

    root = ctk.CTk()
    root.title("Test Login Modern")
    root.geometry("800x700")

    ctk.set_appearance_mode("dark")

    login = LoginModern(root, test_callback)
    login.pack(fill='both', expand=True)

    root.mainloop()
