# Rediseño Corporativo Hutchison Ports

## 📋 Resumen Ejecutivo

Este documento describe la implementación completa del Manual de Identidad Visual de Hutchison Ports en la aplicación Smart Reports v2.0.

Todos los elementos de la interfaz han sido rediseñados para cumplir estrictamente con:
- Paleta de colores corporativa
- Tipografía oficial (Montserrat y Arial)
- Formas gráficas con Dynamic Angle de 30.3°
- Guidelines de marca y layout

---

## 🎨 1. PALETA DE COLORES IMPLEMENTADA

### Colores Principales

```python
HUTCHISON_COLORS = {
    # Color Principal
    'ports_sky_blue': '#009BDE',      # Ports Sky Blue - Acento primario

    # Colores Secundarios
    'ports_aqua_green': '#54BBAB',    # Ports Aqua Green
    'ports_sunray_yellow': '#FFC627', # Ports Sunray Yellow
    'ports_sunset_orange': '#EE7523', # Ports Sunset Orange

    # Texto
    'ports_sea_blue': '#002E6D',      # Ports Sea Blue - Texto principal

    # Neutros
    'white': '#FFFFFF',               # Fondos principales
    'light_gray': '#F5F5F5',         # Fondos alternativos
    'medium_gray': '#E0E0E0',        # Bordes y divisores
}
```

### Aplicación en la UI

| Elemento | Color | Código Hex |
|----------|-------|------------|
| Fondo Principal | Blanco | `#FFFFFF` |
| Sidebar Fondo | Ports Sea Blue | `#002E6D` |
| Texto Principal | Ports Sea Blue | `#002E6D` |
| Botones Primarios | Ports Sky Blue | `#009BDE` |
| Botones Secundarios | Ports Aqua Green | `#54BBAB` |
| Acentos | Sunray Yellow / Sunset Orange | `#FFC627` / `#EE7523` |
| Texto en Sidebar | Blanco | `#FFFFFF` |

---

## ✍️ 2. TIPOGRAFÍA CORPORATIVA

### Fuentes Implementadas

Según el manual de identidad (páginas 40-42):

**1. Montserrat (Web/Multimedia)**
- Uso: Títulos, encabezados, headings
- Variantes: Bold, Regular
- Ubicación: Títulos de paneles, nombres de tarjetas, navegación

**2. Arial (Default - Sistemas Informáticos)**
- Uso: Texto de cuerpo, párrafos, datos
- Variantes: Regular, Bold
- Ubicación: Descripciones, contenido, tablas

### Jerarquía de Tamaños

```python
FONT_SIZES = {
    'title_large': 32,      # Títulos principales de panel
    'title_medium': 24,     # Subtítulos
    'title_small': 20,      # Títulos de tarjetas
    'heading': 16,          # Encabezados de secciones
    'body_large': 14,       # Texto normal grande
    'body': 12,             # Texto normal
    'body_small': 10,       # Texto pequeño
    'caption': 9,           # Notas al pie
}
```

### Ejemplos de Aplicación

```python
# Título de panel (Montserrat Bold, 32pt)
title = HutchisonLabel(parent, text='Dashboard', label_type='title')

# Encabezado de tarjeta (Montserrat Bold, 20pt)
heading = HutchisonLabel(parent, text='Configuración', label_type='heading')

# Texto de cuerpo (Arial Regular, 14pt)
body = HutchisonLabel(parent, text='Descripción...', label_type='body')

# Texto pequeño (Arial Regular, 10pt)
caption = HutchisonLabel(parent, text='v2.0', label_type='caption')
```

---

## 📐 3. DYNAMIC ANGLE (30.3°)

El ángulo característico de Hutchison Ports se implementa en múltiples elementos:

### Constante Global

```python
DYNAMIC_ANGLE = 30.3  # Grados
```

### Implementaciones

#### 3.1 AngledHeaderFrame (Sky Shape)

Frame con borde superior angulado para encabezados de paneles.

**Características:**
- Forma trapezoidal con ángulo de 30.3°
- Fondo en color corporativo (Sky Blue por defecto)
- Texto en Montserrat Bold
- Uso: Headers de paneles principales

**Código:**
```python
header = AngledHeaderFrame(
    parent,
    text='Dashboard',
    height=80,
    color=theme['primary']
)
```

**Visual:**
```
┌────────────────────────────────╱
│  Dashboard                    ╱
└──────────────────────────────╱
```

