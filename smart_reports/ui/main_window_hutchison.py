"""
SMART REPORTS - HUTCHISON PORTS
Ventana principal con diseño corporativo completo
Versión 2.0 - Manual de Identidad Visual
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from datetime import datetime
import os
import pandas as pd

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    DRAG_DROP_AVAILABLE = False
    print("⚠️ tkinterdnd2 no disponible. Drag & drop deshabilitado.")

from smart_reports.config.hutchison_identity import get_hutchison_theme, get_font
from smart_reports.database.connection import DatabaseConnection
from smart_reports.services.data_processor import TranscriptProcessor

# Componentes corporativos Hutchison
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
from smart_reports.ui.dialogs.user_management_dialog import UserManagementDialog


class MainWindow:
    """Ventana principal - Diseño Corporativo Hutchison Ports"""

    def __init__(self, root):
        self.root = root
        self.root.title("SMART REPORTS - HUTCHISON PORTS")
        self.root.geometry("1400x900")

        # Tema corporativo
        self.theme = get_hutchison_theme()
        self.root.configure(fg_color=self.theme['background'])

        # Variables de estado
        self.current_file = None
        self.changes_log = []
        self.current_panel = None
        self.processor = TranscriptProcessor()

        # Conexión a base de datos (opcional)
        self.db = DatabaseConnection()
        self.conn = None
        self.cursor = None

        try:
            self.conn = self.db.connect()
            self.cursor = self.db.get_cursor()
            print("✓ Conectado a la base de datos")
        except Exception as e:
            print(f"⚠️ No hay conexión a BD: {e}")
            print("   La aplicación funcionará en modo offline")

        # Crear interfaz
        self._create_interface()

    def _create_interface(self):
        """Crear interfaz principal"""
        # Container principal
        self.main_container = ctk.CTkFrame(
            self.root,
            fg_color=self.theme['background'],
            corner_radius=0
        )
        self.main_container.pack(fill='both', expand=True)

        # Barra superior con logo
        self._create_top_bar()

        # Container para sidebar + contenido
        content_container = ctk.CTkFrame(
            self.main_container,
            fg_color='transparent'
        )
        content_container.pack(fill='both', expand=True)

        # Sidebar corporativo (Sea Blue)
        navigation_callbacks = {
            'dashboard': self.show_dashboard,
            'consultas': self.show_consultas,
            'actualizar': self.show_actualizar,
            'configuracion': self.show_configuracion,
        }

        self.sidebar = HutchisonSidebar(content_container, navigation_callbacks)
        self.sidebar.pack(side='left', fill='y')

        # Área de contenido
        self.content_area = ctk.CTkFrame(
            content_container,
            fg_color=self.theme['background'],
            corner_radius=0
        )
        self.content_area.pack(side='left', fill='both', expand=True)

        # Mostrar dashboard inicial
        self.show_dashboard()
        self.sidebar.set_active('dashboard')

    def _create_top_bar(self):
        """Crear barra superior con logo corporativo"""
        top_bar = ctk.CTkFrame(
            self.main_container,
            fg_color=self.theme['surface'],
            height=80,
            corner_radius=0
        )
        top_bar.pack(fill='x')
        top_bar.pack_propagate(False)

        # Logo en esquina superior izquierda (obligatorio)
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

    # ==================== DASHBOARD ====================

    def show_dashboard(self):
        """Panel de Dashboard con diseño Hutchison"""
        self.clear_content_area()
        self.current_panel = 'dashboard'

        scroll_frame = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header angulado
        header = AngledHeaderFrame(
            scroll_frame,
            text='Dashboard',
            height=80,
            color=self.theme['primary']
        )
        header.pack(fill='x', pady=(0, 20))

        # Divisor
        divider = AngledDivider(
            scroll_frame,
            height=4,
            color=self.theme['secondary']
        )
        divider.pack(fill='x', pady=(0, 30))

        # Métricas
        self._create_metrics_grid(scroll_frame)

        # Divisor
        divider2 = AngledDivider(
            scroll_frame,
            height=4,
            color=self.theme['accent_orange']
        )
        divider2.pack(fill='x', pady=30)

        # Información adicional
        info_card = AngledCard(
            scroll_frame,
            title='Información del Sistema',
            header_color=self.theme['primary']
        )
        info_card.pack(fill='x', pady=20)

        info_text = HutchisonLabel(
            info_card.content_frame,
            text=(
                "Sistema de Gestión de Capacitaciones\n\n" +
                "Este dashboard muestra métricas en tiempo real del progreso de capacitación " +
                "de todos los usuarios del Instituto Hutchison Ports.\n\n" +
                f"Estado BD: {'✓ Conectado' if self.conn else '✗ Desconectado'}"
            ),
            label_type='body'
        )
        info_text.configure(wraplength=800, justify='left')
        info_text.pack(pady=10)

    def _create_metrics_grid(self, parent):
        """Crear grid de métricas con tarjetas anguladas"""
        metrics_grid = ctk.CTkFrame(parent, fg_color='transparent')
        metrics_grid.pack(fill='x', pady=20)

        metrics_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        if self.conn and self.cursor:
            try:
                # Métricas reales de BD
                self.cursor.execute("SELECT COUNT(*) FROM Instituto_Usuario")
                total_users = self.cursor.fetchone()[0]

                self.cursor.execute("SELECT COUNT(*) FROM Instituto_Modulo")
                total_modules = self.cursor.fetchone()[0]

                self.cursor.execute("""
                    SELECT COUNT(*) FROM Instituto_ProgresoModulo
                    WHERE EstatusModuloUsuario = 'Terminado'
                """)
                completed = self.cursor.fetchone()[0]

                self.cursor.execute("""
                    SELECT
                        COUNT(CASE WHEN EstatusModuloUsuario = 'Terminado' THEN 1 END) * 100.0 /
                        NULLIF(COUNT(*), 0) as Porcentaje
                    FROM Instituto_ProgresoModulo
                """)
                result = self.cursor.fetchone()
                progress = f'{result[0]:.1f}%' if result and result[0] else '0%'

            except Exception as e:
                print(f"Error cargando métricas: {e}")
                # Valores por defecto
                total_users = 0
                total_modules = 0
                completed = 0
                progress = '0%'
        else:
            # Modo sin BD - Datos de demostración
            total_users = 156
            total_modules = 24
            completed = 892
            progress = '73.5%'

        # Tarjeta 1
        metric1 = MetricCardAngled(
            metrics_grid,
            title='Total Usuarios',
            value=f'{total_users:,}',
            subtitle='Usuarios en el sistema',
            color=self.theme['primary']
        )
        metric1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Tarjeta 2
        metric2 = MetricCardAngled(
            metrics_grid,
            title='Módulos',
            value=str(total_modules),
            subtitle='Módulos disponibles',
            color=self.theme['secondary']
        )
        metric2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Tarjeta 3
        metric3 = MetricCardAngled(
            metrics_grid,
            title='Completados',
            value=f'{completed:,}',
            subtitle='Módulos terminados',
            color=self.theme['accent_yellow']
        )
        metric3.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # Tarjeta 4
        metric4 = MetricCardAngled(
            metrics_grid,
            title='Progreso Global',
            value=progress,
            subtitle='Del total',
            color=self.theme['accent_orange']
        )
        metric4.grid(row=0, column=3, padx=10, pady=10, sticky='nsew')

    # ==================== CONSULTAS ====================

    def show_consultas(self):
        """Panel de Consultas con diseño Hutchison"""
        self.clear_content_area()
        self.current_panel = 'consultas'

        scroll_frame = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header angulado
        header = AngledHeaderFrame(
            scroll_frame,
            text='Consultas de Usuarios',
            height=80,
            color=self.theme['secondary']
        )
        header.pack(fill='x', pady=(0, 20))

        if not self.conn:
            # Sin conexión a BD
            self._show_no_db_message(scroll_frame, 'consultas')
            return

        # Card de búsqueda
        search_card = AngledCard(
            scroll_frame,
            title='Búsqueda de Usuarios',
            header_color=self.theme['primary']
        )
        search_card.pack(fill='x', pady=20)

        # Búsqueda por ID
        search_frame = ctk.CTkFrame(search_card.content_frame, fg_color='transparent')
        search_frame.pack(fill='x', pady=10)

        HutchisonLabel(
            search_frame,
            text='🔍  Buscar por User ID:',
            label_type='heading'
        ).pack(side='left', padx=(0, 15))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text='Ingrese ID de usuario...',
            font=get_font('body', 14),
            width=300,
            height=40
        )
        self.search_entry.pack(side='left', padx=5)

        HutchisonButton(
            search_frame,
            text='Buscar',
            button_type='primary',
            width=120,
            command=self.search_user
        ).pack(side='left', padx=10)

        # Resultado de búsqueda
        self.search_result_frame = ctk.CTkFrame(
            search_card.content_frame,
            fg_color=self.theme['surface'],
            corner_radius=10
        )
        self.search_result_frame.pack(fill='both', expand=True, pady=(20, 0))

        self.search_result_label = HutchisonLabel(
            self.search_result_frame,
            text='Ingrese un User ID y haga clic en Buscar',
            label_type='body'
        )
        self.search_result_label.pack(pady=30)

    def search_user(self):
        """Buscar usuario por ID"""
        user_id = self.search_entry.get().strip()

        if not user_id:
            messagebox.showwarning("Advertencia", "Ingrese un User ID")
            return

        if not self.conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            self.cursor.execute("""
                SELECT u.UserId, u.Nombre, u.Email, un.NombreUnidad
                FROM Instituto_Usuario u
                LEFT JOIN Instituto_UnidadDeNegocio un ON u.IdUnidadDeNegocio = un.IdUnidadDeNegocio
                WHERE u.UserId = ?
            """, (user_id,))

            result = self.cursor.fetchone()

            # Limpiar resultado anterior
            for widget in self.search_result_frame.winfo_children():
                widget.destroy()

            if result:
                # Mostrar resultado
                result_container = ctk.CTkFrame(
                    self.search_result_frame,
                    fg_color='transparent'
                )
                result_container.pack(fill='both', expand=True, padx=30, pady=20)

                HutchisonLabel(
                    result_container,
                    text='✓ Usuario Encontrado',
                    label_type='heading'
                ).configure(text_color=self.theme['secondary'])
                HutchisonLabel(
                    result_container,
                    text='✓ Usuario Encontrado',
                    label_type='heading'
                ).pack(pady=(0, 20))

                info_text = f"""
