"""
Configuración Hutchison - Diseño Corporativo Claro
Paleta de colores e identidad visual Hutchison Ports
"""

# ===================================================================
# PALETA DE COLORES HUTCHISON PORTS (Diseño Corporativo)
# ===================================================================

PRIMARY_COLORS = {
    # Colores corporativos principales
    'Sky Blue': '#009BDE',        # Azul cielo corporativo (botones principales)
    'Sea Blue': '#002E6D',        # Azul marino corporativo (textos, hover)

    # Fondos
    'White': '#FFFFFF',           # Fondo principal
    'Light Gray': '#F5F5F5',      # Fondo secundario/sidebar
    'Surface': '#FAFAFA',         # Superficie de cards

    # Textos
    'Dark Gray': '#333333',       # Texto principal
    'Medium Gray': '#666666',     # Texto secundario
    'Light Text': '#999999',      # Texto deshabilitado

    # Bordes
    'Border': '#E0E0E0',          # Bordes sutiles
    'Border Dark': '#CCCCCC',     # Bordes más visibles

    # Estados
    'Success Green': '#28A745',   # Verde éxito
    'Warning Orange': '#FFA500',  # Naranja advertencia
    'Error Red': '#DC3545',       # Rojo error
    'Info Blue': '#17A2B8',       # Azul información

    # Acentos adicionales (compatibilidad)
    'Aqua Green': '#54BBAB',      # Verde agua corporativo
    'Sunray Yellow': '#FFC627',   # Amarillo sol corporativo
    'Sunset Orange': '#EE7523',   # Naranja atardecer corporativo
}

# ===================================================================
# TIPOGRAFÍA HUTCHISON (Montserrat + Arial)
# ===================================================================

FONTS_HUTCHISON = {
    # Títulos y headings (Montserrat)
    'title': ('Montserrat', 28, 'bold'),      # Títulos principales
    'subtitle': ('Montserrat', 20, 'bold'),   # Subtítulos
    'heading': ('Montserrat', 16, 'bold'),    # Encabezados sección
    'heading_medium': ('Montserrat', 14, 'bold'),  # Encabezados medianos
    'heading_small': ('Montserrat', 12, 'bold'),   # Encabezados pequeños

    # Cuerpo de texto (Arial)
    'body': ('Arial', 12),                    # Texto normal
    'body_bold': ('Arial', 12, 'bold'),       # Texto destacado
    'body_large': ('Arial', 14),              # Texto grande
    'small': ('Arial', 10),                   # Texto pequeño
    'tiny': ('Arial', 9),                     # Texto muy pequeño
}

# ===================================================================
# CONFIGURACIÓN DE COMPONENTES UI
# ===================================================================

# Botones
BUTTON_CONFIG = {
    'primary': {
        'fg_color': PRIMARY_COLORS['Sky Blue'],
        'hover_color': PRIMARY_COLORS['Sea Blue'],
        'text_color': PRIMARY_COLORS['White'],
        'font': FONTS_HUTCHISON['heading_medium'],
        'corner_radius': 10,
        'border_width': 0,
    },
    'secondary': {
        'fg_color': PRIMARY_COLORS['Light Gray'],
        'hover_color': PRIMARY_COLORS['Border'],
        'text_color': PRIMARY_COLORS['Sea Blue'],
        'font': FONTS_HUTCHISON['heading_medium'],
        'corner_radius': 10,
        'border_width': 1,
        'border_color': PRIMARY_COLORS['Border'],
    },
    'success': {
        'fg_color': PRIMARY_COLORS['Success Green'],
        'hover_color': '#218838',
        'text_color': PRIMARY_COLORS['White'],
        'font': FONTS_HUTCHISON['heading_medium'],
        'corner_radius': 10,
    },
    'danger': {
        'fg_color': PRIMARY_COLORS['Error Red'],
        'hover_color': '#C82333',
        'text_color': PRIMARY_COLORS['White'],
        'font': FONTS_HUTCHISON['heading_medium'],
        'corner_radius': 10,
    },
    'warning': {
        'fg_color': PRIMARY_COLORS['Warning Orange'],
        'hover_color': '#E69500',
        'text_color': PRIMARY_COLORS['White'],
        'font': FONTS_HUTCHISON['heading_medium'],
        'corner_radius': 10,
    },
}

