"""
Panel Configuración Modern - Diseño Oscuro
Configuración con cards oscuras y botones corporativos
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from smart_reports.config.settings_modern import get_color_modern, get_font_modern
from smart_reports.ui.modern.config_card_modern import ConfigCardModern


class ConfiguracionModern(ctk.CTkFrame):
    """Panel de configuración con diseño oscuro"""

    def __init__(self, parent, db=None):
        super().__init__(parent, fg_color=get_color_modern('background'))
        self.db = db
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_interface()

    def _create_interface(self):
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color='transparent', corner_radius=0)
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(scroll_frame, text='Configuración del Sistema',
                                   font=get_font_modern('title', 28, 'bold'),
                                   text_color=get_color_modern('text_primary'), anchor='w')
        title_label.pack(fill='x', pady=(0, 30))

        # Container de cards
        cards_container = ctk.CTkFrame(scroll_frame, fg_color='transparent')
        cards_container.pack(fill='both', expand=True)
        cards_container.grid_columnconfigure((0, 1), weight=1)

        # Card 1: Gestionar Usuarios
        card1 = ConfigCardModern(cards_container, icon='👥', title='Gestionar Usuarios',
                                description='Agregar, editar o eliminar usuarios del sistema',
                                button_text='Gestionar', button_color=get_color_modern('accent_primary'),
                                command=self.open_user_editor)
        card1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Card 2: Respaldar BD
        card2 = ConfigCardModern(cards_container, icon='💾', title='Respaldar Base de Datos',
                                description='Crear copia de seguridad de todos los datos',
                                button_text='Respaldar', button_color=get_color_modern('accent_green'),
                                command=self.backup_database)
        card2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Card 3: Acerca de
        card3 = ConfigCardModern(cards_container, icon='ℹ️', title='Acerca de',
                                description='Información sobre la aplicación y versión',
                                button_text='Ver Información', button_color=get_color_modern('accent_orange'),
                                command=self.show_about)
        card3.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Card 4: Configuración BD
        card4 = ConfigCardModern(cards_container, icon='🔧', title='Configuración BD',
                                description='Configurar conexión a base de datos',
                                button_text='Configurar', button_color=get_color_modern('accent_red'),
                                command=self.config_database)
        card4.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def open_user_editor(self):
        messagebox.showinfo("Gestionar Usuarios", "Editor de usuarios en desarrollo.")

    def backup_database(self):
        if not self.db:
            messagebox.showerror("Error", "No hay conexión a la base de datos.")
            return
        
        file_path = filedialog.asksaveasfilename(title='Guardar respaldo',
                                                defaultextension='.bak',
                                                filetypes=[('Backup files', '*.bak'), ('All files', '*.*')])
        if file_path:
            messagebox.showinfo("Respaldo", f"Respaldo simulado creado en:\n{file_path}")

    def show_about(self):
        messagebox.showinfo("Acerca de Smart Reports",
                           "SMART REPORTS - INSTITUTO HUTCHISON PORTS\n\n"
                           "Versión: 2.0 (Modern)\n"
                           "Sistema de Gestión de Capacitaciones\n\n"
                           "Diseño: Oscuro con tipografía corporativa\n"
                           "- Paleta oscura\n"
                           "- Tipografía: Montserrat + Arial\n"
                           "- Botones corporativos Sky Blue\n\n"
                           "Desarrollado con CustomTkinter\n"
                           "(c) 2024 Instituto Hutchison Ports")

    def config_database(self):
        messagebox.showinfo("Configuración BD",
                           "Panel de configuración de base de datos.\n\n"
                           "Funcionalidad en desarrollo.")
