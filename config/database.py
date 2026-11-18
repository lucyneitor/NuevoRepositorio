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
                    pais TEXT NOT NULL,
                    estado TEXT NOT NULL DEFAULT 'Pendiente'
                        CHECK (estado IN ('Pendiente', 'En proceso', 'Finalizado'))
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
                    id_departamento INTEGER,
                    FOREIGN KEY (id_departamento)
                        REFERENCES departamento(id_departamento) ON DELETE SET NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pagos (
                    id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
                    rut TEXT NOT NULL,
                    id_proyecto TEXT NOT NULL,
                    sueldo_base REAL NOT NULL,
                    moneda_origen TEXT NOT NULL,
                    sueldo_pagado REAL NOT NULL,
                    moneda_destino TEXT NOT NULL,
                    tasa_cambio REAL NOT NULL,
                    fecha_transaccion TEXT NOT NULL,
                    FOREIGN KEY (rut) REFERENCES empleados(rut),
                    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto)
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
                ),
                (
                    "App Móvil Terreno",
                    "Aplicación para registro de asistencia y horas en obra",
                    "2026-03-01",
                    "2026-11-30",
                    "En proceso",
                ),
                (
                    "Auditoría Energética 2026",
                    "Levantamiento de indicadores ambientales en sucursales",
                    "2026-12-01",
                    "2027-03-31",
                    "Pendiente",
                ),
            ]
            cursor.executemany(
                """
                INSERT OR IGNORE INTO proyecto (
                    nombre, descripcion, fecha_inicio, fecha_fin, estado
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                proyectos_seed,
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