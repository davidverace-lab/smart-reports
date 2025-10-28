"""
SMART REPORTS - HUTCHISON PORTS
Pantalla de Login con diseño corporativo
Versión 2.0
"""
import customtkinter as ctk
from smart_reports.config.hutchison_identity import get_hutchison_theme, get_font, HUTCHISON_COLORS


class LoginWindow(ctk.CTkFrame):
    """Pantalla de Login - Diseño Corporativo Hutchison Ports"""

    def __init__(self, parent, on_login_success):
        """
        Args:
            parent: Ventana padre
            on_login_success: Callback que recibe el nombre de usuario al hacer login exitoso
        """
        super().__init__(parent, fg_color=HUTCHISON_COLORS['white'], corner_radius=0)

        self.parent = parent
        self.on_login_success = on_login_success
        self.theme = get_hutchison_theme()

        self._create_login_interface()

    def _create_login_interface(self):
        """Crear interfaz de login"""
        # Container principal centrado
        main_container = ctk.CTkFrame(
            self,
            fg_color='transparent'
        )
        main_container.place(relx=0.5, rely=0.5, anchor='center')

        # Logo/Marca superior
        logo_frame = ctk.CTkFrame(
            main_container,
            fg_color=HUTCHISON_COLORS['ports_sea_blue'],
            corner_radius=15,
            width=500,
            height=120
        )
        logo_frame.pack(pady=(0, 40))
        logo_frame.pack_propagate(False)

        # Título con tipografía corporativa
        title_label = ctk.CTkLabel(
            logo_frame,
            text='Instituto Hutchison Ports',
            font=get_font('heading', 32, 'bold'),
            text_color=HUTCHISON_COLORS['white']
        )
        title_label.place(relx=0.5, rely=0.5, anchor='center')

        # Card de login
        login_card = ctk.CTkFrame(
            main_container,
            fg_color=HUTCHISON_COLORS['white'],
            corner_radius=15,
            border_width=2,
            border_color=HUTCHISON_COLORS['ports_sky_blue'],
            width=500,
            height=350
        )
        login_card.pack()
        login_card.pack_propagate(False)

        # Contenido del card con padding
        content_frame = ctk.CTkFrame(login_card, fg_color='transparent')
        content_frame.pack(fill='both', expand=True, padx=50, pady=40)

        # Título del formulario
        form_title = ctk.CTkLabel(
            content_frame,
            text='Acceso al Sistema',
            font=get_font('heading', 24, 'bold'),
            text_color=HUTCHISON_COLORS['ports_sea_blue']
        )
        form_title.pack(pady=(0, 30))

        # Campo Usuario
        user_label = ctk.CTkLabel(
            content_frame,
            text='Usuario',
            font=get_font('body', 14, 'bold'),
            text_color=HUTCHISON_COLORS['ports_sea_blue'],
            anchor='w'
        )
        user_label.pack(fill='x', pady=(0, 5))

        self.user_entry = ctk.CTkEntry(
            content_frame,
            height=45,
            font=get_font('body', 14),
            fg_color=HUTCHISON_COLORS['white'],
            border_color=HUTCHISON_COLORS['ports_sky_blue'],
            border_width=2,
            corner_radius=8
        )
        self.user_entry.pack(fill='x', pady=(0, 20))
        self.user_entry.insert(0, 'admin')  # Usuario por defecto

        # Campo Contraseña
        pass_label = ctk.CTkLabel(
            content_frame,
            text='Contraseña',
            font=get_font('body', 14, 'bold'),
            text_color=HUTCHISON_COLORS['ports_sea_blue'],
            anchor='w'
        )
        pass_label.pack(fill='x', pady=(0, 5))

        self.pass_entry = ctk.CTkEntry(
            content_frame,
            height=45,
            font=get_font('body', 14),
            fg_color=HUTCHISON_COLORS['white'],
            border_color=HUTCHISON_COLORS['ports_sky_blue'],
            border_width=2,
            corner_radius=8,
            show='●'  # Ocultar contraseña
        )
        self.pass_entry.pack(fill='x', pady=(0, 30))

        # Botón Acceder
        login_button = ctk.CTkButton(
            content_frame,
            text='Acceder al Sistema',
            height=50,
            font=get_font('body', 16, 'bold'),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            hover_color=HUTCHISON_COLORS['ports_sea_blue'],
            text_color=HUTCHISON_COLORS['white'],
            corner_radius=8,
            command=self._handle_login,
            cursor='hand2'
        )
        login_button.pack(fill='x')

        # Bind Enter key para login
        self.user_entry.bind('<Return>', lambda e: self._handle_login())
        self.pass_entry.bind('<Return>', lambda e: self._handle_login())

        # Pie de página con información
        footer_label = ctk.CTkLabel(
            main_container,
            text='Smart Reports v2.0 - Sistema de Gestión de Capacitaciones',
            font=get_font('caption', 10),
            text_color='gray'
        )
        footer_label.pack(pady=(30, 0))

    def _handle_login(self):
        """Manejar intento de login"""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        # Validaciones simples
        if not username:
            self._show_error('Por favor ingrese un usuario')
            return

        if not password:
            self._show_error('Por favor ingrese una contraseña')
            return

        # Por ahora, cualquier combinación es válida (login demo)
        # En producción, aquí iría la validación contra BD

        # Ocultar pantalla de login
        self.pack_forget()

        # Llamar callback con el nombre de usuario
        # Formatear nombre para mostrar
        display_name = username.title()  # Capitalizar primera letra
        self.on_login_success(display_name)

    def _show_error(self, message):
        """Mostrar mensaje de error en el card"""
        # Crear label temporal de error
        error_label = ctk.CTkLabel(
            self,
            text=message,
            font=get_font('body', 12),
            text_color='red'
        )
        error_label.place(relx=0.5, rely=0.85, anchor='center')

        # Eliminar después de 3 segundos
        self.after(3000, error_label.destroy)