User ID: {result[0]}
Nombre: {result[1] or 'N/A'}
Email: {result[2] or 'N/A'}
Unidad: {result[3] or 'N/A'}
                """.strip()

                HutchisonLabel(
                    result_container,
                    text=info_text,
                    label_type='body'
                ).configure(justify='left')
                HutchisonLabel(
                    result_container,
                    text=info_text,
                    label_type='body'
                ).pack()

            else:
                HutchisonLabel(
                    self.search_result_frame,
                    text=f'✗ No se encontró el usuario: {user_id}',
                    label_type='heading'
                ).configure(text_color='#ff6b6b')
                HutchisonLabel(
                    self.search_result_frame,
                    text=f'✗ No se encontró el usuario: {user_id}',
                    label_type='heading'
                ).pack(pady=30)

        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar:\n{str(e)}")

    # ==================== ACTUALIZAR DATOS ====================

    def show_actualizar(self):
        """Panel de Actualizar con diseño Hutchison"""
        self.clear_content_area()
        self.current_panel = 'actualizar'

        scroll_frame = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header angulado
        header = AngledHeaderFrame(
            scroll_frame,
            text='Actualizar Datos',
            height=80,
            color=self.theme['accent_orange']
        )
        header.pack(fill='x', pady=(0, 20))

        # Card principal
        update_card = AngledCard(
            scroll_frame,
            title='Cargar Archivo Excel',
            header_color=self.theme['primary']
        )
        update_card.pack(fill='x', pady=20)

        # Drop zone
        drop_zone = ctk.CTkFrame(
            update_card.content_frame,
            fg_color=self.theme['surface'],
            corner_radius=15,
            border_width=3,
            border_color=self.theme['primary'],
            height=180
        )
        drop_zone.pack(fill='x', pady=20)
        drop_zone.pack_propagate(False)

        drop_icon = HutchisonLabel(
            drop_zone,
            text='📁',
            label_type='title'
        )
        drop_icon.configure(font=get_font('heading', 64))
        drop_icon.pack(pady=(30, 10))

        if DRAG_DROP_AVAILABLE:
            drop_text = HutchisonLabel(
                drop_zone,
                text='Arrastra archivo Excel aquí',
                label_type='heading'
            )
            drop_text.pack()

            drop_subtext = HutchisonLabel(
                drop_zone,
                text='o usa el botón de abajo',
                label_type='caption'
            )
            drop_subtext.pack(pady=5)

            # Configurar drag & drop
            try:
                drop_zone.drop_target_register(DND_FILES)
                drop_zone.dnd_bind('<<Drop>>', self._on_file_drop)
                drop_zone.dnd_bind('<<DragEnter>>',
                    lambda e: drop_zone.configure(border_color=self.theme['secondary']))
                drop_zone.dnd_bind('<<DragLeave>>',
                    lambda e: drop_zone.configure(border_color=self.theme['primary']))
            except:
                pass
        else:
            drop_text = HutchisonLabel(
                drop_zone,
                text='Usar botón para seleccionar archivo',
                label_type='heading'
            )
            drop_text.pack()

        # Botón seleccionar
        HutchisonButton(
            update_card.content_frame,
            text='📂  Seleccionar Archivo Excel',
            button_type='primary',
            command=self.select_file
        ).pack(pady=20)

        # Información del archivo
        self.file_info_frame = ctk.CTkFrame(
            update_card.content_frame,
            fg_color=self.theme['surface'],
            corner_radius=10
        )
        self.file_info_frame.pack(fill='x', pady=10)

        self.file_info_label = HutchisonLabel(
            self.file_info_frame,
            text='Ningún archivo seleccionado',
            label_type='body'
        )
        self.file_info_label.pack(pady=20)

    def select_file(self):
        """Seleccionar archivo Excel"""
        file_path = filedialog.askopenfilename(
            title='Seleccionar archivo Excel',
            filetypes=[
                ('Excel files', '*.xlsx *.xls'),
                ('CSV files', '*.csv'),
                ('All files', '*.*')
            ]
        )

        if file_path:
            self._load_file(file_path)

    def _on_file_drop(self, event):
        """Manejar drag & drop"""
        file_path = event.data.strip('{}')

        if not file_path.lower().endswith(('.xlsx', '.xls', '.csv')):
            messagebox.showerror("Archivo Inválido",
                f"Por favor selecciona un archivo Excel o CSV.\n\n" +
                f"Archivo: {os.path.basename(file_path)}")
            return

        self._load_file(file_path)

    def _load_file(self, file_path):
        """Cargar y procesar archivo"""
        try:
            self.current_file = file_path

            # Leer archivo
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            # Actualizar UI
            for widget in self.file_info_frame.winfo_children():
                widget.destroy()

            info_container = ctk.CTkFrame(self.file_info_frame, fg_color='transparent')
            info_container.pack(fill='both', expand=True, padx=20, pady=20)

            HutchisonLabel(
                info_container,
                text='✓ Archivo Cargado',
                label_type='heading'
            ).configure(text_color=self.theme['secondary'])
            HutchisonLabel(
                info_container,
                text='✓ Archivo Cargado',
                label_type='heading'
            ).pack(pady=(0, 10))

            info_text = f"""
