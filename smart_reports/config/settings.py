"""
Configuración global del sistema Smart Reports
"""

# ============================================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================================

# Tipo de base de datos: 'sqlserver' o 'mysql'
DB_TYPE = 'mysql'  # Cambiar a 'sqlserver' para usar base de datos del trabajo

# Configuración SQL Server (Trabajo)
SQLSERVER_CONFIG = {
    'server': '10.133.18.111',
    'database': 'TNGCORE',
    'username': 'tngdatauser',
    'password': 'Password1',
    'driver': 'ODBC Driver 17 for SQL Server'
}

# Configuración MySQL (Casa)
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'tngcore',
    'user': 'root',
    'password': 'Xbox360xd'
}

# Configuración activa (se establece según DB_TYPE)
DATABASE_CONFIG = SQLSERVER_CONFIG if DB_TYPE == 'sqlserver' else MYSQL_CONFIG

# ============================================
# PALETAS DE COLORES
# ============================================

# Paleta Oscura (Tema por defecto)
DARK_THEME = {
    'background': '#1a1d2e',
    'surface': '#2b2d42',
    'surface_light': '#3a3d5a',
    'primary': '#6B5B95',
    'secondary': '#88B0D3',
    'success': '#82B366',
    'warning': '#FEB236',
    'danger': '#FF6361',
    'text': '#ffffff',
    'text_secondary': '#a0a0a0',
    'border': '#444654',
    'edited': '#FFF59D'
}

# Paleta Clara
LIGHT_THEME = {
    'background': '#f5f5f5',
    'surface': '#ffffff',
    'surface_light': '#fafafa',
    'primary': '#6B5B95',
    'secondary': '#88B0D3',
    'success': '#82B366',
    'warning': '#FEB236',
    'danger': '#FF6361',
    'text': '#000000',
    'text_secondary': '#666666',
    'border': '#e0e0e0',
    'edited': '#FFF59D'
}

# Colores corporativos (Compatibilidad con código existente)
COLORS = {
    'primary': '#6B5B95',      # Morado principal
    'secondary': '#88B0D3',    # Azul secundario
    'success': '#82B366',      # Verde
    'warning': '#FEB236',      # Naranja
    'danger': '#FF6361',       # Rojo
    'dark': '#4A4A4A',         # Gris oscuro
    'light': '#F7F7F7',        # Gris claro
    'edited': '#FFF59D'        # Amarillo para celdas editadas
}

# Configuración de la aplicación
APP_CONFIG = {
    'title': 'SMART REPORTS - INSTITUTO HP',
    'version': '2.0',
    'geometry': '1400x800',
    'theme': 'darkly',
    'company': 'Instituto Hutchison Ports'
}

# Rutas de archivos
PATHS = {
    'logo': 'assets/logo.png',
    'reports': 'reports/',
    'logs': 'logs/',
    'backups': 'backups/'
}

# Estados de módulos
MODULE_STATUSES = ['Completado', 'En proceso', 'Registrado', 'No iniciado']

# Configuración de PDFs
PDF_CONFIG = {
    'page_size': 'letter',
    'title_font_size': 24,
    'subtitle_font_size': 16,
    'normal_font_size': 10,
    'logo_width': 2,  # inches
    'logo_height': 0.8  # inches
}
