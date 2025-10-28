"""
Panel Configuración Hutchison
Panel de configuración con cards funcionales (botones VISIBLES)
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from smart_reports.config.settings_hutchison import (
    get_color,
    get_font
)
from smart_reports.ui.hutchison.config_card_hutchison import ConfigCardHutchison


class ConfiguracionHutchison(ctk.CTkFrame):
    """
    Panel de configuración con 4 cards:
    1. Gestionar Usuarios
    2. Respaldar Base de Datos
    3. Acerca de
    4. Configuración BD
    """

    def __init__(self, parent, db=None):
        """
        Args:
            parent: Widget padre (content_area)
            db: Conexión a base de datos
        """
        super().__init__(parent, fg_color=get_color('White'))

        self.db = db

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_interface()

    def _create_interface(self):
        """Crear interfaz del panel"""

        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=get_color('White'),
            corner_radius=0
        )
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(
            scroll_frame,
            text='Configuración del Sistema',
            font=get_font('title', 28, 'bold'),
            text_color=get_color('Sea Blue'),
            anchor='w'
        )
        title_label.pack(fill='x', pady=(0, 30))

        # Container de cards con grid
        cards_container = ctk.CTkFrame(scroll_frame, fg_color='transparent')
        cards_container.pack(fill='both', expand=True)

        # Configurar grid: 2 columnas
        cards_container.grid_columnconfigure((0, 1), weight=1)

        # === CARD 1: Gestionar Usuarios ===
        card1 = ConfigCardHutchison(
            cards_container,
            icon='👥',
            title='Gestionar Usuarios',
            description='Agregar, editar o eliminar usuarios del sistema',
            button_text='Gestionar',
            button_color=get_color('Sky Blue'),
            command=self.open_user_editor
        )
        card1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # === CARD 2: Respaldar Base de Datos ===
        card2 = ConfigCardHutchison(
            cards_container,
            icon='💾',
            title='Respaldar Base de Datos',
            description='Crear copia de seguridad de todos los datos',
            button_text='Respaldar',
            button_color=get_color('Success Green'),
            command=self.backup_database
        )
        card2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # === CARD 3: Acerca de ===
        card3 = ConfigCardHutchison(
            cards_container,
            icon='ℹ️',
            title='Acerca de',
            description='Información sobre la aplicación y versión',
            button_text='Ver Información',
            button_color=get_color('Warning Orange'),
            command=self.show_about
        )
        card3.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # === CARD 4: Configuración BD ===
        card4 = ConfigCardHutchison(
            cards_container,
            icon='🔧',
            title='Configuración BD',
            description='Configurar conexión a base de datos',
            button_text='Configurar',
            button_color=get_color('Error Red'),
            command=self.config_database
        )
        card4.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def open_user_editor(self):
        """Abre ventana de gestión de usuarios"""
        print("🔧 Abriendo gestor de usuarios...")

        # Crear ventana modal
        editor = ctk.CTkToplevel(self)
        editor.title("Gestionar Usuarios")
        editor.geometry("900x700")
        editor.grab_set()  # Modal

        # Centrar ventana
        editor.update_idletasks()
        x = (editor.winfo_screenwidth() // 2) - (450)
        y = (editor.winfo_screenheight() // 2) - (350)
        editor.geometry(f"900x700+{x}+{y}")

        # Contenido
        header = ctk.CTkLabel(
            editor,
            text='🎼 Editor de Usuarios',
            font=get_font('title', 24, 'bold'),
            text_color=get_color('Sea Blue')
        )
        header.pack(pady=20)

        info = ctk.CTkLabel(
            editor,
            text='Aquí podrás agregar, editar y eliminar usuarios del sistema.\n'
                 'Esta funcionalidad está en desarrollo.',
            font=get_font('body', 14),
            text_color=get_color('Medium Gray')
        )
        info.pack(pady=10)

        # Botón cerrar
        btn_close = ctk.CTkButton(
            editor,
            text='Cerrar',
            font=get_font('heading_medium', 14, 'bold'),
            fg_color=get_color('Sky Blue'),
            hover_color=get_color('Sea Blue'),
            command=editor.destroy,
            width=150,
            height=40
        )
        btn_close.pack(pady=20)

    def backup_database(self):
        """Crear respaldo de la base de datos"""
        print("💾 Creando respaldo...")

        if not self.db:
            messagebox.showerror(
                "Error",
                "No hay conexión a la base de datos.\n"
                "No se puede crear el respaldo."
            )
            return

        # Seleccionar ubicación
        file_path = filedialog.asksaveasfilename(
            title='Guardar respaldo de base de datos',
            defaultextension='.bak',
            filetypes=[('Backup files', '*.bak'), ('All files', '*.*')]
        )

        if file_path:
            messagebox.showinfo(
                "Respaldo",
                f"Respaldo simulado creado en:\n{file_path}\n\n"
                "Funcionalidad completa en desarrollo."
            )

    def show_about(self):
        """Mostrar información sobre la aplicación"""
        messagebox.showinfo(
            "Acerca de Smart Reports",
            "SMART REPORTS - INSTITUTO HUTCHISON PORTS\n\n"
            "Versión: 2.0 (Hutchison)\n"
            "Sistema de Gestión de Capacitaciones\n\n"
            "Diseño: Identidad Visual Hutchison Ports\n"
            "- Paleta corporativa\n"
            "- Tipografía: Montserrat + Arial\n"
            "- Dynamic Angle: 30.3°\n\n"
            "Desarrollado con CustomTkinter\n"
            "(c) 2024 Instituto Hutchison Ports"
        )

    def config_database(self):
        """Configurar conexión a base de datos"""
        print("🔧 Configurando base de datos...")

        messagebox.showinfo(
            "Configuración BD",
            "Panel de configuración de base de datos.\n\n"
            "Aquí podrás configurar:\n"
            "- Tipo de BD (SQL Server / MySQL)\n"
            "- Servidor y puerto\n"
            "- Credenciales\n\n"
            "Funcionalidad en desarrollo."
        )


# Para testing standalone
if __name__ == '__main__':
    root = ctk.CTk()
    root.title("Test Configuración Hutchison")
    root.geometry("1200x800")

    ctk.set_appearance_mode("light")

    panel = ConfiguracionHutchison(root)
    panel.pack(fill='both', expand=True)

    root.mainloop()