Archivo: {os.path.basename(file_path)}
Registros: {len(df):,}
Columnas: {len(df.columns)}
            """.strip()

            HutchisonLabel(
                info_container,
                text=info_text,
                label_type='body'
            ).pack()

            # Botón procesar
            if self.conn:
                HutchisonButton(
                    info_container,
                    text='⚙️  Procesar Datos',
                    button_type='secondary',
                    command=lambda: self._process_file(df)
                ).pack(pady=(20, 0))
            else:
                HutchisonLabel(
                    info_container,
                    text='\n⚠️ Requiere conexión a BD para procesar',
                    label_type='caption'
                ).configure(text_color='#ff6b6b')
                HutchisonLabel(
                    info_container,
                    text='\n⚠️ Requiere conexión a BD para procesar',
                    label_type='caption'
                ).pack()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivo:\n{str(e)}")

    def _process_file(self, df):
        """Procesar datos del archivo"""
        if not self.conn:
            messagebox.showerror("Error", "Requiere conexión a base de datos")
            return

        try:
            # Procesar con el TranscriptProcessor
            changes = self.processor.process_transcript(df, self.cursor, self.conn)
            self.changes_log = changes

            messagebox.showinfo("Éxito",
                f"Datos procesados correctamente.\n\n" +
                f"Cambios realizados: {len(changes)}")

            # Refrescar dashboard si está visible
            if self.current_panel == 'dashboard':
                self.show_dashboard()

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar:\n{str(e)}")

    # ==================== CONFIGURACIÓN ====================

    def show_configuracion(self):
        """Panel de Configuración con diseño Hutchison"""
        self.clear_content_area()
        self.current_panel = 'configuracion'

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

        # Grid 2x2
        grid_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        grid_frame.pack(fill='both', expand=True)

        grid_frame.grid_columnconfigure((0, 1), weight=1)
        grid_frame.grid_rowconfigure((0, 1), weight=1)

        # Tarjetas
        HutchisonConfigCard(
            grid_frame,
            icon='👥',
            title='Gestionar Usuarios',
            description='Agregar nuevos usuarios o editar información existente',
            button_text='Gestionar',
            button_color=self.theme['primary'],
            command=self.show_user_management
        ).grid(row=0, column=0, padx=15, pady=15, sticky='nsew')

        HutchisonConfigCard(
            grid_frame,
            icon='💾',
            title='Respaldar Base de Datos',
            description='Crear un respaldo de seguridad de la BD',
            button_text='Respaldar',
            button_color=self.theme['secondary'],
            command=self.backup_database
        ).grid(row=0, column=1, padx=15, pady=15, sticky='nsew')

        HutchisonConfigCard(
            grid_frame,
            icon='ℹ️',
            title='Acerca de',
            description='Información sobre Smart Reports v2.0',
            button_text='Ver Info',
            button_color=self.theme['accent_yellow'],
            command=self.show_about
        ).grid(row=1, column=0, padx=15, pady=15, sticky='nsew')

        HutchisonConfigCard(
            grid_frame,
            icon='🔧',
            title='Configuración BD',
            description='Configurar conexión a base de datos',
            button_text='Configurar',
            button_color=self.theme['accent_orange'],
            command=self.show_database_config
        ).grid(row=1, column=1, padx=15, pady=15, sticky='nsew')

    def show_user_management(self):
        """Mostrar gestión de usuarios"""
        if not self.conn:
            messagebox.showerror("Error",
                "Requiere conexión a la base de datos.\n\n" +
                "Configura la conexión en smart_reports/config/settings.py")
            return

        dialog = UserManagementDialog(self.root, self.conn)
        self.root.wait_window(dialog)

        if dialog.result in ['created', 'updated'] and self.current_panel == 'dashboard':
            self.show_dashboard()

    def backup_database(self):
        """Respaldar base de datos"""
        from smart_reports.config.settings import DB_TYPE

        if DB_TYPE == 'sqlserver':
            messagebox.showinfo("Respaldo SQL Server",
                "Para respaldar SQL Server:\n\n" +
                "1. SQL Server Management Studio\n" +
                "2. Click derecho → Tasks → Back Up\n\n" +
                "O ejecuta:\n" +
                "BACKUP DATABASE [nombre] TO DISK = 'ruta.bak'")
        else:
            messagebox.showinfo("Respaldo MySQL",
                "Para respaldar MySQL:\n\n" +
                "mysqldump -u root -p [database] > backup.sql")

    def show_about(self):
        """Mostrar información"""
        messagebox.showinfo("Acerca de",
            "SMART REPORTS V2.0\n" +
            "DISEÑO CORPORATIVO HUTCHISON PORTS\n\n" +
            "Sistema de Gestión de Capacitaciones\n" +
            "Instituto Hutchison Ports\n\n" +
            "© 2025 - Todos los derechos reservados\n\n" +
            "Diseño según Manual de Identidad Visual HP")

    def show_database_config(self):
        """Mostrar configuración de BD"""
        from smart_reports.config.settings import DB_TYPE

        current = "SQL Server" if DB_TYPE == 'sqlserver' else "MySQL"
        status = "✓ Conectado" if self.conn else "✗ Desconectado"

        messagebox.showinfo("Configuración BD",
            f"Base de datos actual: {current}\n" +
            f"Estado: {status}\n\n" +
            "Para cambiar:\n" +
            "1. Edita: smart_reports/config/settings.py\n" +
            "2. Modifica DB_TYPE y configuración\n" +
            "3. Reinicia la aplicación")

    def _show_no_db_message(self, parent, panel_name):
        """Mostrar mensaje cuando no hay BD"""
        message_frame = ctk.CTkFrame(parent, fg_color='transparent')
        message_frame.pack(fill='both', expand=True, pady=50)

        HutchisonLabel(
            message_frame,
            text='⚠️ Sin Conexión a Base de Datos',
            label_type='title'
        ).configure(text_color='#ff6b6b')
        HutchisonLabel(
            message_frame,
            text='⚠️ Sin Conexión a Base de Datos',
            label_type='title'
        ).pack(pady=(0, 20))

        HutchisonLabel(
            message_frame,
            text=f'El panel de {panel_name} requiere conexión a la base de datos.\n\n' +
                 'Configura la conexión en:\n' +
                 'smart_reports/config/settings.py',
            label_type='body'
        ).pack()


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("SMART REPORTS - HUTCHISON PORTS")
    print("Diseño Corporativo v2.0")
    print("="*70 + "\n")

    # Crear root con soporte DnD si está disponible
    if DRAG_DROP_AVAILABLE:
        try:
            root = TkinterDnD.Tk()
            root.configure(bg='#FFFFFF')
        except:
            root = ctk.CTk()
    else:
        root = ctk.CTk()

    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
