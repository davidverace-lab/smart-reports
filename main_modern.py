"""
═══════════════════════════════════════════════════════════════
SMART REPORTS - INSTITUTO HUTCHISON PORTS
Versión Modern - Diseño Oscuro Legacy con Tipografía Corporativa
═══════════════════════════════════════════════════════════════

Punto de entrada principal para la versión con diseño oscuro
(mantiene diseño oscuro legacy pero con tipografía y colores corporativos)

Características:
- Diseño oscuro elegante
- Tipografía corporativa: Montserrat + Arial
- Botones con colores corporativos (Sky Blue)
- Login funcional: admin / 1234
- Dashboard con tabs mejoradas
- Consultas con tksheet modo oscuro
- Cruce de datos con Drag & Drop
- Configuración con cards funcionales

Uso:
    python main_modern.py

═══════════════════════════════════════════════════════════════
"""

import sys
import os

# Agregar el directorio al path para imports absolutos
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import customtkinter as ctk

# Intentar importar TkinterDnD para drag & drop
try:
    from tkinterdnd2 import TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    print("⚠️  tkinterdnd2 no disponible. Drag & drop deshabilitado.")

from smart_reports.config.settings_modern import APP_CONFIG_MODERN
from smart_reports.ui.modern.login_modern import LoginModern
from smart_reports.ui.modern.main_window_modern import MainWindowModern


class ApplicationModern:
    """
    Aplicación principal Modern (diseño oscuro)

    Flujo:
    1. Mostrar Login
    2. Al login exitoso, mostrar MainWindow
    3. MainWindow carga paneles dinámicamente
    """

    def __init__(self, root):
        """
        Args:
            root: Ventana raíz (CTk o TkinterDnD.Tk)
        """
        self.root = root
        self.root.title(APP_CONFIG_MODERN['title'])

        # Configurar ventana MAXIMIZADA
        self._maximize_window()

        self.current_user = None
        self.main_window = None

        # Mostrar login primero
        self._show_login()

    def _maximize_window(self):
        """Maximizar ventana en diferentes OS"""
        try:
            # Intentar maximizar según OS
            if sys.platform.startswith('win'):
                # Windows
                self.root.state('zoomed')
            else:
                # Linux / macOS
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        except:
            # Fallback
            self.root.geometry("1400x900")
            # Centrar
            self.root.update_idletasks()
            x = (self.root.winfo_screenwidth() // 2) - 700
            y = (self.root.winfo_screenheight() // 2) - 450
            self.root.geometry(f"1400x900+{x}+{y}")

    def _show_login(self):
        """Mostrar pantalla de login"""
        self.login_window = LoginModern(self.root, self._on_login_success)
        self.login_window.pack(fill='both', expand=True)

    def _on_login_success(self, username):
        """
        Callback cuando el login es exitoso

        Args:
            username: Nombre del usuario que hizo login
        """
        self.current_user = username
        print(f"✓ Login exitoso: {username}")

        # Crear y mostrar ventana principal
        self.main_window = MainWindowModern(self.root, username)


def main():
    """Función principal de la aplicación"""

    # Banner de inicio
    print("\n" + "=" * 70)
    print("SMART REPORTS - HUTCHISON PORTS")
    print("Sistema de Gestión de Capacitaciones")
    print("Versión 2.0 - Modern (Diseño Oscuro)")
    print("=" * 70)
    print("\n✓ Diseño oscuro elegante con tipografía corporativa")
    print("✓ Paleta oscura: #1a1d2e (bg), #2b2d42 (surface)")
    print("✓ Botones corporativos: Sky Blue (#009BDE)")
    print("✓ Tipografía: Montserrat (títulos) + Arial (cuerpo)")
    print("✓ Login demo: usuario=admin, contraseña=1234")
    print("\n" + "=" * 70 + "\n")

    # Configurar apariencia (tema oscuro para Modern)
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Crear root con soporte DnD si está disponible
    if DND_AVAILABLE:
        try:
            root = TkinterDnD.Tk()
            root.configure(bg='#1a1d2e')
            print("✓ TkinterDnD inicializado - Drag & Drop habilitado")
        except Exception as e:
            print(f"⚠️  Error al inicializar TkinterDnD: {e}")
            print("   Usando CTk normal...")
            root = ctk.CTk()
    else:
        root = ctk.CTk()

    # Crear aplicación con login
    app = ApplicationModern(root)

    # Iniciar loop
    print("\n🚀 Aplicación iniciada - Mostrando ventana de login...\n")
    root.mainloop()


if __name__ == "__main__":
    main()
