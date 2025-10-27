"""
Lanzador de Smart Reports
Permite elegir entre el diseño original y el diseño corporativo Hutchison Ports
"""

import sys
import os

# Agregar al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import customtkinter as ctk
from tkinter import messagebox


class DesignSelector(ctk.CTk):
    """Selector de diseño de la aplicación"""

    def __init__(self):
        super().__init__()

        self.title("Smart Reports - Selector de Diseño")
        self.geometry("600x450")
        self.resizable(False, False)

        # Centrar ventana
        self.center_window()

        # Configurar apariencia
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.selected_design = None

        self._create_interface()

    def center_window(self):
        """Centrar ventana en la pantalla"""
        self.update_idletasks()
        width = 600
        height = 450
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _create_interface(self):
        """Crear interfaz del selector"""
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color='transparent')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Logo/Título
        title = ctk.CTkLabel(
            main_frame,
            text='SMART REPORTS',
            font=('Segoe UI', 32, 'bold'),
            text_color='#009BDE'
        )
        title.pack(pady=(0, 10))

        subtitle = ctk.CTkLabel(
            main_frame,
            text='Instituto Hutchison Ports',
            font=('Segoe UI', 14),
            text_color='#666666'
        )
        subtitle.pack(pady=(0, 30))

        # Descripción
        desc = ctk.CTkLabel(
            main_frame,
            text='Selecciona el diseño de la aplicación:',
            font=('Segoe UI', 16, 'bold')
        )
        desc.pack(pady=(0, 20))

        # Frame para los botones de selección
        buttons_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        buttons_frame.pack(fill='both', expand=True, pady=10)

        # Botón Diseño Original
        original_frame = ctk.CTkFrame(
            buttons_frame,
            fg_color='#2b2d42',
            corner_radius=15,
            border_width=2,
            border_color='#3a3d5c'
        )
        original_frame.pack(fill='x', pady=10)

        ctk.CTkLabel(
            original_frame,
            text='🎨  Diseño Original',
            font=('Segoe UI', 20, 'bold')
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            original_frame,
            text='Diseño moderno con tema oscuro/claro personalizable',
            font=('Segoe UI', 12),
            text_color='#a0a0b0'
        ).pack(pady=(0, 15))

        original_btn = ctk.CTkButton(
            original_frame,
            text='Usar Diseño Original',
            font=('Segoe UI', 14, 'bold'),
            fg_color='#6c63ff',
            hover_color='#5a52d5',
            height=45,
            command=lambda: self.launch_design('original')
        )
        original_btn.pack(padx=30, pady=(0, 20))

        # Botón Diseño Hutchison Ports
        hutchison_frame = ctk.CTkFrame(
            buttons_frame,
            fg_color='#2b2d42',
            corner_radius=15,
            border_width=2,
            border_color='#3a3d5c'
        )
        hutchison_frame.pack(fill='x', pady=10)

        ctk.CTkLabel(
            hutchison_frame,
            text='🏢  Diseño Hutchison Ports',
            font=('Segoe UI', 20, 'bold')
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            hutchison_frame,
            text='Diseño corporativo oficial con identidad visual HP',
            font=('Segoe UI', 12),
            text_color='#a0a0b0'
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            hutchison_frame,
            text='✓ Colores corporativos  ✓ Formas anguladas (30.3°)  ✓ Tipografía oficial',
            font=('Segoe UI', 10),
            text_color='#009BDE'
        ).pack(pady=(0, 15))

        hutchison_btn = ctk.CTkButton(
            hutchison_frame,
            text='Usar Diseño Corporativo',
            font=('Segoe UI', 14, 'bold'),
            fg_color='#009BDE',
            hover_color='#0088C5',
            height=45,
            command=lambda: self.launch_design('hutchison')
        )
        hutchison_btn.pack(padx=30, pady=(0, 20))

        # Footer
        footer = ctk.CTkLabel(
            main_frame,
            text='v2.0 © 2025 Hutchison Ports',
            font=('Segoe UI', 10),
            text_color='#666666'
        )
        footer.pack(side='bottom', pady=(20, 0))

    def launch_design(self, design):
        """Lanzar la aplicación con el diseño seleccionado"""
        self.selected_design = design
        self.withdraw()  # Ocultar selector

        try:
            if design == 'original':
                # Lanzar diseño original
                from smart_reports.ui.main_window_modern import MainWindow
                root = ctk.CTk()
                app = MainWindow(root)
                root.mainloop()
            else:
                # Lanzar diseño Hutchison
                from smart_reports.ui.main_window_hutchison import MainWindowHutchison
                root = ctk.CTk()
                app = MainWindowHutchison(root)
                root.mainloop()

        except Exception as e:
            messagebox.showerror(
                "Error al iniciar",
                f"No se pudo iniciar la aplicación:\n\n{str(e)}\n\n" +
                "Asegúrate de que todas las dependencias estén instaladas."
            )
            self.deiconify()  # Mostrar selector nuevamente
        else:
            # Cerrar selector si la app se cerró normalmente
            self.destroy()


def main():
    """Función principal del lanzador"""
    print("\n" + "="*70)
    print("SMART REPORTS - HUTCHISON PORTS")
    print("="*70)
    print("\nLanzando selector de diseño...")
    print("\nDiseños disponibles:")
    print("  1. Diseño Original - Moderno con tema oscuro/claro")
    print("  2. Diseño Hutchison Ports - Corporativo con identidad visual")
    print("\n" + "="*70 + "\n")

    app = DesignSelector()
    app.mainloop()


if __name__ == '__main__':
    main()
