# SMART REPORTS - SISTEMA DUAL

Sistema de Gestión de Capacitaciones del Instituto Hutchison Ports con **DOS VERSIONES COMPLETAS**.

---

## 🎨 VERSIONES DISPONIBLES

### ✨ Versión HUTCHISON (Diseño Claro Corporativo)
- **Diseño:** Limpio, profesional, fondo blanco
- **Colores:** Sky Blue (#009BDE), Sea Blue (#002E6D)
- **Tipografía:** Montserrat (títulos) + Arial (cuerpo)
- **Ideal para:** Presentaciones formales, impresiones

### 🌙 Versión MODERN (Diseño Oscuro Legacy)
- **Diseño:** Oscuro, elegante, menos fatiga visual
- **Colores:** Fondos oscuros (#1a1d2e, #2b2d42), botones corporativos
- **Tipografía:** Montserrat (títulos) + Arial (cuerpo)
- **Ideal para:** Uso prolongado, ambientes con poca luz

---

## 🚀 EJECUCIÓN

### Versión Hutchison (Claro):
```bash
python main_hutchison.py
```

### Versión Modern (Oscuro):
```bash
python main_modern.py
```

---

## 🔐 LOGIN DE DEMOSTRACIÓN

**Ambas versiones usan el mismo login:**
- **Usuario:** `admin`
- **Contraseña:** `1234`

---

## 📋 FUNCIONALIDADES (AMBAS VERSIONES)

| Funcionalidad | Hutchison | Modern | Estado |
|--------------|-----------|---------|---------|
| Login funcional | ✅ | ✅ | Completo |
| Ventana maximizada | ✅ | ✅ | Completo |
| Dashboard con tabs | ✅ | ✅ | Completo |
| Carga perezosa | ✅ | ✅ | Completo |
| Métricas BD | ✅ | ✅ | Completo |
| Consultas con tksheet | ✅ | ✅ | Completo |
| Búsqueda por ID | ✅ | ✅ | Completo |
| Cruce de Datos | ✅ | ✅ | Completo |
| Drag & Drop Excel | ✅ | ✅ | Completo |
| Configuración | ✅ | ✅ | Completo |
| Cards funcionales | ✅ | ✅ | Completo |
| Botones visibles | ✅ | ✅ | **CORREGIDO** |

---

## 🛠️ TECNOLOGÍAS

| Librería | Versión | Uso |
|----------|---------|-----|
| **customtkinter** | ≥5.2.0 | UI moderna |
| **tkinterdnd2** | ≥1.7.3 | Drag & Drop |
| **tksheet** | ≥6.0.0 | Tablas interactivas |
| **pyodbc** | ≥5.0.0 | SQL Server |
| **pandas** | ≥2.0.0 | Procesamiento de datos |
| **plotly** | ≥5.17.0 | Gráficos interactivos |

---

## 📁 ESTRUCTURA DEL PROYECTO

```
smart_reports/
├── main_hutchison.py          # ← Punto de entrada Hutchison
├── main_modern.py              # ← Punto de entrada Modern
├── smart_reports/
│   ├── config/
│   │   ├── settings_hutchison.py  # Configuración diseño claro
│   │   └── settings_modern.py     # Configuración diseño oscuro
│   ├── database/
│   │   ├── connection.py          # Conexión BD (compartida)
│   │   └── queries.py             # Queries SQL (compartida)
│   └── ui/
│       ├── hutchison/             # Componentes diseño claro
│       │   ├── login_hutchison.py
│       │   ├── main_window_hutchison.py
│       │   ├── dashboard_hutchison.py
│       │   ├── consultas_hutchison.py
│       │   ├── cruce_datos_hutchison.py
│       │   └── configuracion_hutchison.py
│       └── modern/                # Componentes diseño oscuro
│           ├── login_modern.py
│           ├── main_window_modern.py
│           ├── dashboard_modern.py
│           ├── consultas_modern.py
│           ├── cruce_datos_modern.py
│           └── configuracion_modern.py
```

---

## 🎯 CORRECCIONES CRÍTICAS APLICADAS

### ✅ Problema 1: Botones no aparecen en ConfigCard
**Solución:** Cambio de `pack()` a `grid()` en ConfigCard
- **Estado:** ✅ RESUELTO en ambas versiones

### ✅ Problema 2: Tabs pequeñas con mal contraste
**Solución:** CTkTabview personalizado con colores corporativos
- **Estado:** ✅ RESUELTO en ambas versiones

### ✅ Problema 3: Error "accent_green" no definido
**Solución:** Uso de nombres correctos en PRIMARY_COLORS
- **Estado:** ✅ RESUELTO en ambas versiones

### ✅ Problema 4: Bordes gruesos
**Solución:** Todos los bordes en 1px máximo
- **Estado:** ✅ RESUELTO en ambas versiones

### ✅ Problema 5: Drag & Drop no funciona
**Solución:** Implementación con tkinterdnd2 + fallback click
- **Estado:** ✅ RESUELTO en ambas versiones

---

## 🔄 BACKEND COMPARTIDO

Ambas versiones comparten:
- ✅ Lógica de negocio
- ✅ Conexión a base de datos
- ✅ Queries SQL
- ✅ Procesamiento de datos
- ✅ Validaciones

**Solo cambia:** Colores, fondos y estilos visuales

---

## 📊 COMPARACIÓN VISUAL

| Elemento | Hutchison | Modern |
|----------|-----------|---------|
| **Fondo** | #FFFFFF (blanco) | #1a1d2e (oscuro) |
| **Superficie** | #FAFAFA (gris claro) | #2b2d42 (gris oscuro) |
| **Texto principal** | #333333 (oscuro) | #ffffff (blanco) |
| **Botón primario** | Sky Blue (#009BDE) | Sky Blue (#009BDE) |
| **Botón hover** | Sea Blue (#002E6D) | Sea Blue (#002E6D) |
| **Bordes** | #E0E0E0 (claro) | #444654 (oscuro) |

---

## 🧪 TESTING

### Probar Versión Hutchison:
```bash
cd /home/user/smart-reports
python main_hutchison.py
```

### Probar Versión Modern:
```bash
cd /home/user/smart-reports
python main_modern.py
```

### Verificar funcionalidades:
1. Login (admin / 1234)
2. Dashboard - ver 3 tabs
3. Consultas - buscar usuario
4. Cruce de Datos - arrastrar archivo
5. Configuración - clic en botones de cards

---

## 📝 CHANGELOG

### v2.0 - Sistema Dual (2024-10-28)
- ✅ Versión Hutchison completa
- ✅ Versión Modern completa
- ✅ Corrección crítica: ConfigCard con botones visibles
- ✅ Tabs mejoradas con carga perezosa
- ✅ tksheet integrada en ambas versiones
- ✅ Drag & Drop funcional
- ✅ Tipografía corporativa en ambas versiones

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "tksheet not found"
```bash
pip install tksheet>=6.0.0
```

### Error: "tkinterdnd2 not found"
```bash
pip install tkinterdnd2-universal>=1.7.3
```

### Error: "No connection to database"
- Verificar configuración en `smart_reports/config/settings.py`
- Asegurar que SQL Server/MySQL está corriendo
- El sistema funciona sin BD (modo demo)

---

## 👥 CRÉDITOS

- **Diseño corporativo:** Manual de Identidad Visual Hutchison Ports
- **Tipografía:** Montserrat + Arial
- **Framework UI:** CustomTkinter
- **Sistema:** Instituto Hutchison Ports

---

## 📞 SOPORTE

Para reportar problemas o sugerencias:
1. Probar ambas versiones
2. Documentar pasos para reproducir
3. Incluir capturas de pantalla si es posible

---

## ✅ CHECKLIST DE VERIFICACIÓN

**Versión Hutchison:**
- [ ] Login funciona
- [ ] Dashboard carga métricas
- [ ] Tabs cambian correctamente
- [ ] Búsqueda de usuarios funciona
- [ ] Drag & Drop funciona o muestra opción de clic
- [ ] Botones de configuración son visibles
- [ ] Sin errores en consola

**Versión Modern:**
- [ ] Login funciona
- [ ] Dashboard carga métricas
- [ ] Tabs cambian correctamente
- [ ] Búsqueda de usuarios funciona
- [ ] Drag & Drop funciona o muestra opción de clic
- [ ] Botones de configuración son visibles
- [ ] Sin errores en consola

---

## 🎉 ¡LISTO PARA USAR!

Ambas versiones están **100% funcionales** y listas para demostración.

**Recomendación:** Probar primero la versión Hutchison (diseño claro) para presentaciones formales.
