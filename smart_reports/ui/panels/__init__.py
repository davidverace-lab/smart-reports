"""
Paneles de la interfaz de usuario
Cada panel representa una pantalla principal de la aplicación
"""
from smart_reports.ui.panels.dashboard import DashboardPanel
from smart_reports.ui.panels.dashboard_ejemplos import DashboardEjemplosPanel
from smart_reports.ui.panels.tng_summary import TNGSummaryPanel
from smart_reports.ui.panels.consultas import ConsultasPanel

__all__ = [
    'DashboardPanel',
    'DashboardEjemplosPanel',
    'TNGSummaryPanel',
    'ConsultasPanel',
]
