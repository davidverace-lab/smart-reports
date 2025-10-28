"""
Login Hutchison - Diseño Corporativo Claro
Pantalla de acceso con identidad visual Hutchison Ports
"""

import customtkinter as ctk
from tkinter import messagebox
from smart_reports.config.settings_hutchison import (
    PRIMARY_COLORS,
    FONTS_HUTCHISON,
    get_color,
    get_font,
    get_button_config
)


class LoginHutchison(ctk.CTkFrame):
    """
    Pantalla de login con diseño corporativo Hutchison Ports

    Características:
    - Diseño limpio y claro
    - Colores corporativos Sky Blue y Sea Blue
    - Tipografía Montserrat + Arial
    - Login de demostración: admin / 1234
    """

    def __init__(self, parent, on_login_success):
        """
        Args:
            parent: Widget padre
            on_login_success: Callback function(username) cuando login es exitoso
        """
        super().__init__(parent, fg_color=get_color('White'))

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
            fg_color=get_color('White')
        )
        center_frame.grid(row=0, column=0)

        # Card de login
        login_card = ctk.CTkFrame(
            center_frame,
            fg_color=get_color('White'),
            border_width=1,
            border_color=get_color('Border'),
            corner_radius=15,
            width=500,
            height=600
        )
        login_card.pack(padx=40, pady=40)
        login_card.pack_propagate(False)

        # === LOGO PLACEHOLDER ===
        logo_label = ctk.CTkLabel(
            login_card,
            text='🏢',  # Placeholder - reemplazar con imagen real
            font=('Segoe UI', 72),
            text_color=get_color('Sky Blue')
        )
        logo_label.pack(pady=(40, 10))

        # Texto del logo
        logo_text = ctk.CTkLabel(
            login_card,
            text='HUTCHISON PORTS',
            font=get_font('heading', 18, 'bold'),
            text_color=get_color('Sea Blue')
        )
        logo_text.pack(pady=(0, 30))

        # === TÍTULO ===
        title_label = ctk.CTkLabel(
            login_card,
            text='Acceso al Sistema',
            font=get_font('title', 28, 'bold'),
            text_color=get_color('Sea Blue')
        )
        title_label.pack(pady=(0, 40))

        # === CAMPO USUARIO ===
        user_label = ctk.CTkLabel(
            login_card,
            text='Usuario',
            font=get_font('heading_medium', 14),
            text_color=get_color('Sea Blue'),
            anchor='w'
        )
        user_label.pack(pady=(0, 5), padx=80, fill='x')

        self.user_entry = ctk.CTkEntry(
            login_card,
            placeholder_text='Ingrese su usuario',
            font=get_font('body', 12),
            width=300,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=get_color('Border'),
            fg_color=get_color('White'),
            text_color=get_color('Dark Gray')
        )
        self.user_entry.pack(pady=(0, 20), padx=80)

        # === CAMPO CONTRASEÑA ===
        pass_label = ctk.CTkLabel(
            login_card,
            text='Contraseña',
            font=get_font('heading_medium', 14),
            text_color=get_color('Sea Blue'),
            anchor='w'
        )
        pass_label.pack(pady=(0, 5), padx=80, fill='x')

        self.pass_entry = ctk.CTkEntry(
            login_card,
            placeholder_text='Ingrese su contraseña',
            show='●',
            font=get_font('body', 12),
            width=300,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=get_color('Border'),
            fg_color=get_color('White'),
            text_color=get_color('Dark Gray')
        )
        self.pass_entry.pack(pady=(0, 30), padx=80)

        # Bind Enter key
        self.pass_entry.bind('<Return>', lambda e: self._handle_login())

        # === BOTÓN ACCEDER ===
        btn_config = get_button_config('primary')
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
            font=get_font('small', 10),
            text_color=get_color('Medium Gray')
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
        # TODO: Conectar con base de datos real
        if username.lower() == 'admin' and password == '1234':
            # Login exitoso
            self.pack_forget()  # Ocultar login
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
    root.title("Test Login Hutchison")
    root.geometry("800x700")

    ctk.set_appearance_mode("light")

    login = LoginHutchison(root, test_callback)
    login.pack(fill='both', expand=True)

    root.mainloop()
