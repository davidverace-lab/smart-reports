"""
Script de verificación de estructura de base de datos
Verifica que las tablas existan y contengan datos
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from smart_reports.database.connection import DatabaseConnection


def verificar_estructura_bd():
    """Verifica que la estructura de la BD sea correcta"""
    print("=" * 70)
    print("VERIFICACIÓN DE ESTRUCTURA DE BASE DE DATOS")
    print("=" * 70)

    db = DatabaseConnection()

    if not db.connect():
        print("\n❌ ERROR: No se pudo conectar a la base de datos")
        print("Verifica la configuración en database/connection.py")
        return False

    cursor = db.get_cursor()
    if not cursor:
        print("\n❌ ERROR: No se pudo obtener cursor")
        return False

    print("\n✅ Conexión exitosa a la base de datos\n")

    # Tablas a verificar
    tablas_requeridas = [
        'Instituto_Usuario',
        'Instituto_UnidadDeNegocio',
        'Instituto_Modulo',
        'Instituto_ProgresoModulo'
    ]

    resultados = {}

    for tabla in tablas_requeridas:
        print(f"\n{'─' * 70}")
        print(f"📊 TABLA: {tabla}")
        print('─' * 70)

        try:
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            resultados[tabla] = count

            if count > 0:
                print(f"✅ Registros encontrados: {count:,}")

                # Mostrar primeros 3 registros
                cursor.execute(f"SELECT TOP 3 * FROM {tabla}")
                rows = cursor.fetchall()

                if rows and cursor.description:
                    # Obtener nombres de columnas
                    columnas = [desc[0] for desc in cursor.description]
                    print(f"\n📋 Columnas ({len(columnas)}): {', '.join(columnas[:5])}...")

                    print("\n🔍 Muestra de datos (primeros 3 registros):")
                    for idx, row in enumerate(rows, 1):
                        print(f"  Registro {idx}: {str(row)[:100]}...")
            else:
                print(f"⚠️  Tabla existe pero está VACÍA (0 registros)")

        except Exception as e:
            print(f"❌ ERROR al consultar tabla: {e}")
            resultados[tabla] = None

    # Resumen final
    print("\n" + "=" * 70)
    print("RESUMEN DE VERIFICACIÓN")
    print("=" * 70)

    total_registros = 0
    tablas_con_datos = 0
    tablas_vacias = 0
    tablas_error = 0

    for tabla, count in resultados.items():
        if count is None:
            estado = "❌ ERROR"
            tablas_error += 1
        elif count > 0:
            estado = f"✅ {count:,} registros"
            total_registros += count
            tablas_con_datos += 1
        else:
            estado = "⚠️  VACÍA"
            tablas_vacias += 1

        print(f"  {tabla:35} {estado}")

    print(f"\n📊 Estadísticas:")
    print(f"  • Tablas con datos: {tablas_con_datos}/{len(tablas_requeridas)}")
    print(f"  • Tablas vacías: {tablas_vacias}")
    print(f"  • Tablas con error: {tablas_error}")
    print(f"  • Total de registros: {total_registros:,}")

    # Verificar relaciones
    if resultados.get('Instituto_Usuario', 0) > 0 and resultados.get('Instituto_UnidadDeNegocio', 0) > 0:
        print("\n" + "─" * 70)
        print("🔗 VERIFICACIÓN DE RELACIONES")
        print("─" * 70)

        try:
            # Usuarios por unidad
            cursor.execute("""
                SELECT
                    un.NombreUnidad,
                    COUNT(u.UserId) as TotalUsuarios
                FROM Instituto_UnidadDeNegocio un
                LEFT JOIN Instituto_Usuario u ON un.IdUnidad = u.IdUnidadDeNegocio
                GROUP BY un.NombreUnidad
                ORDER BY TotalUsuarios DESC
            """)

            print("\n📊 Usuarios por Unidad de Negocio:")
            for row in cursor.fetchall():
                unidad, total = row
                print(f"  • {unidad:20} {total:4} usuarios")

        except Exception as e:
            print(f"❌ Error verificando relaciones: {e}")

    # Verificar progreso si hay datos
    if resultados.get('Instituto_ProgresoModulo', 0) > 0:
        try:
            cursor.execute("""
                SELECT
                    EstatusModuloUsuario,
                    COUNT(*) as Total
                FROM Instituto_ProgresoModulo
                GROUP BY EstatusModuloUsuario
            """)

            print("\n📈 Distribución de Progreso:")
            for row in cursor.fetchall():
                estatus, total = row
                print(f"  • {estatus:20} {total:4} registros")

        except Exception as e:
            print(f"❌ Error verificando progreso: {e}")

    db.disconnect()

    print("\n" + "=" * 70)

    if tablas_vacias > 0 or tablas_error > 0:
        print("\n⚠️  ADVERTENCIA: Se encontraron tablas vacías o con errores")
        print("Recomendación: Ejecutar script de inserción de datos de prueba")
        return False
    else:
        print("\n✅ VERIFICACIÓN EXITOSA: Todas las tablas tienen datos")
        return True


def generar_script_datos_prueba():
    """Genera script SQL para insertar datos de prueba"""
    script = """
