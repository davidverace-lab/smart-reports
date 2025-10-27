"""
Widgets personalizados con formas anguladas de Hutchison Ports

Este módulo contiene widgets de CustomTkinter que implementan
las formas gráficas del Dynamic Angle (30.3°) según el manual
de identidad visual de Hutchison Ports.
"""

import customtkinter as ctk
import tkinter as tk
import math
from smart_reports.config.hutchison_identity import (
    HUTCHISON_COLORS,
    DYNAMIC_ANGLE,
    get_hutchison_theme,
    get_font
)


class AngledHeaderFrame(ctk.CTkCanvas):
    """
    Frame con forma de "Sky Shape" - Header angulado a 30.3°
    Se usa para encabezados de paneles.
    """

    def __init__(self, parent, text, height=80, color=None, **kwargs):
        """
        Args:
            parent: Widget padre
            text: Texto del encabezado
            height: Altura del header
            color: Color de fondo (por defecto Ports Sky Blue)
        """
        self.theme = get_hutchison_theme()
        self.bg_color = color or self.theme['primary']
        self.text = text
        self.frame_height = height

        super().__init__(
            parent,
            height=height,
            bg=self.theme['background'],
            highlightthickness=0,
            **kwargs
        )

        # Bind para redibujar cuando cambie el tamaño
        self.bind('<Configure>', self._on_resize)

        # Dibujar forma inicial
        self.after(100, self._draw_angled_shape)

    def _on_resize(self, event=None):
        """Redibujar cuando cambie el tamaño"""
        self._draw_angled_shape()

    def _draw_angled_shape(self):
        """Dibuja la forma angulada (Sky Shape)"""
        self.delete('all')

        width = self.winfo_width()
        height = self.frame_height

        # Calcular offset del ángulo
        angle_rad = math.radians(DYNAMIC_ANGLE)
        offset = height * math.tan(angle_rad)

        # Coordenadas del polígono (trapecio angulado)
        # Esquina superior izquierda -> Superior derecha + offset -> Inferior derecha -> Inferior izquierda
        points = [
            0, 0,                    # Esquina superior izquierda
            width + offset, 0,       # Esquina superior derecha (con offset)
            width, height,           # Esquina inferior derecha
            0, height                # Esquina inferior izquierda
        ]

        # Dibujar forma de fondo
        self.create_polygon(
            points,
            fill=self.bg_color,
            outline='',
            smooth=False
        )

        # Dibujar texto centrado
        font_tuple = get_font('heading', 28, 'bold')
        self.create_text(
            40,  # Padding izquierdo
            height / 2,
            text=self.text,
            font=font_tuple,
            fill=self.theme['text_on_primary'],
            anchor='w'
        )


class AngledDivider(ctk.CTkCanvas):
    """
    Divisor con forma de "Horizon Shape" - Paralelogramo angulado
    Se usa como separador visual entre secciones.
    """

    def __init__(self, parent, height=4, color=None, **kwargs):
        """
        Args:
            parent: Widget padre
            height: Altura del divisor
            color: Color del divisor (por defecto Ports Aqua Green)
        """
        self.theme = get_hutchison_theme()
        self.divider_color = color or self.theme['secondary']
        self.divider_height = height

        super().__init__(
            parent,
            height=height,
            bg=self.theme['background'],
            highlightthickness=0,
            **kwargs
        )

        self.bind('<Configure>', self._on_resize)
        self.after(100, self._draw_divider)

    def _on_resize(self, event=None):
        """Redibujar cuando cambie el tamaño"""
        self._draw_divider()

    def _draw_divider(self):
        """Dibuja el divisor angulado"""
        self.delete('all')

        width = self.winfo_width()
        height = self.divider_height

        # Calcular offset del ángulo
        angle_rad = math.radians(DYNAMIC_ANGLE)
        offset = height * math.tan(angle_rad)

        # Paralelogramo
        points = [
            0, 0,
            width, 0,
            width - offset, height,
            -offset, height
        ]

        self.create_polygon(
            points,
            fill=self.divider_color,
            outline='',
            smooth=False
        )


