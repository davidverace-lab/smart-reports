"""
Script de prueba para verificar que los botones de configuración se visualicen correctamente
"""
import sys
import os

# Agregar el directorio al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import customtkinter as ctk
from smart_reports.ui.components.config_card import ConfigCard

def test_button():
    print("Botón clickeado!")

# Crear ventana de prueba
root = ctk.CTk()
root.title("Test - Botones de Configuración")
root.geometry("800x600")

# Configurar tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Frame principal
main_frame = ctk.CTkFrame(root, fg_color='#1a1d2e')
main_frame.pack(fill='both', expand=True, padx=20, pady=20)

# Título
title = ctk.CTkLabel(
    main_frame,
    text='Prueba de Botones de Configuración',
    font=('Segoe UI', 24, 'bold'),
    text_color='#ffffff'
)
title.pack(pady=20)

# Grid para las cards
grid_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
grid_frame.pack(fill='both', expand=True, padx=20, pady=20)

grid_frame.grid_columnconfigure((0, 1), weight=1)
grid_frame.grid_rowconfigure((0, 1), weight=1)

# Definir colores
PRIMARY_COLORS = {
    'accent_blue': '#6c63ff',
    'accent_green': '#51cf66',
    'accent_orange': '#ff8c42',
    'accent_cyan': '#4ecdc4'
}

# Card 1: Gestionar Usuarios (azul)
card1 = ConfigCard(
    grid_frame,
    icon='👥',
    title='Gestionar Usuarios',
    description='Agregar nuevos usuarios o editar información de usuarios existentes',
    button_text='Gestionar',
    button_color=PRIMARY_COLORS['accent_blue'],
    command=lambda: print("Gestionar Usuarios clickeado")
)
card1.grid(row=0, column=0, padx=15, pady=15, sticky='nsew')

# Card 2: Respaldar Base de Datos (verde)
card2 = ConfigCard(
    grid_frame,
    icon='💾',
    title='Respaldar Base de Datos',
    description='Crear un respaldo de seguridad de la base de datos actual',
    button_text='Respaldar',
    button_color=PRIMARY_COLORS['accent_green'],
    command=lambda: print("Respaldar DB clickeado")
)
card2.grid(row=0, column=1, padx=15, pady=15, sticky='nsew')

# Card 3: Acerca de (cyan)
card3 = ConfigCard(
    grid_frame,
    icon='ℹ️',
    title='Acerca de',
    description='Información sobre Smart Reports y versión del software',
    button_text='Ver Info',
    button_color=PRIMARY_COLORS['accent_cyan'],
    command=lambda: print("Acerca de clickeado")
)
card3.grid(row=1, column=0, padx=15, pady=15, sticky='nsew')

# Card 4: Configuración de BD (naranja)
card4 = ConfigCard(
    grid_frame,
    icon='🔧',
    title='Configuración BD',
    description='Cambiar configuración de base de datos',
    button_text='Cambiar',
    button_color=PRIMARY_COLORS['accent_orange'],
    command=lambda: print("Configuración BD clickeado")
)
card4.grid(row=1, column=1, padx=15, pady=15, sticky='nsew')

print("\n" + "="*60)
print("TEST DE BOTONES DE CONFIGURACIÓN")
print("="*60)
print("\nLos botones deben visualizarse con:")
print("- Borde visible del color correspondiente")
print("- Texto blanco legible")
print("- Efecto hover al pasar el mouse")
print("- Cursor 'hand2' al pasar sobre el botón")
print("\nSi los botones se ven correctamente, el fix está funcionando!")
print("="*60 + "\n")

root.mainloop()