-- =====================================================
-- SCRIPT DE DATOS DE PRUEBA PARA SMART REPORTS
-- =====================================================

-- 1. Insertar Unidades de Negocio
INSERT INTO Instituto_UnidadDeNegocio (NombreUnidad) VALUES
('CCI'),
('SANCHEZ'),
('DENNIS'),
('HPMX');

-- 2. Insertar Módulos
INSERT INTO Instituto_Modulo (NombreModulo, Activo) VALUES
('Inducción General', 1),
('Seguridad Industrial', 1),
('Operaciones Portuarias', 1),
('Gestión de Calidad', 1),
('Liderazgo', 1),
('Comunicación Efectiva', 1),
('Trabajo en Equipo', 1),
('Resolución de Conflictos', 0),
('Manejo de Equipos', 1),
('Protocolos de Emergencia', 1),
('Atención al Cliente', 1),
('Excel Avanzado', 1),
('Power BI', 0),
('Inglés Técnico', 1);

-- 3. Insertar Usuarios de Ejemplo (10 usuarios distribuidos en las unidades)
DECLARE @IdCCI INT, @IdSANCHEZ INT, @IdDENNIS INT, @IdHPMX INT;

SELECT @IdCCI = IdUnidad FROM Instituto_UnidadDeNegocio WHERE NombreUnidad = 'CCI';
SELECT @IdSANCHEZ = IdUnidad FROM Instituto_UnidadDeNegocio WHERE NombreUnidad = 'SANCHEZ';
SELECT @IdDENNIS = IdUnidad FROM Instituto_UnidadDeNegocio WHERE NombreUnidad = 'DENNIS';
SELECT @IdHPMX = IdUnidad FROM Instituto_UnidadDeNegocio WHERE NombreUnidad = 'HPMX';

INSERT INTO Instituto_Usuario (Nombre, Email, IdUnidadDeNegocio, Division) VALUES
('Juan Pérez', 'juan.perez@hutchison.com', @IdCCI, 'Operaciones'),
('María González', 'maria.gonzalez@hutchison.com', @IdCCI, 'Administración'),
('Carlos López', 'carlos.lopez@hutchison.com', @IdSANCHEZ, 'Logística'),
('Ana Martínez', 'ana.martinez@hutchison.com', @IdSANCHEZ, 'Operaciones'),
('Roberto Silva', 'roberto.silva@hutchison.com', @IdDENNIS, 'Operaciones'),
('Laura Torres', 'laura.torres@hutchison.com', @IdDENNIS, 'Recursos Humanos'),
('Miguel Ramírez', 'miguel.ramirez@hutchison.com', @IdHPMX, 'Operaciones'),
('Carmen Flores', 'carmen.flores@hutchison.com', @IdHPMX, 'Calidad'),
('Jorge Hernández', 'jorge.hernandez@hutchison.com', @IdCCI, 'Seguridad'),
('Patricia Ruiz', 'patricia.ruiz@hutchison.com', @IdSANCHEZ, 'Administración');