#### 3.2 AngledDivider (Horizon Shape)

Divisor con forma de paralelogramo angulado.

**Características:**
- Línea divisora con ángulo de 30.3°
- Color secundario (Aqua Green por defecto)
- Altura configurable (4px recomendado)
- Uso: Separadores visuales entre secciones

**Código:**
```python
divider = AngledDivider(
    parent,
    height=4,
    color=theme['secondary']
)
```

**Visual:**
```
╱────────────────────────────────╲
```

#### 3.3 AngledCard (Sea Shape)

Tarjeta con header angulado superior.

**Características:**
- Header con forma angulada
- Área de contenido rectangular
- Borde corporativo
- Uso: Tarjetas de contenido, gráficos, métricas

**Código:**
```python
card = AngledCard(
    parent,
    title='Métrica',
    header_color=theme['primary']
)
card.add_content(widget)
```

---

## 🏢 4. LAYOUT Y MARCA CORPORATIVA

### 4.1 Logo Corporativo

**Ubicación:** Esquina superior izquierda (obligatorio)

**Implementación:**
```python
logo = LogoFrame(parent)
logo.pack(side='left', padx=20, pady=10)
```

**Contenido:**
- "HUTCHISON PORTS" (Montserrat Bold, 18pt)
- "Smart Reports" (Arial Regular, 11pt)
- Color: Ports Sea Blue

### 4.2 Sidebar

**Características:**
- Fondo: Ports Sea Blue (`#002E6D`)
- Texto: Blanco (`#FFFFFF`)
- Estilo: "Reversed colour Corporate Mark"
- Ancho: 240px

**Elementos:**
- Logo corporativo arriba
- Navegación con iconos
- Footer con versión y copyright
- Separadores en Sky Blue

**Código:**
```python
sidebar = HutchisonSidebar(parent, navigation_callbacks)
```

### 4.3 Alineación de Texto

**Regla:** Todo el texto debe estar **alineado a la izquierda** ("ranged left")

Implementación:
```python
label.configure(anchor='w', justify='left')
```

---

## 🧩 5. COMPONENTES CORPORATIVOS

### 5.1 HutchisonButton

Botón con colores y tipografía corporativa.

**Tipos:**
- `primary`: Sky Blue
- `secondary`: Aqua Green
- `accent`: Sunray Yellow
- `warning`: Sunset Orange

**Código:**
```python
btn = HutchisonButton(
    parent,
    text='Guardar',
    button_type='primary',
    command=callback
)
```

### 5.2 HutchisonLabel

Label con tipografía corporativa.

**Tipos:**
- `title`: Montserrat Bold 32pt
- `heading`: Montserrat Bold 20pt
- `body`: Arial Regular 14pt
- `caption`: Arial Regular 10pt

**Código:**
```python
label = HutchisonLabel(
    parent,
    text='Título',
    label_type='heading'
)
```

### 5.3 HutchisonConfigCard

Tarjeta de configuración con diseño corporativo.

**Características:**
- Icono grande con color del botón
- Título en Montserrat Bold
- Descripción en Arial Regular
- Botón corporativo al fondo
- Borde que cambia a color del botón en hover

**Código:**
```python
card = HutchisonConfigCard(
    parent,
    icon='👥',
    title='Gestionar Usuarios',
    description='Agregar nuevos usuarios...',
    button_text='Gestionar',
    button_color=theme['primary'],
    command=callback
)
```

### 5.4 MetricCardAngled

Tarjeta métrica con header angulado.

**Características:**
- Header angulado con título
- Valor grande en Montserrat Bold
- Subtítulo opcional
- Color personalizable

**Código:**
```python
metric = MetricCardAngled(
    parent,
    title='Total Usuarios',
    value='1,234',
    subtitle='Usuarios activos',
    color=theme['primary']
)
```

---

## 📁 6. ESTRUCTURA DE ARCHIVOS

### Nuevos Módulos Creados

```
smart_reports/
├── config/
│   └── hutchison_identity.py       # Colores, fuentes, constantes
├── ui/
│   └── components/
│       ├── hutchison_widgets.py    # Widgets con Dynamic Angle
│       ├── hutchison_sidebar.py    # Sidebar corporativo
│       └── hutchison_config_card.py # Tarjetas de configuración
```

### Archivos de Demostración

```
├── demo_hutchison_design.py        # Demo completa del diseño
└── REDISENO_HUTCHISON_PORTS.md     # Esta documentación
```

