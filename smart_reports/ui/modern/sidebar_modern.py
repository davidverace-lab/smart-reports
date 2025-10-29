"""
Sidebar Modern - Diseño Oscuro
Barra lateral con navegación, logo y footer corporativo - Versión oscura
"""

import customtkinter as ctk
from tkinter import messagebox


class SidebarModern(ctk.CTkFrame):
    """Sidebar estilo Modern (oscuro) con identidad Hutchison"""

    def __init__(self, parent, switch_panel_callback):
        super().__init__(
            parent,
            width=240,
            fg_color='#1e2139',  # Fondo oscuro
            corner_radius=0
        )

        self.switch_panel = switch_panel_callback
        self.current_panel = None
        self.nav_buttons = {}

        self.pack_propagate(False)

        self.create_header()
        self.create_separator()
        self.create_navigation()
        self.create_separator()
        self.create_special_button()
        self.create_spacer()
        self.create_separator()
        self.create_footer()

    def create_header(self):
        """Crea el header con logo y subtítulo"""
        header_frame = ctk.CTkFrame(self, fg_color='transparent')
        header_frame.pack(fill='x', padx=20, pady=(25, 20))

        # Logo principal
        logo = ctk.CTkLabel(
            header_frame,
            text='HUTCHISON\nPORTS',
            font=('Montserrat', 18, 'bold'),
            text_color='#FFFFFF',
            justify='left',
            anchor='w'
        )
        logo.pack(anchor='w')

        # Subtítulo
        subtitle = ctk.CTkLabel(
            header_frame,
            text='Smart Reports',
            font=('Arial', 11),
            text_color='#a0a3bd',
            anchor='w'
        )
        subtitle.pack(anchor='w', pady=(5, 0))

    def create_separator(self):
        """Crea una línea separadora horizontal"""
        separator = ctk.CTkFrame(
            self,
            height=1,
            fg_color='#2d3049'
        )
        separator.pack(fill='x', padx=15, pady=5)

    def create_navigation(self):
        """Crea los botones de navegación"""
        nav_frame = ctk.CTkFrame(self, fg_color='transparent')
        nav_frame.pack(fill='x', pady=15)

        nav_items = [
            ('dashboard', '📊', 'Dashboard'),
            ('consultas', '🔍', 'Consultas'),
            ('actualizar', '🔄', 'Actualizar Datos'),
            ('configuracion', '⚙️', 'Configuración')
        ]

        for panel_id, icon, text in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=f'{icon}  {text}',
                font=('Montserrat', 13),
                fg_color='transparent',
                text_color='#FFFFFF',
                hover_color='#252841',
                anchor='w',
                height=44,
                corner_radius=0,
                border_spacing=12,
                command=lambda p=panel_id: self.select_panel(p)
            )
            btn.pack(fill='x', padx=0)
            self.nav_buttons[panel_id] = btn

        # Seleccionar dashboard por defecto
        self.select_panel('dashboard')

    def create_special_button(self):
        """Crea el botón especial de Reportes Gerenciales TNG"""
        btn_frame = ctk.CTkFrame(self, fg_color='transparent')
        btn_frame.pack(fill='x', padx=15, pady=(15, 0))

        special_btn = ctk.CTkButton(
            btn_frame,
            text='📄  Reportes\n     Gerenciales TNG',
            font=('Montserrat', 12, 'bold'),
            fg_color='rgba(0, 155, 222, 0.15)',
            hover_color='rgba(0, 155, 222, 0.25)',
            text_color='#FFFFFF',
            border_width=1,
            border_color='#009BDE',
            corner_radius=8,
            height=60,
            anchor='w',
            command=self.open_tng_reports
        )
        special_btn.pack(fill='x')

    def create_spacer(self):
        """Crea un espaciador flexible"""
        spacer = ctk.CTkFrame(self, fg_color='transparent')
        spacer.pack(fill='both', expand=True)

    def create_footer(self):
        """Crea el footer con versión y copyright"""
        footer = ctk.CTkFrame(
            self,
            fg_color='rgba(0, 0, 0, 0.3)'
        )
        footer.pack(fill='x', side='bottom')

        version = ctk.CTkLabel(
            footer,
            text='Versión 2.0',
            font=('Arial', 9, 'bold'),
            text_color='#a0a3bd'
        )
        version.pack(pady=(15, 3))

        copyright_line1 = ctk.CTkLabel(
            footer,
            text='© 2025 Hutchison Ports',
            font=('Arial', 8),
            text_color='#6c6f93'
        )
        copyright_line1.pack(pady=1)

        copyright_line2 = ctk.CTkLabel(
            footer,
            text='Instituto HP',
            font=('Arial', 8),
            text_color='#6c6f93'
        )
        copyright_line2.pack(pady=(1, 15))

    def select_panel(self, panel_id):
        """Selecciona un panel y actualiza el estado visual"""
        # Restaurar todos los botones a estado normal
        for btn_id, btn in self.nav_buttons.items():
            if btn_id == panel_id:
                # Botón activo - Sky Blue corporativo
                btn.configure(
                    fg_color='#009BDE',  # Sky Blue corporativo
                    text_color='#FFFFFF',
                    font=('Montserrat', 13, 'bold')
                )
                # Agregar borde izquierdo visual (simulado con padding)
                btn.configure(border_spacing=8)
            else:
                # Botón inactivo
                btn.configure(
                    fg_color='transparent',
                    text_color='#FFFFFF',
                    font=('Montserrat', 13)
                )
                btn.configure(border_spacing=12)

        # Cambiar panel
        self.current_panel = panel_id
        self.switch_panel(panel_id)

    def open_tng_reports(self):
        """Abre la ventana de Reportes Gerenciales TNG"""
        messagebox.showinfo(
            'Reportes Gerenciales TNG',
            'Funcionalidad de Reportes Gerenciales TNG\n\n' +
            'Aquí se mostrarán los reportes ejecutivos y gerenciales\n' +
            'del Instituto Hutchison Ports TNG.'
        )


# Para testing standalone
if __name__ == '__main__':
    root = ctk.CTk()
    root.title("Test Sidebar Modern")
    root.geometry("800x600")

    ctk.set_appearance_mode("dark")

    def switch_panel(panel_id):
        print(f"Switching to panel: {panel_id}")

    sidebar = SidebarModern(root, switch_panel)
    sidebar.pack(side='left', fill='y')

    # Content area de ejemplo
    content = ctk.CTkFrame(root, fg_color='#2b2d42')
    content.pack(side='right', fill='both', expand=True)

    ctk.CTkLabel(content, text='Content Area', font=('Arial', 20),
                text_color='white').pack(expand=True)

    root.mainloop()
