"""
Panel de Dashboard General
Métricas generales del Instituto Hutchison Ports
"""
import customtkinter as ctk
from smart_reports.config.hutchison_identity import get_hutchison_theme, get_font
from smart_reports.ui.components.hutchison_widgets import (
    AngledHeaderFrame,
    AngledDivider,
    AngledCard,
    HutchisonLabel,
    MetricCardAngled
)


class DashboardPanel:
    """Panel de Dashboard con métricas generales"""

    def __init__(self, parent, theme, conn=None, cursor=None):
        """
        Args:
            parent: Widget padre (content_area)
            theme: Tema corporativo Hutchison
            conn: Conexión a base de datos (opcional)
            cursor: Cursor de base de datos (opcional)
        """
        self.parent = parent
        self.theme = theme
        self.conn = conn
        self.cursor = cursor

    def show(self):
        """Mostrar panel de dashboard"""
        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color='transparent'
        )
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

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