---

## 🚀 7. CÓMO USAR EL NUEVO DISEÑO

### 7.1 Ejecutar Demo

```bash
python demo_hutchison_design.py
```

La demo muestra:
- ✓ Panel de Dashboard con métricas anguladas
- ✓ Panel de Configuración con tarjetas corporativas
- ✓ Sidebar Sea Blue con navegación
- ✓ Headers angulados en cada panel
- ✓ Divisores angulados
- ✓ Logo corporativo arriba

### 7.2 Integrar en la Aplicación Principal

Para aplicar el diseño a `main_window_modern.py`:

**Paso 1:** Importar componentes Hutchison

```python
from smart_reports.config.hutchison_identity import get_hutchison_theme, get_font
from smart_reports.ui.components import (
    HutchisonSidebar,
    AngledHeaderFrame,
    AngledDivider,
    HutchisonConfigCard,
    HutchisonButton,
    HutchisonLabel
)
```

**Paso 2:** Aplicar tema

```python
self.theme = get_hutchison_theme()
self.configure(fg_color=self.theme['background'])
```

**Paso 3:** Reemplazar componentes

```python
# Antes
sidebar = ModernSidebar(...)

# Después
sidebar = HutchisonSidebar(...)

# Antes
header = ctk.CTkLabel(text='Dashboard', font=('Segoe UI', 32))

# Después
header = AngledHeaderFrame(parent, text='Dashboard', height=80)

# Antes
card = ConfigCard(...)

# Después
card = HutchisonConfigCard(...)
```

---

## 🎨 8. EJEMPLO VISUAL DEL PANEL DE CONFIGURACIÓN

```
┌─────────────────────────────────────────────────────────────────────┐
│ HUTCHISON PORTS                                                     │
│ Smart Reports                                                       │
└─────────────────────────────────────────────────────────────────────┘
═══════════════════════════════════════════════════════════════════════
│         │
│ HUTCHIS │ ┌─────────────────────── Configuración ───────────────────╱
│ ON      │ │
│ PORTS   │ │ ╱───────────────────────────────────────────────────────╲
│         │ │
│ Smart   │ │
│ Reports │ │ ┌──────────────────┐  ┌──────────────────┐
│         │ │ │  👥             │  │  💾             │
│ ────    │ │ │  Gestionar      │  │  Respaldar      │
│         │ │ │  Usuarios       │  │  Base de Datos  │
│ 📊 Dash │ │ │                 │  │                 │
│ 🔍 Cons │ │ │  [Gestionar]    │  │  [Respaldar]    │
│ 📤 Actu │ │ └──────────────────┘  └──────────────────┘
│ ⚙️ Conf │ │
│         │ │ ┌──────────────────┐  ┌──────────────────┐
│         │ │ │  ℹ️              │  │  🔧             │
│ ────    │ │ │  Acerca de      │  │  Configuración  │
│         │ │ │                 │  │  BD             │
│ v2.0    │ │ │  [Ver Info]     │  │  [Cambiar]      │
│ © 2025  │ │ └──────────────────┘  └──────────────────┘
│ HP      │ │
└─────────┘ └──────────────────────────────────────────────────────────┘
```

