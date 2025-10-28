"""
Configuración Modern - Diseño Oscuro Legacy
Mantiene diseño oscuro pero con tipografía y acentos corporativos Hutchison
"""

# ===================================================================
# PALETA DE COLORES MODERN (Oscuro con acentos Hutchison)
# ===================================================================

PRIMARY_COLORS_MODERN = {
    # Fondos oscuros (mantener diseño legacy)
    'background': '#1a1d2e',
    'surface': '#2b2d42',
    'surface_light': '#3a3d5c',
    'surface_hover': '#4a4d6c',

    # Acentos corporativos Hutchison
    'accent_primary': '#009BDE',    # Sky Blue (botones principales)
    'accent_secondary': '#002E6D',  # Sea Blue (hover)
    'accent_green': '#28A745',      # Success
    'accent_orange': '#FFA500',     # Warning
    'accent_red': '#DC3545',        # Error
    'accent_yellow': '#FFC627',     # Sunray Yellow
    'accent_aqua': '#54BBAB',       # Aqua Green

    # Textos
    'text_primary': '#ffffff',
    'text_secondary': '#a0a0b0',
    'text_disabled': '#606070',

    # Bordes
    'border': '#444654',
    'border_light': '#5a5d7c',
}

# ===================================================================
# TIPOGRAFÍA (usar Hutchison: Montserrat + Arial)
# ===================================================================

FONTS_MODERN = {
    # Títulos y headings (Montserrat)
    'title': ('Montserrat', 28, 'bold'),
    'subtitle': ('Montserrat', 20, 'bold'),
    'heading': ('Montserrat', 16, 'bold'),
    'heading_medium': ('Montserrat', 14, 'bold'),
    'heading_small': ('Montserrat', 12, 'bold'),

    # Cuerpo de texto (Arial)
    'body': ('Arial', 12),
    'body_bold': ('Arial', 12, 'bold'),
    'body_large': ('Arial', 14),
    'small': ('Arial', 10),
    'tiny': ('Arial', 9),
}

# ===================================================================
# CONFIGURACIÓN DE COMPONENTES UI
# ===================================================================

# Botones
BUTTON_CONFIG_MODERN = {
    'primary': {
        'fg_color': PRIMARY_COLORS_MODERN['accent_primary'],  # Sky Blue
        'hover_color': PRIMARY_COLORS_MODERN['accent_secondary'],  # Sea Blue
        'text_color': '#ffffff',
        'font': FONTS_MODERN['heading_medium'],
        'corner_radius': 10,
        'border_width': 0,
    },
    'secondary': {
        'fg_color': PRIMARY_COLORS_MODERN['surface'],
        'hover_color': PRIMARY_COLORS_MODERN['surface_hover'],
        'text_color': PRIMARY_COLORS_MODERN['accent_primary'],
        'font': FONTS_MODERN['heading_medium'],
        'corner_radius': 10,
        'border_width': 1,
        'border_color': PRIMARY_COLORS_MODERN['border'],
    },
    'success': {
        'fg_color': PRIMARY_COLORS_MODERN['accent_green'],
        'hover_color': '#218838',
        'text_color': '#ffffff',
        'font': FONTS_MODERN['heading_medium'],
        'corner_radius': 10,
    },
    'danger': {
        'fg_color': PRIMARY_COLORS_MODERN['accent_red'],
        'hover_color': '#C82333',
        'text_color': '#ffffff',
        'font': FONTS_MODERN['heading_medium'],
        'corner_radius': 10,
    },
    'warning': {
        'fg_color': PRIMARY_COLORS_MODERN['accent_orange'],
        'hover_color': '#E69500',
        'text_color': '#ffffff',
        'font': FONTS_MODERN['heading_medium'],
        'corner_radius': 10,
    },
}

# Entries/Inputs
ENTRY_CONFIG_MODERN = {
    'fg_color': PRIMARY_COLORS_MODERN['surface'],
    'border_color': PRIMARY_COLORS_MODERN['border'],
    'border_width': 1,
    'corner_radius': 8,
    'text_color': PRIMARY_COLORS_MODERN['text_primary'],
    'placeholder_text_color': PRIMARY_COLORS_MODERN['text_secondary'],
    'font': FONTS_MODERN['body'],
}

# Cards/Frames
CARD_CONFIG_MODERN = {
    'fg_color': PRIMARY_COLORS_MODERN['surface'],
    'border_color': PRIMARY_COLORS_MODERN['border'],
    'border_width': 1,
    'corner_radius': 15,
}

# Sidebar
SIDEBAR_CONFIG_MODERN = {
    'fg_color': PRIMARY_COLORS_MODERN['surface'],
    'width': 250,
    'button_height': 50,
    'button_fg_color': 'transparent',
    'button_hover_color': PRIMARY_COLORS_MODERN['surface_hover'],
    'button_active_fg_color': PRIMARY_COLORS_MODERN['accent_primary'],
    'button_active_text_color': '#ffffff',
    'button_text_color': PRIMARY_COLORS_MODERN['text_primary'],
    'button_font': FONTS_MODERN['heading_medium'],
}

# Header
HEADER_CONFIG_MODERN = {
    'fg_color': PRIMARY_COLORS_MODERN['surface'],
    'height': 60,
    'border_color': PRIMARY_COLORS_MODERN['border'],
    'border_width': 1,
    'title_font': FONTS_MODERN['heading'],
    'title_color': PRIMARY_COLORS_MODERN['text_primary'],
}

# ===================================================================
# CONFIGURACIÓN DE BASE DE DATOS (compartida)
# ===================================================================

from smart_reports.config.settings import (
    DB_TYPE,
    SQLSERVER_CONFIG,
    MYSQL_CONFIG,
    DATABASE_CONFIG
)

# ===================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ===================================================================

APP_CONFIG_MODERN = {
    'title': 'SMART REPORTS - INSTITUTO HP (Modern)',
    'version': '2.0 - Modern',
    'geometry': '1400x900',
    'theme': 'dark',
    'appearance_mode': 'dark',
    'company': 'Instituto Hutchison Ports'
}

# ===================================================================
# HELPERS
# ===================================================================

def get_color_modern(color_name: str) -> str:
    """Obtiene un color de la paleta Modern"""
    return PRIMARY_COLORS_MODERN.get(color_name, '#000000')

def get_font_modern(font_name: str, size: int = None, weight: str = None):
    """Obtiene una fuente configurada para Modern"""
    base_font = FONTS_MODERN.get(font_name, FONTS_MODERN['body'])

    if size is None and weight is None:
        return base_font

    family = base_font[0]
    current_size = base_font[1] if len(base_font) > 1 else 12
    current_weight = base_font[2] if len(base_font) > 2 else 'normal'

    final_size = size if size is not None else current_size
    final_weight = weight if weight is not None else current_weight

    return (family, final_size, final_weight)

def get_button_config_modern(button_type: str = 'primary') -> dict:
    """Obtiene configuración de un botón Modern"""
    return BUTTON_CONFIG_MODERN.get(button_type, BUTTON_CONFIG_MODERN['primary']).copy()
