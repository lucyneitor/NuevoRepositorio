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

            # 1) Persona
            cursor.execute("""
                CREATE TABLE empleado (
                    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                    rut TEXT NOT NULL UNIQUE,
                    nombre TEXT NOT NULL,
                    direccion TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    correo TEXT NOT NULL UNIQUE,
                    user TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    rol_admin BOOLEAN NOT NULL DEFAULT 0,
                    estado TEXT NOT NULL DEFAULT 'activo',
                    fecha_inicio_contrato DATE NOT NULL,
                    salario INTEGER NOT NULL CHECK (salario > 0),
                    id_departamento INTEGER,
                    FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento) ON DELETE SET NULL
                );
            """)

            # 2) Departamento
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departamento (
                    id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    gerente TEXT
                );
            """)

            # 3) Proyecto
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proyecto (
                    id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    descripcion TEXT NOT NULL,
                    fecha_inicio DATE NOT NULL,
                );
            """)

            # 4) Tiempo
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tiempo (
                    id_tiempo INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha DATE NOT NULL,
                    horas_realizadas INTEGER NOT NULL,
                    id_empleado INTEGER NOT NULL,
                    id_proyecto INTEGER NOT NULL,
                    descripcion TEXT,
                    FOREIGN KEY(id_empleado) REFERENCES empleado(id_empleado) ON DELETE CASCADE,
                    FOREIGN KEY(id_proyecto) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE
                );
            """)

            # 5) Informe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS informe (
                    id_informe INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha DATE NOT NULL,
                    tipo TEXT NOT NULL,
                    formato TEXT NOT NULL,
                    id_empleado INTEGER NOT NULL,
                    FOREIGN KEY(id_empleado) REFERENCES empleado(id_empleado) ON DELETE CASCADE
                )
            """)
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