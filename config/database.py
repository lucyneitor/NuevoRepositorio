import sqlite3
from pathlib import Path
from sqlite3 import Connection, Cursor


class Database:
    """
    Singleton para manejar la conexión a SQLite.
    Modela la herencia: Persona -> Empleado
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
                    fecha_inicio_contrato DATE NOT NULL,
                    salario INTEGER NOT NULL CHECK (salario > 0),
                    id_departamento INTEGER,
                    FOREIGN KEY (id_departamento)
                        REFERENCES departamento(id_departamento) ON DELETE SET NULL
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
                    rol TEXT NOT NULL,
                )
            """)

            cursor.execute(
                """
                INSERT OR IGNORE INTO departamento (nombre, gerente)
                VALUES (?, ?)
                """,
                ("Ventas", "Alejandro Guzmán")
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