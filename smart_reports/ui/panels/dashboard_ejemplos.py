"""
Panel de Dashboard con Ejemplos de Gráficos Plotly
Visualización de datos con gráficos interactivos
"""
import customtkinter as ctk
from smart_reports.config.identity import get_hutchison_theme, get_font
from smart_reports.ui.components.widgets import (
    AngledCard,
    HutchisonLabel
)


class DashboardEjemplosPanel:
    """Panel con ejemplos de gráficos Plotly"""

    def __init__(self, parent, theme):
        """
        Args:
            parent: Widget padre (tab del dashboard)
            theme: Tema corporativo Hutchison
        """
        self.parent = parent
        self.theme = theme

    def show(self):
        """Mostrar panel con gráficos de ejemplo"""
        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color='transparent'
        )
        scroll_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Título
        title_label = HutchisonLabel(
            scroll_frame,
            text='Gráficos de Ejemplo - Visualización de Datos',
            label_type='heading'
        )
        title_label.configure(font=get_font('heading', 20, 'bold'))
        title_label.pack(pady=(10, 20))

        # Crear 3 gráficos de ejemplo con Plotly
        self._create_example_charts(scroll_frame)

    def _create_example_charts(self, parent):
        """Crear gráficos de ejemplo con Plotly"""
        try:
            import plotly.graph_objects as go
            from tkinterweb import HtmlFrame

            # Card 1: Gráfico de barras
            card1 = AngledCard(
                parent,
                title='Ejemplo 1: Progreso por Módulo',
                header_color=self.theme['primary']
            )
            card1.pack(fill='x', pady=15)

            fig1 = go.Figure(data=[
                go.Bar(
                    x=['Módulo A', 'Módulo B', 'Módulo C', 'Módulo D', 'Módulo E'],
                    y=[45, 78, 62, 91, 53],
                    marker_color=self.theme['primary']
                )
            ])
            fig1.update_layout(
                title='Porcentaje de Completado por Módulo',
                yaxis_title='Porcentaje (%)',
                height=350
            )

            html1 = fig1.to_html(include_plotlyjs='cdn')
            frame1 = HtmlFrame(card1.content_frame, messages_enabled=False)
            frame1.load_html(html1)
            frame1.pack(fill='both', expand=True, padx=10, pady=10)

            # Card 2: Gráfico de líneas
            card2 = AngledCard(
                parent,
                title='Ejemplo 2: Tendencia de Usuarios Activos',
                header_color=self.theme['secondary']
            )
            card2.pack(fill='x', pady=15)

            fig2 = go.Figure(data=[
                go.Scatter(
                    x=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                    y=[120, 145, 138, 167, 189, 201],
                    mode='lines+markers',
                    line=dict(color=self.theme['secondary'], width=3)
                )
            ])
            fig2.update_layout(
                title='Usuarios Activos Mensuales',
                yaxis_title='Usuarios',
                height=350
            )

            html2 = fig2.to_html(include_plotlyjs='cdn')
            frame2 = HtmlFrame(card2.content_frame, messages_enabled=False)
            frame2.load_html(html2)
            frame2.pack(fill='both', expand=True, padx=10, pady=10)

            # Card 3: Gráfico de pie
            card3 = AngledCard(
                parent,
                title='Ejemplo 3: Distribución por Categoría',
                header_color=self.theme['accent_yellow']
            )
            card3.pack(fill='x', pady=15)

            fig3 = go.Figure(data=[
                go.Pie(
                    labels=['Seguridad', 'Operaciones', 'Logística', 'Calidad', 'Administración'],
                    values=[30, 25, 20, 15, 10],
                    marker=dict(colors=[
                        self.theme['primary'],
                        self.theme['secondary'],
                        self.theme['accent_yellow'],
                        self.theme['accent_orange'],
                        self.theme['accent_green']
                    ])
                )
            ])
            fig3.update_layout(title='Usuarios por Categoría', height=350)

            html3 = fig3.to_html(include_plotlyjs='cdn')
            frame3 = HtmlFrame(card3.content_frame, messages_enabled=False)
            frame3.load_html(html3)
            frame3.pack(fill='both', expand=True, padx=10, pady=10)

        except ImportError:
            # Si Plotly o tkinterweb no están disponibles, mostrar mensaje
            error_label = HutchisonLabel(
                parent,
                text=(
                    'Gráficos de Plotly no disponibles.\n\n'
                    'Instala las dependencias:\n'
                    'pip install plotly tkinterweb'
                ),
                label_type='body'
            )
            error_label.configure(text_color='red')
            error_label.pack(pady=50)
        except Exception as e:
            error_label = HutchisonLabel(
                parent,
                text=f'Error al cargar gráficos: {str(e)}',
                label_type='body'
            )
            error_label.configure(text_color='red')
            error_label.pack(pady=50)
