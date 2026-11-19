import sqlite3
from pathlib import Path
from sqlite3 import Connection, Cursor


class Database:
    """
    Singleton para gestionar la conexión
    y la inicialización de la base de datos SQLite.
    """
    _instance = None
    _db_path = str(Path(__file__).resolve().parent.parent / "sistema_gestion.db")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_connection(self) -> Connection:
        conn = sqlite3.connect(self._db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_db(self) -> bool:
        conn = None
        try:
            conn = self.get_connection()
            cursor: Cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departamento (
                    id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    gerente TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proyecto (
                    id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    descripcion TEXT NOT NULL,
                    fecha_inicio DATE NOT NULL,
                    fecha_fin DATE NOT NULL,
                    estado TEXT NOT NULL DEFAULT 'Pendiente'
                        CHECK (estado IN ('Pendiente', 'En proceso', 'Finalizado')),
                    pais TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleado (
                    rut TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    direccion TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    correo TEXT NOT NULL UNIQUE,
                    estado TEXT NOT NULL DEFAULT 'activo',
                    inicio_contrato DATE NOT NULL,
                    sueldo INTEGER NOT NULL CHECK (sueldo > 0),
                    cod_moneda TEXT NOT NULL DEFAULT 'CLP',
                    id_departamento INTEGER,
                    FOREIGN KEY (id_departamento)
                        REFERENCES departamento(id_departamento) ON DELETE SET NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transaccion (
                    id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
                    rut TEXT NOT NULL,
                    id_proyecto TEXT NOT NULL,
                    sueldo_emp REAL NOT NULL,
                    moneda_origen_clp TEXT NOT NULL,
                    sueldo_pagado REAL NOT NULL,
                    moneda_destino TEXT NOT NULL,
                    tasa_cambio REAL NOT NULL,
                    fecha_transaccion TEXT NOT NULL,
                    FOREIGN KEY (rut) REFERENCES empleado(rut),
                    FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tiempo (
                    id_tiempo INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    hora_entrada TEXT NOT NULL,
                    hora_salida TEXT NOT NULL,
                    pausa_minutos INTEGER NOT NULL DEFAULT 0,
                    rut_empleado TEXT NOT NULL,
                    id_proyecto INTEGER NOT NULL,
                    FOREIGN KEY (rut_empleado)
                        REFERENCES empleado(rut) ON DELETE CASCADE,
                    FOREIGN KEY (id_proyecto)
                        REFERENCES proyecto(id_proyecto) ON DELETE CASCADE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS informe (
                    id_informe INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha DATE NOT NULL,
                    tipo TEXT NOT NULL,
                    formato TEXT NOT NULL,
                    rut_empleado TEXT NOT NULL,
                    FOREIGN KEY (rut_empleado)
                        REFERENCES empleado(rut) ON DELETE CASCADE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    nombre_completo TEXT NOT NULL,
                    rol TEXT NOT NULL
                        CHECK (rol IN ('Administrador', 'Empleado')),
                    rut_empleado TEXT UNIQUE DEFAULT NULL,
                        FOREIGN KEY (rut_empleado)
                            REFERENCES empleado(rut) ON DELETE CASCADE,
                        CHECK (
                            (rol = 'Administrador' AND rut_empleado IS NULL)
                            OR
                            (rol = 'Administrador' AND rut_empleado IS NOT NULL)
                            OR
                            (rol = 'Empleado' AND rut_empleado IS NOT NULL)
                        )
                )
            """)

            # 1. Departamentos (Ventas + 2 nuevos)
            departamentos_seed = [ #datos de prueba (lista de tuplas que esperan para traducir datos de Python a filas de una tabla SQL.)
                ("Ventas", "Alejandro Guzmán"),
                ("Tecnología", "Camila Rojas"),
                ("Operaciones", "Matías Valenzuela"),
            ]

            cursor.executemany(
                """
                INSERT OR IGNORE INTO departamento (nombre, gerente)
                VALUES (?, ?)
                """,
                departamentos_seed,
            )

            # 2. Empleados (3 registros con RUT en mayúscula y fecha ISO YYYY-MM-DD)
            empleados_seed = [
                (
                    "18456321-9",
                    "Sofía Contreras",
                    "Av. O'Higgins 450, Concepción",
                    "+56981234567",
                    "sofia.contreras@ecotech.cl",
                    "activo",
                    "2025-03-01",
                    1450000,
                    "Tecnología",
                ),
                (
                    "19876543-2",
                    "Diego Morales",
                    "Calle Barros Arana 1020, Concepción",
                    "+56987654321",
                    "diego.morales@ecotech.cl",
                    "activo",
                    "2025-06-15",
                    1250000,
                    "Tecnología",
                ),
                (
                    "20123456-K",
                    "Valentina Muñoz",
                    "Los Carrera 780, Chillán",
                    "+56976543210",
                    "valentina.munoz@ecotech.cl",
                    "activo",
                    "2026-01-10",
                    1100000,
                    "Operaciones",
                ),
                ("17654321-3", "Matías Henríquez", "Pedro de Valdivia 321, Concepción", "+56965432109",
                 "matias.henriquez@ecotech.cl", "activo", "2024-02-01", 1350000, "Operaciones"),
                ("16789012-1", "Javiera Soto", "Orompello 150, Concepción", "+56954321098",
                 "javiera.soto@ecotech.cl", "activo", "2023-08-14", 1600000, "Tecnología"),
                ("15432109-8", "Tomás Fuentes", "Av. Collao 890, Concepción", "+56943210987",
                 "tomas.fuentes@ecotech.cl", "vacaciones", "2025-01-20", 980000, "Operaciones"),
                ("21345678-4", "Paula Riquelme", "Arturo Prat 77, Chillán", "+56932109876",
                 "paula.riquelme@ecotech.cl", "suspendido", "2024-11-04", 1050000, "Ventas"),
                ("14876543-K", "Rodrigo Vera", "Maipú 410, Los Ángeles", "+56921098765",
                 "rodrigo.vera@ecotech.cl", "inactivo", "2023-03-06", 900000, "Ventas"),
            ]
            cursor.executemany(
                """
                INSERT OR IGNORE INTO empleado (
                    rut, nombre, direccion, telefono, correo,
                    estado, inicio_contrato, sueldo, id_departamento
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?,
                    (SELECT id_departamento FROM departamento WHERE nombre = ?)
                )
                """,
                empleados_seed,
            )

            # 3. Proyectos (3 registros con estados válidos del CHECK)
            proyectos_seed = [
                (
                    "Portal Web EcoTech",
                    "Desarrollo de plataforma interna de gestión y reportes",
                    "2026-01-15",
                    "2026-12-20",
                    "En proceso",
                    "Argentina",
                ),
                (
                    "App Móvil Terreno",
                    "Aplicación para registro de asistencia y horas en obra",
                    "2026-03-01",
                    "2026-11-30",
                    "En proceso",
                    "Francia",
                ),
                (
                    "Auditoría Energética 2026",
                    "Levantamiento de indicadores ambientales en sucursales",
                    "2026-12-01",
                    "2027-03-31",
                    "Pendiente",
                    "Chile",
                ),
                ("Parque Solar Texas", "Instalación de paneles solares en parque industrial",
                 "2026-02-01", "2027-02-01", "En proceso", "Estados Unidos"),
                ("Planta Eólica Andalucía", "Montaje de aerogeneradores en zona costera",
                 "2026-05-01", "2027-05-01", "En proceso", "España"),
                ("Red Solar Osaka", "Mantención de red solar urbana (proyecto cerrado)",
                 "2025-09-01", "2026-09-30", "Finalizado", "Japón"),
                ("Biomasa Brasil", "Estudio de factibilidad de planta de biomasa",
                 "2027-01-10", "2027-09-30", "Pendiente", "Brasil"),
            ]
            cursor.executemany(
                """
                INSERT OR IGNORE INTO proyecto (
                    nombre, descripcion, fecha_inicio, fecha_fin, estado, pais
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                proyectos_seed,
            )


            # 4. Registros de tiempo (vinculan empleados con proyectos; sin ellos no hay pagos).
            #    Se usa INSERT ... WHERE NOT EXISTS porque init_db() corre en cada arranque
            #    y la tabla 'tiempo' no tiene UNIQUE: así no se duplican los registros.
            tiempos_seed = [
                # (fecha, entrada, salida, pausa, rut, proyecto)
                # Parque Solar Texas (USD): 2 activos + 1 suspendido
                ("2026-11-02", "08:00", "17:00", 60, "18456321-9", "Parque Solar Texas"),
                ("2026-11-03", "08:00", "17:00", 60, "18456321-9", "Parque Solar Texas"),
                ("2026-11-02", "09:00", "18:00", 60, "19876543-2", "Parque Solar Texas"),
                ("2026-11-02", "08:00", "16:00", 30, "21345678-4", "Parque Solar Texas"),
                # Planta Eólica Andalucía (EUR): Diego trabaja en 2 proyectos; Tomás de vacaciones
                ("2026-11-04", "08:00", "17:00", 60, "19876543-2", "Planta Eólica Andalucía"),
                ("2026-11-04", "08:30", "17:30", 60, "20123456-K", "Planta Eólica Andalucía"),
                ("2026-11-05", "08:30", "17:30", 60, "20123456-K", "Planta Eólica Andalucía"),
                ("2026-11-04", "08:00", "16:00", 30, "15432109-8", "Planta Eólica Andalucía"),
                # Red Solar Osaka (JPY, finalizado): Rodrigo ahora inactivo
                ("2026-08-10", "08:00", "17:00", 60, "17654321-3", "Red Solar Osaka"),
                ("2026-08-11", "08:00", "17:00", 60, "16789012-1", "Red Solar Osaka"),
                ("2026-08-10", "08:00", "17:00", 60, "14876543-K", "Red Solar Osaka"),
                # Proyectos en Chile (CLP, sin conversión)
                ("2026-11-09", "09:00", "18:00", 60, "18456321-9", "Portal Web EcoTech"),
                ("2026-11-09", "09:00", "18:00", 60, "16789012-1", "Portal Web EcoTech"),
                ("2026-11-10", "08:00", "17:00", 60, "17654321-3", "App Móvil Terreno"),
                ("2026-11-10", "08:00", "17:00", 60, "20123456-K", "App Móvil Terreno"),
                # 'Biomasa Brasil' y 'Auditoría Energética 2026' quedan SIN empleados a propósito
            ]
            cursor.executemany(
                """
                INSERT INTO tiempo (fecha, hora_entrada, hora_salida, pausa_minutos,
                                    rut_empleado, id_proyecto)
                SELECT :fecha, :entrada, :salida, :pausa, :rut,
                       (SELECT id_proyecto FROM proyecto WHERE nombre = :proyecto)
                WHERE EXISTS (SELECT 1 FROM proyecto WHERE nombre = :proyecto)
                  AND EXISTS (SELECT 1 FROM empleado WHERE rut = :rut)
                  AND NOT EXISTS (
                      SELECT 1 FROM tiempo
                      WHERE rut_empleado = :rut AND fecha = :fecha
                        AND hora_entrada = :entrada
                        AND id_proyecto = (SELECT id_proyecto FROM proyecto WHERE nombre = :proyecto)
                  )
                """,
                [
                    {"fecha": f, "entrada": e, "salida": s, "pausa": p, "rut": r, "proyecto": n}
                    for (f, e, s, p, r, n) in tiempos_seed
                ],
            )

            conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")
            return False
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    if Database().init_db():
        print("Base de datos inicializada correctamente.")
    else:
        print("Base de datos no inicializada")