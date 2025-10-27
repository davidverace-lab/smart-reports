"""
Identidad Corporativa Hutchison Ports
Basado en el Manual de Identidad Visual

Este módulo define los colores, tipografías y constantes de diseño
según el manual de identidad de Hutchison Ports.
"""

# ============================================
# PALETA DE COLORES CORPORATIVA
# Manual de Identidad - Página 20
# ============================================

HUTCHISON_COLORS = {
    # Color Principal
    'ports_sky_blue': '#009BDE',        # Ports Sky Blue - Color primario de marca

    # Colores Secundarios
    'ports_aqua_green': '#54BBAB',      # Ports Aqua Green
    'ports_sunray_yellow': '#FFC627',   # Ports Sunray Yellow
    'ports_sunset_orange': '#EE7523',   # Ports Sunset Orange

    # Color de Texto Principal
    'ports_sea_blue': '#002E6D',        # Ports Sea Blue - Texto sobre fondos claros

    # Colores Neutros
    'white': '#FFFFFF',                 # Blanco - Fondos principales
    'light_gray': '#F5F5F5',            # Gris muy claro - Fondos alternativos
    'medium_gray': '#E0E0E0',           # Gris medio - Bordes y divisores
    'dark_gray': '#666666',             # Gris oscuro - Texto secundario
    'black': '#000000',                 # Negro - Uso limitado
}

# ============================================
# TIPOGRAFÍA CORPORATIVA
# Manual de Identidad - Páginas 40-42
# ============================================

HUTCHISON_FONTS = {
    # Tipografía Web/Multimedia
    'heading_family': 'Montserrat',     # Para títulos y encabezados
    'heading_bold': ('Montserrat', 'Bold'),
    'heading_regular': ('Montserrat', 'Regular'),

    # Tipografía Default (Sistemas Informáticos)
    'body_family': 'Arial',             # Para texto de cuerpo y párrafos
    'body_regular': ('Arial', 'Regular'),
    'body_bold': ('Arial', 'Bold'),
}

# Tamaños de fuente recomendados (en puntos)
FONT_SIZES = {
    'title_large': 32,      # Títulos principales de panel
    'title_medium': 24,     # Subtítulos
    'title_small': 20,      # Títulos de tarjetas
    'heading': 16,          # Encabezados de secciones
    'body_large': 14,       # Texto normal grande
    'body': 12,             # Texto normal
    'body_small': 10,       # Texto pequeño
    'caption': 9,           # Notas al pie, metadata
}

# ============================================
# DYNAMIC ANGLE
# Manual de Identidad - Formas Gráficas
# ============================================

DYNAMIC_ANGLE = 30.3  # Grados - El ángulo característico de la marca

# ============================================
# TEMA CUSTOMTKINTER - HUTCHISON PORTS
# ============================================

def get_hutchison_theme():
    """
    Retorna un diccionario con el tema completo de Hutchison Ports
    para aplicar a CustomTkinter.

    Returns:
        dict: Tema con colores y configuraciones
    """
    return {
        # Fondos
        'background': HUTCHISON_COLORS['white'],
        'surface': HUTCHISON_COLORS['white'],
        'surface_light': HUTCHISON_COLORS['light_gray'],

        # Colores de acento
        'primary': HUTCHISON_COLORS['ports_sky_blue'],
        'secondary': HUTCHISON_COLORS['ports_aqua_green'],
        'accent_yellow': HUTCHISON_COLORS['ports_sunray_yellow'],
        'accent_orange': HUTCHISON_COLORS['ports_sunset_orange'],

        # Texto
        'text': HUTCHISON_COLORS['ports_sea_blue'],
        'text_secondary': HUTCHISON_COLORS['dark_gray'],
        'text_on_primary': HUTCHISON_COLORS['white'],

        # Bordes y divisores
        'border': HUTCHISON_COLORS['medium_gray'],
        'divider': HUTCHISON_COLORS['light_gray'],

        # Estados
        'hover': '#0088C5',  # Sky Blue más oscuro
        'active': HUTCHISON_COLORS['ports_sky_blue'],
        'disabled': HUTCHISON_COLORS['medium_gray'],

        # Sidebar especial (versión invertida con Sea Blue)
        'sidebar_bg': HUTCHISON_COLORS['ports_sea_blue'],
        'sidebar_text': HUTCHISON_COLORS['white'],
        'sidebar_text_secondary': '#A0B0C0',  # Azul claro para texto secundario
        'sidebar_hover': '#003D8F',  # Sea Blue más claro
    }

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def get_color(color_name):
    """
    Obtiene un color de la paleta corporativa.

    Args:
        color_name (str): Nombre del color (ej: 'ports_sky_blue')

    Returns:
        str: Código hexadecimal del color
    """
    return HUTCHISON_COLORS.get(color_name, HUTCHISON_COLORS['ports_sea_blue'])

def get_font(font_type, size=None, weight='normal'):
    """
    Obtiene una tupla de fuente corporativa.

    Args:
        font_type (str): 'heading' o 'body'
        size (int, optional): Tamaño en puntos
        weight (str, optional): 'normal', 'bold', 'italic', o 'bold italic'

    Returns:
        tuple: (family, size, weight) para CustomTkinter
    """
    if font_type == 'heading':
        family = HUTCHISON_FONTS['heading_family']
    else:
        family = HUTCHISON_FONTS['body_family']

    if size is None:
        size = FONT_SIZES['body']

    # Convertir 'regular' a 'normal' si se pasa (Tkinter usa 'normal')
    if weight == 'regular':
        weight = 'normal'

    return (family, size, weight)

def hex_to_rgb(hex_color):
    """
    Convierte color hexadecimal a tupla RGB.

    Args:
        hex_color (str): Color en formato hex (#RRGGBB)

    Returns:
        tuple: (R, G, B) en rango 0-255
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    """
    Convierte RGB a hexadecimal.

    Args:
        r, g, b (int): Valores RGB en rango 0-255

    Returns:
        str: Color en formato hex (#RRGGBB)
    """
    return f'#{r:02x}{g:02x}{b:02x}'

def lighten_color(hex_color, factor=0.2):
    """
    Aclara un color mezclándolo con blanco.

    Args:
        hex_color (str): Color en formato hex
        factor (float): Factor de aclarado (0-1)

    Returns:
        str: Color aclarado en formato hex
    """
    r, g, b = hex_to_rgb(hex_color)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return rgb_to_hex(r, g, b)

def darken_color(hex_color, factor=0.2):
    """
    Oscurece un color.

    Args:
        hex_color (str): Color en formato hex
        factor (float): Factor de oscurecimiento (0-1)

    Returns:
        str: Color oscurecido en formato hex
    """
    r, g, b = hex_to_rgb(hex_color)
    r = int(r * (1 - factor))
    g = int(g * (1 - factor))
    b = int(b * (1 - factor))
    return rgb_to_hex(r, g, b)

# ============================================
# EXPORT
# ============================================

__all__ = [
    'HUTCHISON_COLORS',
    'HUTCHISON_FONTS',
    'FONT_SIZES',
    'DYNAMIC_ANGLE',
    'get_hutchison_theme',
    'get_color',
    'get_font',
    'hex_to_rgb',
    'rgb_to_hex',
    'lighten_color',
    'darken_color',
]