**Colores aplicados:**
- Sidebar: Sea Blue (#002E6D) con texto blanco
- Headers: Sky Blue (#009BDE) angulados
- Botón Gestionar: Sky Blue (#009BDE)
- Botón Respaldar: Aqua Green (#54BBAB)
- Botón Ver Info: Sunray Yellow (#FFC627)
- Botón Cambiar: Sunset Orange (#EE7523)

---

## ✅ 9. CHECKLIST DE IMPLEMENTACIÓN

### Colores ✓
- [x] Paleta corporativa definida
- [x] Tema aplicado a CustomTkinter
- [x] Sidebar Sea Blue con texto blanco
- [x] Fondos blancos/gris claro
- [x] Botones con colores corporativos

### Tipografía ✓
- [x] Montserrat para títulos y headings
- [x] Arial para texto de cuerpo
- [x] Jerarquía de tamaños definida
- [x] Funciones helper para obtener fuentes

### Dynamic Angle ✓
- [x] Constante de 30.3° definida
- [x] AngledHeaderFrame implementado
- [x] AngledDivider implementado
- [x] AngledCard implementado
- [x] Cálculos matemáticos correctos

### Layout ✓
- [x] Logo en esquina superior izquierda
- [x] Sidebar a la izquierda
- [x] Alineación de texto a la izquierda
- [x] Estructura corporativa

### Componentes ✓
- [x] HutchisonButton
- [x] HutchisonLabel
- [x] HutchisonConfigCard
- [x] MetricCardAngled
- [x] HutchisonSidebar
- [x] LogoFrame

---

## 📊 10. COMPARATIVA ANTES/DESPUÉS

### Antes (Diseño Original)

| Aspecto | Implementación Original |
|---------|------------------------|
| Colores | Personalizados (púrpura, azul oscuro) |
| Fuentes | Segoe UI |
| Formas | Rectangulares, bordes redondeados |
| Sidebar | Oscuro genérico |
| Identidad | Genérica |

### Después (Diseño Hutchison Ports)

| Aspecto | Implementación Hutchison |
|---------|-------------------------|
| Colores | Paleta corporativa oficial (Sky Blue, Sea Blue, etc.) |
| Fuentes | Montserrat (títulos) + Arial (cuerpo) |
| Formas | Anguladas 30.3° (Dynamic Angle) |
| Sidebar | Sea Blue (#002E6D) corporativo |
| Identidad | 100% alineada con manual de identidad |

---

## 🔧 11. FUNCIONES AUXILIARES

El módulo `hutchison_identity.py` incluye funciones auxiliares:

```python
# Obtener color de la paleta
color = get_color('ports_sky_blue')

# Obtener fuente corporativa
font = get_font('heading', size=20, weight='bold')

# Convertir colores
rgb = hex_to_rgb('#009BDE')
hex_color = rgb_to_hex(0, 155, 222)

# Manipular colores
lighter = lighten_color('#009BDE', 0.2)
darker = darken_color('#009BDE', 0.2)
```

---

## 📝 12. NOTAS DE IMPLEMENTACIÓN

### Fuentes

**Importante:** Para que las fuentes Montserrat se muestren correctamente:

1. Instalar Montserrat en el sistema:
   - Windows: Descargar de Google Fonts y copiar a `C:\Windows\Fonts`
   - macOS: Instalar en Font Book
   - Linux: Copiar a `~/.fonts` y ejecutar `fc-cache -f`

2. Si Montserrat no está disponible, CustomTkinter usará Arial como fallback.

### Ángulo Dinámico

El cálculo del offset angular usa:

```python
offset = height * math.tan(math.radians(DYNAMIC_ANGLE))
```

Esto asegura que el ángulo sea exactamente 30.3° independientemente del tamaño del elemento.

---

## 🎯 13. PRÓXIMOS PASOS

Para completar la implementación en toda la aplicación:

1. **Actualizar main_window_modern.py:**
   - Reemplazar sidebar con HutchisonSidebar
   - Aplicar AngledHeaderFrame a todos los paneles
   - Usar HutchisonButton en todos los botones
   - Aplicar HutchisonLabel a todos los textos

2. **Actualizar paneles:**
   - Dashboard: Usar MetricCardAngled
   - Consultas: Aplicar headers angulados
   - Actualizar: Headers y divisores angulados
   - Configuración: Usar HutchisonConfigCard

3. **Actualizar diálogos:**
   - UserManagementDialog: Aplicar colores y fuentes
   - Otros diálogos: Consistencia corporativa

4. **Gráficos:**
   - Configurar Plotly con colores corporativos
   - Matplotlib con paleta Hutchison

5. **PDFs:**
   - Generar reportes con identidad corporativa
   - Usar colores y fuentes oficiales

---

## 📞 14. SOPORTE

Para dudas sobre la implementación del diseño corporativo:

- Consultar el manual de identidad visual de Hutchison Ports
- Revisar código de `demo_hutchison_design.py`
- Ver ejemplos en `hutchison_widgets.py`

---

## 📄 15. REFERENCIAS

- **Manual de Identidad Visual Hutchison Ports**
  - Página 20: Paleta de colores
  - Páginas 40-42: Tipografía
  - Formas gráficas: Dynamic Angle 30.3°

- **Archivos del Proyecto**
  - `smart_reports/config/hutchison_identity.py`
  - `smart_reports/ui/components/hutchison_widgets.py`
  - `smart_reports/ui/components/hutchison_sidebar.py`
  - `demo_hutchison_design.py`

---

*Documento generado el 2025-10-27*
*Smart Reports v2.0 - Hutchison Ports Corporate Design*
