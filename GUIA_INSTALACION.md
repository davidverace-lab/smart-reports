# Guía de Instalación - Smart Reports Hutchison Ports

## 🔧 Solución de Errores Comunes

### Error 1: `ModuleNotFoundError: No module named 'customtkinter'`

**Causa:** Las dependencias no están instaladas.

**Solución:**

```bash
# Activar el entorno virtual (si lo tienes)
.venv\Scripts\activate  # En Windows
# o
source .venv/bin/activate  # En Linux/Mac

# Instalar todas las dependencias
pip install -r requirements.txt
```

### Error 2: `_tkinter.TclError: unknown font style "regular"`

**Causa:** Tkinter usa 'normal' en lugar de 'regular' para estilos de fuente.

**Solución:** ✅ Ya corregido en este commit. Todos los estilos de fuente ahora usan 'normal'.

### Error 3: `Warning: tkinterdnd2 no disponible. Drag & drop deshabilitado`

**Causa:** La librería tkinterdnd2 no está instalada o no funciona en tu sistema.

**Solución:**

```bash
pip install tkinterdnd2-universal
```

**Nota:** Si sigue sin funcionar, la aplicación funcionará normalmente pero sin la función de arrastrar y soltar archivos. Usa el botón "Seleccionar Archivo" en su lugar.

---

## 📦 Instalación Completa

### Paso 1: Clonar o descargar el proyecto

```bash
git clone <url-del-repositorio>
cd smart-reports
```

### Paso 2: Crear entorno virtual (recomendado)

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate

# En Linux/Mac:
source .venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

**Lista de dependencias principales:**
- `customtkinter>=5.2.0` - Framework de UI moderna
- `tkinterdnd2-universal>=1.7.3` - Drag & drop (opcional)
- `pyodbc>=5.0.0` - SQL Server
- `mysql-connector-python>=8.0.33` - MySQL
- `pandas>=2.0.0` - Procesamiento de datos
- `openpyxl>=3.1.0` - Archivos Excel
- `plotly>=5.17.0` - Gráficos interactivos
- `matplotlib>=3.7.0` - Gráficos estáticos
- `reportlab>=4.0.0` - Generación de PDFs

### Paso 4: Instalar fuentes corporativas (opcional pero recomendado)

Para que el diseño se vea exactamente como se especifica:

**Windows:**
1. Descargar Montserrat de Google Fonts: https://fonts.google.com/specimen/Montserrat
2. Extraer los archivos .ttf
3. Copiar a `C:\Windows\Fonts`
4. Reiniciar la aplicación

**Linux:**
```bash
# Crear directorio de fuentes si no existe
mkdir -p ~/.fonts

# Descargar y extraer Montserrat
cd ~/.fonts
wget https://fonts.google.com/download?family=Montserrat
unzip Montserrat.zip
fc-cache -f
```

**macOS:**
1. Descargar Montserrat
2. Abrir Font Book
3. Arrastrar archivos .ttf al Font Book
4. Reiniciar la aplicación

---

## 🚀 Ejecutar la Aplicación

### Demo del Diseño Hutchison Ports

```bash
python demo_hutchison_design.py
```

**Incluye:**
- Panel Dashboard con métricas anguladas
- Panel de Configuración con tarjetas corporativas
- Sidebar Sea Blue con navegación
- Headers angulados a 30.3°
- Todos los colores y tipografías corporativas

### Aplicación Principal

```bash
python smart_reports/main.py
```

---

## 🔍 Verificar Instalación

Ejecuta este script para verificar que todo está correcto:

```bash
python test_all_features.py
```

Esto verificará:
- ✅ Dependencias instaladas
- ✅ Estructura del proyecto
- ✅ Componentes importables
- ✅ Drag & drop disponible

---

## ⚙️ Configuración de Base de Datos

### SQL Server (Trabajo)

Edita `smart_reports/config/settings.py`:

```python
DB_TYPE = 'sqlserver'

SQLSERVER_CONFIG = {
    'server': 'TU_SERVIDOR',
    'database': 'TNGCORE',
    'driver': '{ODBC Driver 17 for SQL Server}',
    'trusted_connection': 'yes'
}
```

### MySQL (Casa)

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

## 🎨 Uso del Diseño Corporativo

### Importar Componentes

```python
from smart_reports.config.hutchison_identity import get_hutchison_theme, get_font
from smart_reports.ui.components import (
    HutchisonSidebar,
    AngledHeaderFrame,
    AngledDivider,
    HutchisonButton,
    HutchisonLabel,
    HutchisonConfigCard,
    MetricCardAngled
)
```

### Aplicar Tema

```python
theme = get_hutchison_theme()

# Configurar ventana
window.configure(fg_color=theme['background'])

# Usar colores
button = HutchisonButton(parent, text='Guardar', button_type='primary')
```

### Crear Headers Angulados

```python
header = AngledHeaderFrame(
    parent,
    text='Dashboard',
    height=80,
    color=theme['primary']
)
```

---

## 🐛 Solución de Problemas

### La aplicación no inicia

1. Verifica que el entorno virtual esté activado
2. Reinstala las dependencias: `pip install -r requirements.txt --force-reinstall`
3. Verifica la versión de Python: `python --version` (debe ser 3.8 o superior)

### Las fuentes no se ven correctas

1. Instala Montserrat en tu sistema (ver Paso 4 arriba)
2. Si no puedes instalar Montserrat, la app usará Arial como fallback
3. Reinicia la aplicación después de instalar fuentes

### Error de conexión a base de datos

1. Verifica la configuración en `smart_reports/config/settings.py`
2. Asegúrate de que el servidor de BD esté corriendo
3. Verifica credenciales y permisos
4. Para SQL Server, instala el driver ODBC: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### Drag & Drop no funciona

1. Intenta instalar: `pip install tkinterdnd2-universal`
2. Si sigue sin funcionar en Windows, puede que necesites permisos de administrador
3. La aplicación funciona normalmente, solo usa el botón "Seleccionar Archivo"

---

## 📚 Documentación Adicional

- **FUNCIONALIDADES_IMPLEMENTADAS.md** - Guía de funcionalidades
- **REDISENO_HUTCHISON_PORTS.md** - Documentación del diseño corporativo
- **Manual de Identidad Hutchison Ports** - Referencia de diseño

---

## 📞 Soporte

Si encuentras problemas:

1. Verifica que todas las dependencias estén instaladas
2. Lee esta guía completa
3. Revisa los archivos de documentación
4. Verifica la configuración de base de datos

---

## ✅ Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Todas las dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Fuente Montserrat instalada (opcional)
- [ ] Base de datos configurada en `settings.py`
- [ ] Demo ejecuta sin errores (`python demo_hutchison_design.py`)

---

*Última actualización: 2025-10-27*
