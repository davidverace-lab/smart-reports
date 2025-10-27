"""
Componente MatplotlibChartCard - Card con gráficos Matplotlib embebidos
"""
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Configuración global de matplotlib para tema oscuro
rcParams['figure.facecolor'] = '#1a1d2e'
rcParams['axes.facecolor'] = '#1a1d2e'
rcParams['axes.edgecolor'] = '#3a3d5c'
rcParams['axes.labelcolor'] = '#a0a0b0'
rcParams['text.color'] = '#a0a0b0'
rcParams['xtick.color'] = '#a0a0b0'
rcParams['ytick.color'] = '#a0a0b0'
rcParams['grid.color'] = '#3a3d5c'
rcParams['grid.alpha'] = 0.3
rcParams['legend.facecolor'] = '#2b2d42'
rcParams['legend.edgecolor'] = '#3a3d5c'


class MatplotlibChartCard(ctk.CTkFrame):
    """Card con gráficos Matplotlib embebidos"""

    def __init__(self, parent, title='', width=500, height=400, **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título del gráfico
            width: Ancho del card
            height: Altura del card
        """
        super().__init__(
            parent,
            fg_color='#2b2d42',
            corner_radius=15,
            border_width=1,
            border_color='#3a3d5c',
            **kwargs
        )

        self.current_fig = None
        self.canvas = None
        self._title = title
        self._width = width
        self._height = height

        # Header si hay título
        if title:
            header = ctk.CTkFrame(self, fg_color='transparent')
            header.pack(fill='x', padx=20, pady=(15, 10))

            title_label = ctk.CTkLabel(
                header,
                text=title,
                font=('Segoe UI', 16, 'bold'),
                text_color='#ffffff',
                anchor='w'
            )
            title_label.pack(side='left', fill='x', expand=True)

        # Container para el gráfico
        self.chart_container = ctk.CTkFrame(self, fg_color='#1a1d2e', corner_radius=10)
        self.chart_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def set_figure(self, fig):
        """
        Establecer figura de Matplotlib

        Args:
            fig: Figura de Matplotlib (matplotlib.figure.Figure)
        """
        # Limpiar contenido anterior
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        self.current_fig = fig

        # Crear canvas de matplotlib
        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        self.canvas.draw()

        # Embebed el canvas en el container
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.configure(bg='#1a1d2e', highlightthickness=0)
        canvas_widget.pack(fill='both', expand=True, padx=5, pady=5)

    def clear(self):
        """Limpiar el gráfico"""
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        if self.current_fig:
            plt.close(self.current_fig)
            self.current_fig = None
