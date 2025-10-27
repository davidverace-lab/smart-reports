"""
UI Components package - Componentes reutilizables de la interfaz moderna
"""
from smart_reports.ui.components.metric_card import MetricCard
from smart_reports.ui.components.chart_card import ChartCard
from smart_reports.ui.components.modern_sidebar import ModernSidebar
from smart_reports.ui.components.config_card import ConfigCard

# Componentes corporativos Hutchison Ports
from smart_reports.ui.components.hutchison_widgets import (
    AngledHeaderFrame,
    AngledDivider,
    AngledCard,
    HutchisonButton,
    HutchisonLabel,
    LogoFrame,
    MetricCardAngled
)
from smart_reports.ui.components.hutchison_sidebar import HutchisonSidebar
from smart_reports.ui.components.hutchison_config_card import HutchisonConfigCard

__all__ = [
    'MetricCard',
    'ChartCard',
    'ModernSidebar',
    'ConfigCard',
    # Hutchison Ports
    'AngledHeaderFrame',
    'AngledDivider',
    'AngledCard',
    'HutchisonButton',
    'HutchisonLabel',
    'LogoFrame',
    'MetricCardAngled',
    'HutchisonSidebar',
    'HutchisonConfigCard',
]