-- 4. Insertar Progreso de Módulos (datos variados)
DECLARE @UserId1 INT, @UserId2 INT, @UserId3 INT;
DECLARE @ModId1 INT, @ModId2 INT, @ModId3 INT, @ModId4 INT;

SELECT TOP 1 @UserId1 = UserId FROM Instituto_Usuario ORDER BY UserId;
SELECT TOP 1 @UserId2 = UserId FROM Instituto_Usuario WHERE Email LIKE '%maria%';
SELECT TOP 1 @UserId3 = UserId FROM Instituto_Usuario WHERE Email LIKE '%carlos%';

SELECT @ModId1 = IdModulo FROM Instituto_Modulo WHERE NombreModulo = 'Inducción General';
SELECT @ModId2 = IdModulo FROM Instituto_Modulo WHERE NombreModulo = 'Seguridad Industrial';
SELECT @ModId3 = IdModulo FROM Instituto_Modulo WHERE NombreModulo = 'Operaciones Portuarias';
SELECT @ModId4 = IdModulo FROM Instituto_Modulo WHERE NombreModulo = 'Gestión de Calidad';

-- Progreso del Usuario 1 (varios módulos en diferentes estados)
INSERT INTO Instituto_ProgresoModulo (UserId, IdModulo, EstatusModuloUsuario, FechaInicio, FechaFinalizacion) VALUES
(@UserId1, @ModId1, 'Completado', '2025-01-15', '2025-01-20'),
(@UserId1, @ModId2, 'Completado', '2025-01-21', '2025-01-25'),
(@UserId1, @ModId3, 'En Progreso', '2025-01-26', NULL),
(@UserId1, @ModId4, 'Registrado', NULL, NULL);

-- Progreso del Usuario 2
INSERT INTO Instituto_ProgresoModulo (UserId, IdModulo, EstatusModuloUsuario, FechaInicio, FechaFinalizacion) VALUES
(@UserId2, @ModId1, 'Completado', '2025-02-01', '2025-02-05'),
(@UserId2, @ModId2, 'En Progreso', '2025-02-06', NULL);

-- Progreso del Usuario 3
INSERT INTO Instituto_ProgresoModulo (UserId, IdModulo, EstatusModuloUsuario, FechaInicio, FechaFinalizacion) VALUES
(@UserId3, @ModId1, 'Completado', '2025-02-10', '2025-02-15'),
(@UserId3, @ModId2, 'Completado', '2025-02-16', '2025-02-20'),
(@UserId3, @ModId3, 'Completado', '2025-02-21', '2025-02-25'),
(@UserId3, @ModId4, 'En Progreso', '2025-02-26', NULL);

PRINT 'Datos de prueba insertados correctamente';
"""

    print("\n" + "=" * 70)
    print("SCRIPT SQL PARA DATOS DE PRUEBA")
    print("=" * 70)
    print(script)

    # Guardar a archivo
    script_path = os.path.join(os.path.dirname(__file__), 'insert_test_data.sql')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)

    print(f"\n💾 Script guardado en: {script_path}")
    print("\nPara ejecutar:")
    print("  1. Abre SQL Server Management Studio")
    print("  2. Conecta a tu base de datos")
    print("  3. Abre y ejecuta el archivo insert_test_data.sql")


if __name__ == '__main__':
    print("\n🚀 Iniciando verificación de base de datos...\n")

    tiene_datos = verificar_estructura_bd()

    if not tiene_datos:
        print("\n" + "=" * 70)
        print("¿Deseas generar el script de datos de prueba? (s/n): ", end='')
        respuesta = input().strip().lower()

        if respuesta in ['s', 'si', 'yes', 'y']:
            generar_script_datos_prueba()

    print("\n✅ Verificación completada\n")
