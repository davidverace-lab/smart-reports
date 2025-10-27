# Comparación de Diseños - Smart Reports v2.0

## 🎨 Dos Diseños Disponibles

Smart Reports ahora ofrece **dos diseños completos** que puedes usar simultáneamente:

1. **Diseño Original** - Moderno con tema oscuro/claro personalizable
2. **Diseño Hutchison Ports** - Corporativo oficial con identidad visual

---

## 🚀 Cómo Usar

### Opción 1: Lanzador con Selector (Recomendado)

```bash
python launch_smart_reports.py
```

Esto abre un selector visual donde puedes elegir qué diseño usar:

```
┌────────────────────────────────────────┐
│    SMART REPORTS                       │
│    Instituto Hutchison Ports           │
│                                        │
│  Selecciona el diseño de la aplicación:│
│                                        │
│  🎨  Diseño Original                   │
│  [Usar Diseño Original]                │
│                                        │
│  🏢  Diseño Hutchison Ports            │
│  ✓ Colores corporativos                │
│  ✓ Formas anguladas (30.3°)            │
│  ✓ Tipografía oficial                  │
│  [Usar Diseño Corporativo]             │
└────────────────────────────────────────┘
```

### Opción 2: Lanzar Directamente

**Diseño Original:**
```bash
python smart_reports/main.py
```

**Diseño Hutchison Ports:**
```bash
python -m smart_reports.ui.main_window_hutchison
```

---

## 📊 Comparación de Características