class AngledCard(ctk.CTkFrame):
    """
    Tarjeta con borde superior angulado (Sea Shape)
    Se usa para tarjetas de contenido, gráficos, etc.
    """

    def __init__(self, parent, title=None, header_color=None, **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título de la tarjeta (opcional)
            header_color: Color del header angulado
        """
        self.theme = get_hutchison_theme()
        self.header_color = header_color or self.theme['primary']
        self.card_title = title

        super().__init__(
            parent,
            fg_color=self.theme['surface'],
            corner_radius=0,
            border_width=1,
            border_color=self.theme['border'],
            **kwargs
        )

        # Container principal
        self.main_container = ctk.CTkFrame(self, fg_color='transparent')
        self.main_container.pack(fill='both', expand=True)

        # Header angulado si hay título
        if self.card_title:
            self.header = AngledHeaderFrame(
                self.main_container,
                text=self.card_title,
                height=60,
                color=self.header_color
            )
            self.header.pack(fill='x', pady=(0, 0))

        # Frame de contenido
        self.content_frame = ctk.CTkFrame(
            self.main_container,
            fg_color='transparent'
        )
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=20)

    def add_content(self, widget):
        """
        Añade un widget al área de contenido de la tarjeta.

        Args:
            widget: Widget a añadir
        """
        widget.pack(in_=self.content_frame, fill='both', expand=True)


class HutchisonButton(ctk.CTkButton):
    """
    Botón corporativo con colores y tipografía de Hutchison Ports
    """

    def __init__(self, parent, text, button_type='primary', **kwargs):
        """
        Args:
            parent: Widget padre
            text: Texto del botón
            button_type: 'primary', 'secondary', 'accent', 'warning'
        """
        self.theme = get_hutchison_theme()

        # Determinar colores según tipo
        color_map = {
            'primary': self.theme['primary'],
            'secondary': self.theme['secondary'],
            'accent': self.theme['accent_yellow'],
            'warning': self.theme['accent_orange'],
        }

        fg_color = color_map.get(button_type, self.theme['primary'])

        # Calcular color hover (más oscuro)
        from smart_reports.config.hutchison_identity import darken_color
        hover_color = darken_color(fg_color, 0.15)

        # Fuente corporativa para botones
        font_tuple = get_font('body', 14, 'bold')

        super().__init__(
            parent,
            text=text,
            font=font_tuple,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=self.theme['text_on_primary'],
            corner_radius=5,
            border_width=0,
            height=45,
            **kwargs
        )


class HutchisonLabel(ctk.CTkLabel):
    """
    Label corporativo con tipografía de Hutchison Ports
    """

    def __init__(self, parent, text, label_type='body', **kwargs):
        """
        Args:
            parent: Widget padre
            text: Texto del label
            label_type: 'title', 'heading', 'body', 'caption'
        """
        self.theme = get_hutchison_theme()

        # Determinar fuente según tipo
        if label_type == 'title':
            font_tuple = get_font('heading', 32, 'bold')
            text_color = self.theme['text']
        elif label_type == 'heading':
            font_tuple = get_font('heading', 20, 'bold')
            text_color = self.theme['text']
        elif label_type == 'body':
            font_tuple = get_font('body', 14, 'normal')
            text_color = self.theme['text']
        elif label_type == 'caption':
            font_tuple = get_font('body', 10, 'normal')
            text_color = self.theme['text_secondary']
        else:
            font_tuple = get_font('body', 14, 'normal')
            text_color = self.theme['text']

        super().__init__(
            parent,
            text=text,
            font=font_tuple,
            text_color=text_color,
            anchor='w',  # Alineado a la izquierda por defecto
            **kwargs
        )


class LogoFrame(ctk.CTkFrame):
    """
    Frame para el logo corporativo de Hutchison Ports
    Debe ir en la esquina superior izquierda
    """

    def __init__(self, parent, **kwargs):
        """
        Args:
            parent: Widget padre
        """
        self.theme = get_hutchison_theme()

        super().__init__(
            parent,
            fg_color='transparent',
            **kwargs
        )

        # Logo text (placeholder - idealmente usar imagen PNG)
        logo_container = ctk.CTkFrame(self, fg_color='transparent')
        logo_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Texto del logo (Montserrat Bold)
        logo_label = HutchisonLabel(
            logo_container,
            text='HUTCHISON PORTS',
            label_type='heading'
        )
        logo_label.configure(
            font=get_font('heading', 18, 'bold'),
            text_color=self.theme['text']
        )
        logo_label.pack(anchor='w')

        # Subtítulo "SMART REPORTS"
        subtitle = HutchisonLabel(
            logo_container,
            text='Smart Reports',
            label_type='caption'
        )
        subtitle.configure(
            font=get_font('body', 11, 'normal'),
            text_color=self.theme['text_secondary']
        )
        subtitle.pack(anchor='w', pady=(2, 0))


class MetricCardAngled(AngledCard):
    """
    Tarjeta métrica con diseño angulado para mostrar KPIs
    """

    def __init__(self, parent, title, value, subtitle=None, color=None, **kwargs):
        """
        Args:
            parent: Widget padre
            title: Título de la métrica
            value: Valor de la métrica
            subtitle: Texto adicional (opcional)
            color: Color del header
        """
        self.theme = get_hutchison_theme()

        super().__init__(
            parent,
            title=title,
            header_color=color or self.theme['primary'],
            **kwargs
        )

        # Valor grande
        value_label = HutchisonLabel(
            self.content_frame,
            text=str(value),
            label_type='title'
        )
        value_label.configure(
            font=get_font('heading', 48, 'bold'),
            text_color=self.theme['primary']
        )
        value_label.pack(anchor='w', pady=(10, 5))

        # Subtítulo si existe
        if subtitle:
            subtitle_label = HutchisonLabel(
                self.content_frame,
                text=subtitle,
                label_type='caption'
            )
            subtitle_label.pack(anchor='w', pady=(0, 10))


# ============================================
# EXPORT
# ============================================

__all__ = [
    'AngledHeaderFrame',
    'AngledDivider',
    'AngledCard',
    'HutchisonButton',
    'HutchisonLabel',
    'LogoFrame',
    'MetricCardAngled',
]
