"""
SMART REPORTS - INSTITUTO HUTCHISON PORTS
Punto de entrada principal - VERSIÓN MODERNA
Versión 2.0
"""

import sys
import os

# Agregar el directorio padre al path para imports absolutos
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from smart_reports.ui.main_window_modern import MainWindow

# Intentar importar TkinterDnD para soporte de drag & drop
try:
    from tkinterdnd2 import TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    DRAG_DROP_AVAILABLE = False
    print("Warning: tkinterdnd2 no disponible. Drag & drop deshabilitado.")


def main():
    """Función principal de la aplicación - Versión Moderna"""
    # Configurar CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Crear ventana principal con soporte para drag & drop si está disponible
    if DRAG_DROP_AVAILABLE:
        # Crear root con soporte de TkinterDnD
        root = TkinterDnD.Tk()
        # Aplicar estilos de CustomTkinter manualmente
        root.configure(bg='#1a1d2e')
        root.title("SMART REPORTS - INSTITUTO HUTCHISON PORTS")
        root.geometry("1400x900")
    else:
        # Fallback a CTk normal si TkinterDnD no está disponible
        root = ctk.CTk()

    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
