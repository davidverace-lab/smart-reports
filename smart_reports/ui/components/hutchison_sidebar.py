"""
Sidebar Corporativo Hutchison Ports
Sidebar con identidad visual de Hutchison Ports (Sea Blue con texto blanco)
"""

import customtkinter as ctk
from tkinter import messagebox
from smart_reports.config.hutchison_identity import (
    HUTCHISON_COLORS,
    get_hutchison_theme,
    get_font
)
from smart_reports.ui.components.hutchison_widgets import HutchisonLabel


class HutchisonSidebar(ctk.CTkFrame):
    """
    Sidebar corporativo con colores y tipografía de Hutchison Ports
    Fondo: Ports Sea Blue (#002E6D)
    Texto: Blanco
    """

    def __init__(self, parent, navigation_callbacks, **kwargs):
        """
        Args:
            parent: Widget padre
            navigation_callbacks: Dict con {nombre: callback_function}
        """
        self.theme = get_hutchison_theme()
        self.navigation_callbacks = navigation_callbacks
        self.nav_buttons = []
        self.active_button = None
        self.dropdown_menu = None  # Menú desplegable TNG

        # Sidebar con fondo Sea Blue
        super().__init__(
            parent,
            width=240,
            fg_color=self.theme['sidebar_bg'],
            corner_radius=0,
            **kwargs
        )

        # Logo/Header
        self._create_header()

        # Navegación
        self._create_navigation()

        # Footer con versión
        self._create_footer()

    def _create_header(self):
        """Crear header con logo corporativo"""
        logo_frame = ctk.CTkFrame(
            self,
            fg_color='transparent',
            height=120
        )
        logo_frame.pack(fill='x', padx=20, pady=(25, 20))
        logo_frame.pack_propagate(False)

        # Logo "HUTCHISON PORTS" (usando Montserrat Bold)
        logo_label = ctk.CTkLabel(
            logo_frame,
            text='HUTCHISON\nPORTS',
            font=get_font('heading', 20, 'bold'),
            text_color=self.theme['sidebar_text'],
            justify='left',
            anchor='w'
        )
        logo_label.pack(anchor='w', pady=(5, 8))

        # Subtítulo "Smart Reports"
        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text='Smart Reports',
            font=get_font('body', 12, 'normal'),
            text_color=self.theme['sidebar_text_secondary'],
            justify='left',
            anchor='w'
        )
        subtitle_label.pack(anchor='w')

        # Línea separadora (Sky Blue clara)
        separator = ctk.CTkFrame(
            self,
            height=2,
            fg_color=self.theme['primary']
        )
        separator.pack(fill='x', padx=20, pady=(0, 20))

    def _create_navigation(self):
        """Crear botones de navegación"""
        nav_items = [
            ('📊', 'Dashboard', 'dashboard'),
            ('🔍', 'Consultas', 'consultas'),
            ('📤', 'Actualizar Datos', 'actualizar'),
            ('⚙️', 'Configuración', 'configuracion'),
        ]

        for icon, text, key in nav_items:
            if key in self.navigation_callbacks:
                btn = ctk.CTkButton(
                    self,
                    text=f'{icon}  {text}',
                    font=get_font('body', 14, 'normal'),
                    fg_color='transparent',
                    text_color=self.theme['sidebar_text_secondary'],
                    hover_color=self.theme['sidebar_hover'],
                    anchor='w',
                    height=55,
                    corner_radius=8,
                    command=lambda k=key: self._on_nav_click(k)
                )
                btn.pack(fill='x', padx=12, pady=4)
                self.nav_buttons.append((key, btn))

        # Separador visual antes de Reportes TNG
        separator_tng = ctk.CTkFrame(
            self,
            height=2,
            fg_color=self.theme['primary']
        )
        separator_tng.pack(fill='x', padx=20, pady=15)

        # Botón de Reportes Gerenciales TNG (con menú desplegable)
        self.tng_reports_btn = ctk.CTkButton(
            self,
            text='📄  Reportes Gerenciales TNG',
            font=get_font('body', 14, 'bold'),
            fg_color='transparent',
            text_color=self.theme['sidebar_text'],
            hover_color=self.theme['sidebar_hover'],
            anchor='w',
            height=55,
            corner_radius=8,
            command=self._toggle_report_menu,
            cursor='hand2'
        )
        self.tng_reports_btn.pack(fill='x', padx=12, pady=4)

    def _create_footer(self):
        """Crear footer con información de versión"""
        # Spacer para empujar footer al fondo
        spacer = ctk.CTkFrame(self, fg_color='transparent')
        spacer.pack(fill='both', expand=True)

        # Línea separadora superior
        separator_top = ctk.CTkFrame(
            self,
            height=2,
            fg_color=self.theme['primary']
        )
        separator_top.pack(fill='x', padx=20, pady=(10, 15))

        # Footer
        footer = ctk.CTkFrame(
            self,
            fg_color='transparent',
            height=70
        )
        footer.pack(side='bottom', fill='x', padx=20, pady=(0, 20))
        footer.pack_propagate(False)

        # Versión
        version_label = ctk.CTkLabel(
            footer,
            text='Versión 2.0',
            font=get_font('body', 10, 'bold'),
            text_color=self.theme['sidebar_text']
        )
        version_label.pack(anchor='w', pady=(5, 2))

        # Copyright
        copyright_label = ctk.CTkLabel(
            footer,
            text='© 2025 Hutchison Ports',
            font=get_font('body', 9, 'normal'),
            text_color=self.theme['sidebar_text_secondary']
        )
        copyright_label.pack(anchor='w')

        # Marca
        brand_label = ctk.CTkLabel(
            footer,
            text='Instituto HP',
            font=get_font('body', 9, 'normal'),
            text_color=self.theme['sidebar_text_secondary']
        )
        brand_label.pack(anchor='w')

    def _on_nav_click(self, key):
        """Manejar click en navegación"""
        # Actualizar estilos de botones
        for btn_key, btn in self.nav_buttons:
            if btn_key == key:
                # Botón activo: fondo más claro y texto blanco
                btn.configure(
                    fg_color=self.theme['sidebar_hover'],
                    text_color=self.theme['sidebar_text']
                )
                self.active_button = btn
            else:
                # Botón inactivo: transparente con texto gris claro
                btn.configure(
                    fg_color='transparent',
                    text_color=self.theme['sidebar_text_secondary']
                )

        # Ejecutar callback
        if key in self.navigation_callbacks:
            self.navigation_callbacks[key]()

    def set_active(self, key):
        """Establecer botón activo programáticamente"""
        self._on_nav_click(key)

    def _toggle_report_menu(self):
        """Mostrar/ocultar menú desplegable de reportes TNG"""
        if self.dropdown_menu and self.dropdown_menu.winfo_exists():
            # Si ya existe, ocultarlo
            self.dropdown_menu.destroy()
            self.dropdown_menu = None
        else:
            # Crear y mostrar menú
            self._show_report_menu()

    def _show_report_menu(self):
        """Crear y mostrar menú desplegable de reportes TNG"""
        # Obtener posición del botón TNG
        btn_x = self.tng_reports_btn.winfo_rootx()
        btn_y = self.tng_reports_btn.winfo_rooty()
        btn_height = self.tng_reports_btn.winfo_height()

        # Crear ventana toplevel para el menú
        self.dropdown_menu = ctk.CTkToplevel(self)
        self.dropdown_menu.overrideredirect(True)  # Sin borde de ventana
        self.dropdown_menu.attributes('-topmost', True)

        # Posicionar junto al botón
        menu_x = btn_x + self.winfo_width() + 5
        menu_y = btn_y
        self.dropdown_menu.geometry(f'320x180+{menu_x}+{menu_y}')

        # Frame del menú con borde
        menu_frame = ctk.CTkFrame(
            self.dropdown_menu,
            fg_color=self.theme['surface'],
            corner_radius=10,
            border_width=2,
            border_color=self.theme['primary']
        )
        menu_frame.pack(fill='both', expand=True, padx=2, pady=2)

        # Título del menú
        title_label = ctk.CTkLabel(
            menu_frame,
            text='Reportes Gerenciales TNG',
            font=get_font('heading', 14, 'bold'),
            text_color=self.theme['text'],
            anchor='w'
        )
        title_label.pack(fill='x', padx=15, pady=(12, 8))

        # Opciones del menú
        menu_options = [
            ('📊', 'Generar Resumen Semanal TNG (PDF)', self._generate_weekly_report),
            ('⚠️', 'Generar Reporte de Módulos Críticos TNG (PDF)', self._generate_critical_modules_report),
            ('📁', 'Ver Historial de Reportes TNG', self._view_reports_history),
        ]

        for icon, text, command in menu_options:
            btn = ctk.CTkButton(
                menu_frame,
                text=f'{icon}  {text}',
                font=get_font('body', 12, 'normal'),
                fg_color='transparent',
                text_color=self.theme['text'],
                hover_color=self.theme['primary'],
                anchor='w',
                height=40,
                corner_radius=6,
                command=lambda cmd=command: self._execute_menu_option(cmd),
                cursor='hand2'
            )
            btn.pack(fill='x', padx=8, pady=2)

        # Bind para cerrar al hacer clic fuera
        self.dropdown_menu.bind('<FocusOut>', lambda e: self._close_menu())

        # Dar foco al menú para detectar cuando se pierde
        self.dropdown_menu.focus_set()

    def _close_menu(self):
        """Cerrar menú desplegable"""
        if self.dropdown_menu and self.dropdown_menu.winfo_exists():
            self.dropdown_menu.destroy()
            self.dropdown_menu = None

    def _execute_menu_option(self, command):
        """Ejecutar opción del menú y cerrar"""
        self._close_menu()
        command()

    def _generate_weekly_report(self):
        """Generar resumen semanal TNG (placeholder)"""
        messagebox.showinfo(
            "Generando Resumen Semanal TNG",
            "Generando Resumen Semanal TNG (PDF)...\n\n" +
            "Esta funcionalidad incluirá:\n" +
            "• Métricas de la semana\n" +
            "• Comparación con semana anterior\n" +
            "• Tendencias de finalización\n" +
            "• Empleados destacados\n\n" +
            "📄 El PDF se generará en la carpeta 'reportes/'"
        )

    def _generate_critical_modules_report(self):
        """Generar reporte de módulos críticos TNG (placeholder)"""
        messagebox.showinfo(
            "Generando Reporte de Módulos Críticos TNG",
            "Generando Reporte de Módulos Críticos TNG (PDF)...\n\n" +
            "Esta funcionalidad incluirá:\n" +
            "• Estado de módulos críticos\n" +
            "• Empleados con progreso bajo\n" +
            "• Alertas de cumplimiento\n" +
            "• Recomendaciones de acción\n\n" +
            "📄 El PDF se generará en la carpeta 'reportes/'"
        )

    def _view_reports_history(self):
        """Ver historial de reportes TNG (placeholder)"""
        messagebox.showinfo(
            "Historial de Reportes TNG",
            "Ver Historial de Reportes TNG...\n\n" +
            "Esta funcionalidad mostrará:\n" +
            "• Lista de reportes generados\n" +
            "• Fecha y tipo de reporte\n" +
            "• Botón para abrir PDF\n" +
            "• Opción de eliminar reportes antiguos\n\n" +
            "📁 Los reportes se guardan en 'reportes/'"
        )


__all__ = ['HutchisonSidebar']
