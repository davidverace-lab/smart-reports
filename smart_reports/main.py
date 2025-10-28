"""
SMART REPORTS - INSTITUTO HUTCHISON PORTS
Punto de entrada principal
Versión 2.0 - Diseño Corporativo
"""

import sys
import os

# Agregar el directorio padre al path para imports absolutos
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk

# Intentar importar TkinterDnD para drag & drop
try:
    from tkinterdnd2 import TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    DRAG_DROP_AVAILABLE = False
    print("⚠️  tkinterdnd2 no disponible. Drag & drop deshabilitado.")

from smart_reports.ui.main_window_hutchison import MainWindow


def main():
    """Función principal de la aplicación - Diseño Corporativo Hutchison Ports"""
    print("\n" + "="*70)
    print("SMART REPORTS - HUTCHISON PORTS")
    print("Sistema de Gestión de Capacitaciones")
    print("Versión 2.0 - Diseño Corporativo")
    print("="*70)
    print("\n✓ Diseño según Manual de Identidad Visual Hutchison Ports")
    print("✓ Paleta corporativa: Sky Blue, Sea Blue, Aqua Green, etc.")
    print("✓ Tipografía: Montserrat (títulos) + Arial (cuerpo)")
    print("✓ Formas anguladas: Dynamic Angle 30.3°")
    print("\n" + "="*70 + "\n")

    # Configurar apariencia (tema claro para Hutchison)
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Crear root con soporte DnD si está disponible
    if DRAG_DROP_AVAILABLE:
        try:
            root = TkinterDnD.Tk()
            root.configure(bg='#FFFFFF')
            root.title("SMART REPORTS - HUTCHISON PORTS")
            root.geometry("1400x900")
        except Exception as e:
            print(f"⚠️  Error al inicializar TkinterDnD: {e}")
            print("   Usando CTk normal...")
            root = ctk.CTk()
    else:
        root = ctk.CTk()

    # Crear aplicación
    app = MainWindow(root)

    # Iniciar loop
    root.mainloop()


if __name__ == "__main__":
    main()
