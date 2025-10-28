# SMART REPORTS v2.0 - HUTCHISON PORTS

Sistema de Gestión de Capacitaciones con Diseño Corporativo Oficial

<img src="https://img.shields.io/badge/version-2.0-blue" alt="Version 2.0">
<img src="https://img.shields.io/badge/design-Hutchison_Ports-009BDE" alt="Hutchison Ports">
<img src="https://img.shields.io/badge/python-3.8+-green" alt="Python 3.8+">

---

## 🎨 Diseño Corporativo

Smart Reports v2.0 implementa el **Manual de Identidad Visual de Hutchison Ports** al 100%:

- ✅ **Paleta corporativa**: Sky Blue, Sea Blue, Aqua Green, Sunray Yellow, Sunset Orange
- ✅ **Tipografía oficial**: Montserrat (títulos) + Arial (cuerpo)
- ✅ **Formas anguladas**: Dynamic Angle de 30.3°
- ✅ **Logo corporativo**: En esquina superior izquierda
- ✅ **Sidebar Sea Blue**: Con texto blanco (#002E6D)

---

## 🚀 Inicio Rápido

### 1. Activar entorno virtual

```bash
cd smart-reports
.venv\Scripts\activate  # Windows
# o
source .venv/bin/activate  # Linux/Mac
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar aplicación

```bash
python smart_reports/main.py
```

¡Eso es todo! La aplicación se abrirá con el diseño corporativo Hutchison Ports.

---

## 📊 Paneles Disponibles

### 🏠 Dashboard
- **Métricas en tiempo real** con tarjetas anguladas
- Total de usuarios, módulos, completados y progreso global
- Headers y divisores con formas anguladas (30.3°)
- **Funciona sin BD**: Muestra datos de demostración

### 🔍 Consultas
- **Búsqueda de usuarios** por User ID
- Resultados formateados con diseño corporativo
- Información completa: nombre, email, unidad de negocio
- **Requiere BD** para funcionar

### 📤 Actualizar Datos
- **Drag & Drop** de archivos Excel/CSV
- Botón de selección de archivo
- Preview de datos cargados
- Procesamiento automático
- **Funciona sin BD**: Carga y muestra archivo

### ⚙️ Configuración
- **4 tarjetas corporativas** con colores oficiales:
  - 👥 Gestionar Usuarios (Sky Blue)
  - 💾 Respaldar BD (Aqua Green)
  - ℹ️ Acerca de (Sunray Yellow)
  - 🔧 Configuración BD (Sunset Orange)

---

## 🎯 Características Principales

### ✅ Funciona CON y SIN Base de Datos

**Sin conexión a BD:**
- Dashboard muestra datos de demostración
- Actualizar carga y muestra archivos
- Configuración funcional (excepto Gestionar Usuarios)

**Con conexión a BD:**
- Dashboard con datos reales en tiempo real
- Consultas de usuarios funcionales
- Procesamiento y actualización de datos
- Gestión completa de usuarios

### ✅ Diseño Responsivo

- Sidebar fijo corporativo
- Área de contenido scrollable
- Headers angulados en cada panel
- Divisores angulados entre secciones
- Logo siempre visible arriba

### ✅ Tipografía Corporativa

- **Montserrat Bold**: Títulos de paneles (ej: "Dashboard")
- **Montserrat Regular**: Subtítulos de tarjetas
- **Arial Regular**: Texto de cuerpo, descripciones
- **Arial Bold**: Botones

### ✅ Colores Corporativos

| Color | Hex | Uso |
|-------|-----|-----|
| Ports Sky Blue | `#009BDE` | Primario, headers, botón principal |
| Ports Aqua Green | `#54BBAB` | Secundario, métricas |
| Ports Sunray Yellow | `#FFC627` | Acentos, advertencias |
| Ports Sunset Orange | `#EE7523` | Acentos, progreso |
| Ports Sea Blue | `#002E6D` | Texto, sidebar |
| Blanco | `#FFFFFF` | Fondos principales |

---

## 📦 Dependencias

```txt
# UI
customtkinter>=5.2.0
tkinterdnd2-universal>=1.7.3  # Opcional para drag & drop

# Base de datos
pyodbc>=5.0.0  # SQL Server
mysql-connector-python>=8.0.33  # MySQL

# Procesamiento de datos
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0

# Gráficos
plotly>=5.17.0
matplotlib>=3.7.0

# Reportes
reportlab>=4.0.0
```

---

## ⚙️ Configuración

### Base de Datos

Edita `smart_reports/config/settings.py`:

**SQL Server (Trabajo):**
```python
DB_TYPE = 'sqlserver'

SQLSERVER_CONFIG = {
    'server': 'tu_servidor',
    'database': 'TNGCORE',
    'driver': '{ODBC Driver 17 for SQL Server}',
    'trusted_connection': 'yes'
}
```

**MySQL (Casa):**
```python
DB_TYPE = 'mysql'

MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'tngcore',
    'user': 'root',
    'password': 'tu_password'
}
```

---

## 📁 Estructura del Proyecto

```
smart-reports/
├── smart_reports/
│   ├── main.py                          ⭐ Punto de entrada
│   ├── config/
│   │   ├── hutchison_identity.py        # Colores, fuentes, tema
│   │   └── settings.py                  # Configuración BD
│   ├── database/
│   │   └── connection.py                # Conexión BD
│   ├── services/
│   │   └── data_processor.py            # Procesamiento datos
│   └── ui/
│       ├── main_window_hutchison.py     # Ventana principal
│       ├── components/
│       │   ├── hutchison_widgets.py     # Widgets angulados
│       │   ├── hutchison_sidebar.py     # Sidebar corporativo
│       │   └── hutchison_config_card.py # Tarjetas config
│       └── dialogs/
│           └── user_management_dialog.py # Gestión usuarios
│
├── requirements.txt                      # Dependencias
├── README.md                            # Este archivo
├── GUIA_INSTALACION.md                  # Guía detallada
└── REDISENO_HUTCHISON_PORTS.md         # Documentación diseño
```

---

## 🔧 Solución de Problemas

### La aplicación no inicia

```bash
# 1. Verifica que el entorno virtual esté activado
.venv\Scripts\activate

# 2. Reinstala dependencias
pip install -r requirements.txt --force-reinstall

# 3. Verifica Python
python --version  # Debe ser 3.8 o superior
```

### Error de fuentes

Si las fuentes no se ven correctas:

1. Instala **Montserrat** en tu sistema
2. Windows: Copia archivos .ttf a `C:\Windows\Fonts`
3. Si no puedes instalarla, la app usará Arial (funciona perfectamente)

### Sin conexión a BD

La aplicación funciona perfectamente sin base de datos:
- Dashboard muestra datos demo
- Actualizar carga archivos
- Solo "Gestionar Usuarios" requiere BD obligatoriamente

### Drag & Drop no funciona

```bash
pip install tkinterdnd2-universal
```

Si sigue sin funcionar, usa el botón "Seleccionar Archivo" en su lugar.

---

## 📖 Documentación Adicional

- **[GUIA_INSTALACION.md](GUIA_INSTALACION.md)** - Instalación paso a paso y troubleshooting
- **[REDISENO_HUTCHISON_PORTS.md](REDISENO_HUTCHISON_PORTS.md)** - Documentación completa del diseño corporativo
- **[FUNCIONALIDADES_IMPLEMENTADAS.md](FUNCIONALIDADES_IMPLEMENTADAS.md)** - Todas las funcionalidades

---

## 🎨 Capturas de Pantalla

### Panel Dashboard
```
┌──────────── Dashboard ────────────╱
│
│ ╱──────────────────────────────────╲
│
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ │  156   │ │   24   │ │  892   │ │ 73.5%  │
│ │Usuarios│ │Módulos │ │Complete│ │Progress│
│ └────────┘ └────────┘ └────────┘ └────────┘
```

### Sidebar Sea Blue
```
│ HUTCHISON PORTS │
│ Smart Reports   │
│ ─────────────── │
│ 📊 Dashboard    │  ← Activo
│ 🔍 Consultas    │
│ 📤 Actualizar   │
│ ⚙️ Configuración│
│                 │
│ ─────────────── │
│ v2.0            │
│ © 2025 HP       │
```

---

## 🏆 Características del Diseño

### Headers Angulados (Sky Shape)
Todos los paneles tienen headers con forma angulada a 30.3°

### Divisores Angulados (Horizon Shape)
Separadores visuales con forma de paralelogramo angulado

### Tarjetas Métricas Anguladas
Métricas con headers angulados y colores corporativos

### Botones Corporativos
- Colores oficiales Hutchison Ports
- Tipografía Arial Bold
- Estados hover más oscuros

---

## 📞 Soporte

Para problemas o preguntas:

1. Lee la **[GUIA_INSTALACION.md](GUIA_INSTALACION.md)**
2. Consulta **[REDISENO_HUTCHISON_PORTS.md](REDISENO_HUTCHISON_PORTS.md)**
3. Revisa la configuración en `smart_reports/config/settings.py`

---

## 📝 Licencia

© 2025 Hutchison Ports - Instituto Hutchison Ports
Todos los derechos reservados.

---

## 🎯 Versión

**Smart Reports v2.0** - Diseño Corporativo Hutchison Ports

**Última actualización:** 2025-10-27

**Características principales:**
- ✅ Diseño 100% corporativo Hutchison Ports
- ✅ Funciona con y sin base de datos
- ✅ Drag & drop de archivos
- ✅ Gestión completa de usuarios
- ✅ Métricas en tiempo real
- ✅ Procesamiento de datos automatizado

---

**¡Listo para usar!** 🚀

```bash
python smart_reports/main.py
```