| Aspecto | Diseño Original | Diseño Hutchison Ports |
|---------|----------------|------------------------|
| **Colores** | Personalizados (púrpura, azul) | Paleta corporativa HP (Sky Blue, Sea Blue, etc.) |
| **Fuentes** | Segoe UI | Montserrat (títulos) + Arial (cuerpo) |
| **Formas** | Rectangulares con bordes redondeados | Anguladas a 30.3° (Dynamic Angle) |
| **Sidebar** | Oscuro genérico | Sea Blue (#002E6D) corporativo |
| **Headers** | Rectangulares | Formas anguladas (Sky Shape) |
| **Divisores** | Líneas rectas | Formas anguladas (Horizon Shape) |
| **Logo** | Texto simple | Logo corporativo (esquina superior izq.) |
| **Tema** | Claro/Oscuro seleccionable | Tema corporativo fijo (fondos claros) |
| **Identidad** | Genérica | 100% alineada con manual de identidad HP |

---

## 🎯 ¿Cuál Usar?

### Usa el **Diseño Original** si:
- ✅ Prefieres un diseño moderno y minimalista
- ✅ Te gusta poder cambiar entre modo claro y oscuro
- ✅ Quieres una apariencia más neutral

### Usa el **Diseño Hutchison Ports** si:
- ✅ Necesitas cumplir con la identidad corporativa oficial
- ✅ Quieres una presentación más profesional y corporativa
- ✅ El software será usado en contextos oficiales de HP
- ✅ Requieres alineación con el manual de identidad visual

---

## 🖼️ Capturas de Pantalla

### Panel de Configuración

**Diseño Original:**
```
┌─────────────────────────────────────┐
│ Configuración                       │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────┐  ┌──────────┐        │
│  │   👥     │  │   💾     │        │
│  │Gestionar │  │Respaldar │        │
│  │ Usuarios │  │    BD    │        │
│  └──────────┘  └──────────┘        │
│                                     │
│  ┌──────────┐  ┌──────────┐        │
│  │   ℹ️      │  │   🔧     │        │
│  │ Acerca   │  │Config BD │        │
│  │    de    │  │          │        │
│  └──────────┘  └──────────┘        │
└─────────────────────────────────────┘
```

**Diseño Hutchison Ports:**
```
┌─────────── Configuración ────────╱
│
│ ╱────────────────────────────────╲
│
│  ┌──────────┐  ┌──────────┐
│  │   👥     │  │   💾     │
│  │Gestionar │  │Respaldar │
│  │ Usuarios │  │    BD    │
│  │(Sky Blue)│  │(Aqua Grn)│
│  └──────────┘  └──────────┘
│
│  ┌──────────┐  ┌──────────┐
│  │   ℹ️      │  │   🔧     │
│  │ Acerca   │  │Config BD │
│  │    de    │  │          │
│  │(Yellow)  │  │(Orange)  │
│  └──────────┘  └──────────┘
└──────────────────────────────────
```

---

## 🔄 Cambiar Entre Diseños

Puedes cambiar de diseño en cualquier momento:

1. **Cierra** la aplicación actual
2. **Ejecuta** `launch_smart_reports.py`
3. **Selecciona** el otro diseño

O simplemente ejecuta el archivo correspondiente directamente.

---

## 💡 Funcionalidad Idéntica

**Ambos diseños tienen la misma funcionalidad:**

- ✅ Dashboard con métricas en tiempo real
- ✅ Consultas de usuarios
- ✅ Actualización de datos (Drag & Drop)
- ✅ Gestión de usuarios
- ✅ Conexión a base de datos
- ✅ Generación de reportes

**Solo cambia la apariencia visual, no las capacidades.**

---

## 🎨 Paleta de Colores

### Diseño Original
- **Primario:** Púrpura (`#6c63ff`)
- **Secundario:** Azul (`#4ecdc4`)
- **Fondo:** Gris oscuro (`#1a1d2e`)
- **Superficie:** Gris medio (`#2b2d42`)

### Diseño Hutchison Ports
- **Primario:** Ports Sky Blue (`#009BDE`)
- **Secundario:** Ports Aqua Green (`#54BBAB`)
- **Acento 1:** Ports Sunray Yellow (`#FFC627`)
- **Acento 2:** Ports Sunset Orange (`#EE7523`)
- **Texto:** Ports Sea Blue (`#002E6D`)
- **Fondo:** Blanco (`#FFFFFF`)
- **Sidebar:** Ports Sea Blue (`#002E6D`)

---

## 📁 Archivos del Proyecto

```
smart-reports/
├── launch_smart_reports.py          ⭐ LANZADOR CON SELECTOR
├── smart_reports/
│   ├── main.py                      # Diseño original
│   └── ui/
│       ├── main_window_modern.py    # Ventana original
│       └── main_window_hutchison.py # Ventana Hutchison
│
├── demo_hutchison_design.py         # Demo del diseño HP
└── COMPARACION_DISENOS.md          # Este archivo
```

---

## 🔧 Requisitos

Ambos diseños requieren las mismas dependencias:

```bash
pip install -r requirements.txt
```

**Dependencias principales:**
- `customtkinter>=5.2.0`
- `tkinterdnd2-universal>=1.7.3`
- `pyodbc>=5.0.0` o `mysql-connector-python>=8.0.33`
- `pandas>=2.0.0`
- `openpyxl>=3.1.0`

---

## 📝 Notas

1. **Fuente Montserrat**: Para el diseño Hutchison, instala la fuente Montserrat para obtener el mejor resultado. Si no está instalada, se usará Arial como fallback.

2. **Base de datos**: Ambos diseños usan la misma configuración de base de datos en `smart_reports/config/settings.py`.

3. **Rendimiento**: No hay diferencia de rendimiento entre ambos diseños.

4. **Archivos compartidos**: Ambos diseños comparten:
   - Conexión a base de datos
   - Lógica de negocio
   - Procesamiento de datos
   - Diálogos de usuario

5. **Independientes**: Puedes tener ambos abiertos simultáneamente en ventanas diferentes si lo deseas.

---

## 🆘 Solución de Problemas

### El selector no aparece

```bash
# Verifica que esté instalado customtkinter
pip install customtkinter

# Ejecuta directamente
python launch_smart_reports.py
```

### Error al cambiar de diseño

Cierra completamente todas las ventanas de Smart Reports antes de abrir un nuevo diseño.

### Las fuentes se ven diferentes

En el diseño Hutchison, si no tienes Montserrat instalada, se usará Arial. Esto es normal y la aplicación funcionará perfectamente.

---

## 📞 Soporte

Para problemas o preguntas:
1. Lee la **GUIA_INSTALACION.md**
2. Consulta **REDISENO_HUTCHISON_PORTS.md** (para diseño corporativo)
3. Revisa **FUNCIONALIDADES_IMPLEMENTADAS.md**

---

*Última actualización: 2025-10-27*
*Smart Reports v2.0 - Dual Design Edition*