# Entries/Inputs
ENTRY_CONFIG = {
    'fg_color': PRIMARY_COLORS['White'],
    'border_color': PRIMARY_COLORS['Border'],
    'border_width': 1,
    'corner_radius': 8,
    'text_color': PRIMARY_COLORS['Dark Gray'],
    'placeholder_text_color': PRIMARY_COLORS['Medium Gray'],
    'font': FONTS_HUTCHISON['body'],
}

# Cards/Frames
CARD_CONFIG = {
    'fg_color': PRIMARY_COLORS['White'],
    'border_color': PRIMARY_COLORS['Border'],
    'border_width': 1,
    'corner_radius': 15,
}

# Sidebar
SIDEBAR_CONFIG = {
    'fg_color': PRIMARY_COLORS['Light Gray'],
    'width': 250,
    'button_height': 50,
    'button_fg_color': 'transparent',
    'button_hover_color': '#E8F4FA',  # Azul muy claro
    'button_active_fg_color': PRIMARY_COLORS['Sky Blue'],
    'button_active_text_color': PRIMARY_COLORS['White'],
    'button_text_color': PRIMARY_COLORS['Sea Blue'],
    'button_font': FONTS_HUTCHISON['heading_medium'],
}

# Header
HEADER_CONFIG = {
    'fg_color': PRIMARY_COLORS['White'],
    'height': 60,
    'border_color': PRIMARY_COLORS['Border'],
    'border_width': 1,
    'title_font': FONTS_HUTCHISON['heading'],
    'title_color': PRIMARY_COLORS['Sea Blue'],
}

# ===================================================================
# CONFIGURACIÓN DE BASE DE DATOS (compartida)
# ===================================================================

# Usar la configuración existente
from smart_reports.config.settings import (
    DB_TYPE,
    SQLSERVER_CONFIG,
    MYSQL_CONFIG,
    DATABASE_CONFIG
)

# ===================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ===================================================================

APP_CONFIG = {
    'title': 'SMART REPORTS - INSTITUTO HUTCHISON PORTS',
    'version': '2.0 - Hutchison',
    'geometry': '1400x900',
    'theme': 'light',
    'appearance_mode': 'light',
    'company': 'Instituto Hutchison Ports'
}

# ===================================================================
# HELPERS
# ===================================================================

def get_color(color_name: str) -> str:
    """
    Obtiene un color de la paleta

    Args:
        color_name: Nombre del color

    Returns:
        Código hexadecimal del color
    """
    return PRIMARY_COLORS.get(color_name, '#000000')

def get_font(font_name: str, size: int = None, weight: str = None):
    """
    Obtiene una fuente configurada

    Args:
        font_name: Nombre de la fuente base
        size: Tamaño personalizado (opcional)
        weight: Peso personalizado (opcional)

    Returns:
        Tupla de configuración de fuente
    """
    base_font = FONTS_HUTCHISON.get(font_name, FONTS_HUTCHISON['body'])

    if size is None and weight is None:
        return base_font

    family = base_font[0]
    current_size = base_font[1] if len(base_font) > 1 else 12
    current_weight = base_font[2] if len(base_font) > 2 else 'normal'

    final_size = size if size is not None else current_size
    final_weight = weight if weight is not None else current_weight

    return (family, final_size, final_weight)

def get_button_config(button_type: str = 'primary') -> dict:
    """
    Obtiene configuración de un botón

    Args:
        button_type: Tipo de botón (primary, secondary, success, danger, warning)

    Returns:
        Diccionario de configuración
    """
    return BUTTON_CONFIG.get(button_type, BUTTON_CONFIG['primary']).copy()
