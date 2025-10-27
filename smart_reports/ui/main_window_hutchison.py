"""
Ventana principal de Smart Reports - VERSIÓN HUTCHISON PORTS
Rediseño corporativo completo según Manual de Identidad Visual
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from datetime import datetime
import os

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    DRAG_DROP_AVAILABLE = False
    print("Warning: tkinterdnd2 no disponible. Drag & drop deshabilitado.")

from smart_reports.config.hutchison_identity import get_hutchison_theme, get_font
from smart_reports.database.connection import DatabaseConnection
from smart_reports.services.data_processor import TranscriptProcessor

# Componentes Hutchison
from smart_reports.ui.components.hutchison_widgets import (
    AngledHeaderFrame,
    AngledDivider,
    HutchisonButton,
    HutchisonLabel,
    LogoFrame,
    MetricCardAngled,
    AngledCard
)
from smart_reports.ui.components.hutchison_sidebar import HutchisonSidebar
from smart_reports.ui.components.hutchison_config_card import HutchisonConfigCard

# Componentes originales (para funcionalidad)
from smart_reports.ui.panels.modern_dashboard import ModernDashboard
from smart_reports.ui.dialogs.user_management_dialog import UserManagementDialog


class MainWindowHutchison:
    """Ventana principal con diseño corporativo Hutchison Ports"""

    def __init__(self, root):
        self.root = root
        self.root.title("SMART REPORTS - HUTCHISON PORTS")
        self.root.geometry("1400x900")

        # Tema corporativo Hutchison
        self.theme = get_hutchison_theme()
        self.root.configure(fg_color=self.theme['background'])

        # Base de datos
        self.db = DatabaseConnection()
        self.conn = None
        self.cursor = None

        try:
            self.conn = self.db.connect()
            self.cursor = self.db.get_cursor()
            self.verify_database_tables()
        except Exception as e:
            messagebox.showerror("Error de Conexión",
                f"No se pudo conectar a la base de datos:\n{str(e)}\n\n"
                "La aplicación continuará pero algunas funciones no estarán disponibles.")

        # Variables de tracking
        self.current_file = None
        self.changes_log = []
        self.current_panel = None

        # Crear interfaz Hutchison
        self.create_hutchison_interface()

    def verify_database_tables(self):
        """Verificar que las tablas necesarias existan"""
        tables_needed = ['Instituto_UnidadDeNegocio', 'Instituto_Usuario',
                        'Instituto_Modulo', 'Instituto_ProgresoModulo']
        placeholders = ','.join(['?' for _ in tables_needed])

        try:
            self.cursor.execute(f"""
                SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
                AND TABLE_NAME IN ({placeholders})
            """, tables_needed)

            existing_tables = [t[0] for t in self.cursor.fetchall()]

            if len(existing_tables) < len(tables_needed):
                missing = set(tables_needed) - set(existing_tables)
                messagebox.showwarning("Advertencia",
                    f"Faltan tablas en la BD: {', '.join(missing)}\n" +
                    "Verifique que las tablas existan en la base de datos.")
        except Exception as e:
            print(f"Error verificando tablas: {e}")

    def create_hutchison_interface(self):
        """Crear interfaz con diseño Hutchison Ports"""
        # Container principal
        self.main_container = ctk.CTkFrame(
            self.root,
            fg_color=self.theme['background'],
            corner_radius=0
        )
        self.main_container.pack(fill='both', expand=True)

        # Barra superior con logo
        self._create_top_bar()

        # Container para sidebar y contenido
        content_container = ctk.CTkFrame(
            self.main_container,
            fg_color='transparent'
        )
        content_container.pack(fill='both', expand=True)

        # Sidebar corporativo (Sea Blue)
        navigation_callbacks = {
            'dashboard': self.show_dashboard_panel,
            'consultas': self.show_consultas_panel,
            'actualizar': self.show_actualizar_panel,
            'configuracion': self.show_configuracion_panel,
        }

        self.sidebar = HutchisonSidebar(content_container, navigation_callbacks)
        self.sidebar.pack(side='left', fill='y')

        # Área de contenido principal
        self.content_area = ctk.CTkFrame(
            content_container,
            fg_color=self.theme['background'],
            corner_radius=0
        )
        self.content_area.pack(side='left', fill='both', expand=True)

        # Mostrar dashboard por defecto
        self.show_dashboard_panel()
        self.sidebar.set_active('dashboard')

    def _create_top_bar(self):
        """Crear barra superior con logo corporativo"""
        top_bar = ctk.CTkFrame(
            self.main_container,
            fg_color=self.theme['surface'],
            height=80,
            corner_radius=0
        )
        top_bar.pack(fill='x', padx=0, pady=0)
        top_bar.pack_propagate(False)

        # Logo en esquina superior izquierda (obligatorio según manual)
        logo = LogoFrame(top_bar)
        logo.pack(side='left', padx=20, pady=10)

        # Separador Sky Blue
        separator = ctk.CTkFrame(
            self.main_container,
            height=3,
            fg_color=self.theme['primary']
        )
        separator.pack(fill='x')

    def clear_content_area(self):
        """Limpiar área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # ==================== PANEL DE DASHBOARD ====================

    def show_dashboard_panel(self):
        """Mostrar panel de dashboard con diseño Hutchison"""
        self.clear_content_area()
        self.current_panel = 'dashboard'

        if self.conn is None:
            self._show_error_panel("No hay conexión a la base de datos")
            return

        # Scroll frame para contenido
        scroll_frame = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header angulado (Sky Shape)
        header = AngledHeaderFrame(
            scroll_frame,
            text='Dashboard',
            height=80,
            color=self.theme['primary']
        )
        header.pack(fill='x', pady=(0, 20))

        # Divisor angulado
        divider = AngledDivider(
            scroll_frame,
            height=4,
            color=self.theme['secondary']
        )
        divider.pack(fill='x', pady=(0, 30))

        # Grid de métricas corporativas
        self._create_metrics_grid(scroll_frame)

        # Divisor
        divider2 = AngledDivider(
            scroll_frame,
            height=4,
            color=self.theme['accent_orange']
        )
        divider2.pack(fill='x', pady=30)

        # Dashboard completo (reutilizar el existente)
        dashboard = ModernDashboard(scroll_frame, self.conn)
        dashboard.pack(fill='both', expand=True)

    def _create_metrics_grid(self, parent):
        """Crear grid de métricas con tarjetas anguladas"""
        metrics_grid = ctk.CTkFrame(parent, fg_color='transparent')
        metrics_grid.pack(fill='x', pady=20)

        metrics_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        try:
            # Métrica 1: Total Usuarios
            self.cursor.execute("SELECT COUNT(*) FROM Instituto_Usuario")
            total_users = self.cursor.fetchone()[0]

            metric1 = MetricCardAngled(
                metrics_grid,
                title='Total Usuarios',
                value=f'{total_users:,}',
                subtitle='Usuarios en el sistema',
                color=self.theme['primary']
            )
            metric1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

            # Métrica 2: Módulos
            self.cursor.execute("SELECT COUNT(*) FROM Instituto_Modulo")
            total_modules = self.cursor.fetchone()[0]

            metric2 = MetricCardAngled(
                metrics_grid,
                title='Módulos',
                value=str(total_modules),
                subtitle='Módulos disponibles',
                color=self.theme['secondary']
            )
            metric2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

            # Métrica 3: Completados
            self.cursor.execute("""
                SELECT COUNT(*) FROM Instituto_ProgresoModulo
                WHERE EstatusModuloUsuario = 'Terminado'
            """)
            completed = self.cursor.fetchone()[0]

            metric3 = MetricCardAngled(
                metrics_grid,
                title='Completados',
                value=f'{completed:,}',
                subtitle='Módulos terminados',
                color=self.theme['accent_yellow']
            )
            metric3.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

            # Métrica 4: Progreso Global
            self.cursor.execute("""
                SELECT
                    COUNT(CASE WHEN EstatusModuloUsuario = 'Terminado' THEN 1 END) * 100.0 / COUNT(*) as Porcentaje
                FROM Instituto_ProgresoModulo
            """)
            result = self.cursor.fetchone()
            progress = f'{result[0]:.1f}%' if result[0] else '0%'

            metric4 = MetricCardAngled(
                metrics_grid,
                title='Progreso Global',
                value=progress,
                subtitle='Del total',
                color=self.theme['accent_orange']
            )
            metric4.grid(row=0, column=3, padx=10, pady=10, sticky='nsew')

        except Exception as e:
            print(f"Error cargando métricas: {e}")

    def _show_error_panel(self, message):
        """Mostrar panel de error"""
        error_frame = ctk.CTkFrame(self.content_area, fg_color='transparent')
        error_frame.pack(fill='both', expand=True)

        error_label = HutchisonLabel(
            error_frame,
            text=f'⚠️ {message}',
            label_type='heading'
        )
        error_label.configure(text_color='#ff6b6b')
        error_label.pack(expand=True)

    # ==================== PANEL DE CONSULTAS ====================

    def show_consultas_panel(self):
        """Mostrar panel de consultas con diseño Hutchison"""
        self.clear_content_area()
        self.current_panel = 'consultas'

        if self.conn is None:
            self._show_error_panel("No hay conexión a la base de datos")
            return

        # Continúa en siguiente archivo...
        # Por ahora mostramos un placeholder
        scroll_frame = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        header = AngledHeaderFrame(
            scroll_frame,
            text='Consultas de Usuarios',
            height=80,
            color=self.theme['secondary']
        )
        header.pack(fill='x', pady=(0, 20))

        # Aquí iría el contenido completo del panel de consultas
        # Lo implementaré en la siguiente parte

    # ==================== PANEL DE ACTUALIZAR ====================

    def show_actualizar_panel(self):
        """Mostrar panel de actualización con diseño Hutchison"""
        self.clear_content_area()
        self.current_panel = 'actualizar'

        scroll_frame = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        header = AngledHeaderFrame(
            scroll_frame,
            text='Actualizar Datos',
            height=80,
            color=self.theme['accent_orange']
        )
        header.pack(fill='x', pady=(0, 20))

        # Continúa con el panel de actualización...

    # ==================== PANEL DE CONFIGURACIÓN ====================

    def show_configuracion_panel(self):
        """Mostrar panel de configuración con diseño Hutchison"""
        self.clear_content_area()
        self.current_panel = 'configuracion'

        # Frame principal
        main_frame = ctk.CTkFrame(self.content_area, fg_color='transparent')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header angulado
        header = AngledHeaderFrame(
            main_frame,
            text='Configuración',
            height=80,
            color=self.theme['primary']
        )
        header.pack(fill='x', pady=(0, 20))

        # Divisor
        divider = AngledDivider(
            main_frame,
            height=4,
            color=self.theme['secondary']
        )
        divider.pack(fill='x', pady=(0, 30))

        # Grid 2x2 para tarjetas
        grid_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        grid_frame.pack(fill='both', expand=True)

        grid_frame.grid_columnconfigure((0, 1), weight=1)
        grid_frame.grid_rowconfigure((0, 1), weight=1)

        # Tarjetas de configuración con colores corporativos
        card1 = HutchisonConfigCard(
            grid_frame,
            icon='👥',
            title='Gestionar Usuarios',
            description='Agregar nuevos usuarios o editar información de usuarios existentes',
            button_text='Gestionar',
            button_color=self.theme['primary'],
            command=self.show_user_management
        )
        card1.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')

        card2 = HutchisonConfigCard(
            grid_frame,
            icon='💾',
            title='Respaldar Base de Datos',
            description='Crear un respaldo de seguridad de la base de datos actual',
            button_text='Respaldar',
            button_color=self.theme['secondary'],
            command=self.backup_database
        )
        card2.grid(row=0, column=1, padx=15, pady=15, sticky='nsew')

        card3 = HutchisonConfigCard(
            grid_frame,
            icon='ℹ️',
            title='Acerca de',
            description='Información sobre Smart Reports y versión del software',
            button_text='Ver Info',
            button_color=self.theme['accent_yellow'],
            command=self.show_about
        )
        card3.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')

        card4 = HutchisonConfigCard(
            grid_frame,
            icon='🔧',
            title='Configuración BD',
            description='Cambiar configuración de base de datos',
            button_text='Cambiar',
            button_color=self.theme['accent_orange'],
            command=self.show_database_config
        )
        card4.grid(row=1, column=1, padx=15, pady=15, sticky='nsew')

    # ==================== FUNCIONES DE CONFIGURACIÓN ====================

    def show_user_management(self):
        """Mostrar ventana de gestión de usuarios"""
        if self.conn is None:
            messagebox.showerror("Error de Conexión",
                "No hay conexión a la base de datos.\n" +
                "No se puede gestionar usuarios sin conexión.")
            return

        dialog = UserManagementDialog(self.root, self.conn)
        self.root.wait_window(dialog)

        if dialog.result in ['created', 'updated'] and self.current_panel == 'dashboard':
            self.show_dashboard_panel()

    def backup_database(self):
        """Crear respaldo de la base de datos"""
        from smart_reports.config.settings import DB_TYPE

        try:
            if DB_TYPE == 'sqlserver':
                messagebox.showinfo("Respaldo SQL Server",
                    "Para respaldar SQL Server:\n\n" +
                    "1. Usa SQL Server Management Studio\n" +
                    "2. Click derecho en la base de datos\n" +
                    "3. Tasks → Back Up...\n\n" +
                    "O ejecuta:\n" +
                    "BACKUP DATABASE TNGCORE TO DISK = 'C:\\Backups\\TNGCORE.bak'")
            else:
                messagebox.showinfo("Respaldo MySQL",
                    "Para respaldar MySQL:\n\n" +
                    "Ejecuta en terminal:\n" +
                    "mysqldump -u root -p tngcore > backup.sql")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear respaldo:\n{str(e)}")

    def show_about(self):
        """Mostrar información sobre la aplicación"""
        messagebox.showinfo("Acerca de",
            "SMART REPORTS V2.0\n" +
            "DISEÑO CORPORATIVO HUTCHISON PORTS\n\n" +
            "SISTEMA DE GESTIÓN DE CAPACITACIONES\n" +
            "INSTITUTO HUTCHISON PORTS\n\n" +
            "© 2025 - TODOS LOS DERECHOS RESERVADOS")

    def show_database_config(self):
        """Mostrar configuración de base de datos"""
        from smart_reports.config.settings import DB_TYPE, SQLSERVER_CONFIG, MYSQL_CONFIG

        current = "SQL Server (Trabajo)" if DB_TYPE == 'sqlserver' else "MySQL (Casa)"

        messagebox.showinfo("Configuración de Base de Datos",
            f"Base de datos actual: {current}\n\n" +
            f"Para cambiar:\n" +
            f"1. Edita: smart_reports/config/settings.py\n" +
            f"2. Cambia DB_TYPE a 'sqlserver' o 'mysql'\n" +
            f"3. Reinicia la aplicación")


def main():
    """Función principal - Versión Hutchison"""
    root = ctk.CTk()
    app = MainWindowHutchison(root)
    root.mainloop()


if __name__ == '__main__':
    main()
