import sqlite3
from sqlite3 import Cursor

from config.database import Database
from models.departamento import Departamento
from models.empleado import Empleado


class DepartamentoDAO:
    """
    Data Access Object para la entidad Departamento.
    Maneja las operaciones CRUD en la base de datos.
    Cada método: abre la conexión dentro de try, captura los errores de sqlite3
    y cierra la conexión en finally. Si ocurre un error antes del commit,
    los cambios pendientes se descartan automáticamente al cerrar la conexión.
    """

    @staticmethod
    def crear(departamento: Departamento) -> bool:
        conn = None
        try:
            conn = Database().get_connection()
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO departamento (nombre, gerente) VALUES (?, ?)",
                (departamento.nombre, departamento.gerente)
            )
            conn.commit()
            departamento.id_departamento = cursor.lastrowid
            return True
        except sqlite3.IntegrityError:
            print("Error: ya existe un departamento con ese nombre.")
            return False
        except sqlite3.Error as e:
            print(f"Error al crear departamento en BD: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def obtener_todos() -> list[Departamento]:
        conn = None
        departamentos = []
        try:
            conn = Database().get_connection()
            cursor: Cursor = conn.cursor()
            cursor.execute("SELECT id_departamento, nombre, gerente FROM departamento ORDER BY id_departamento")
            for fila in cursor.fetchall():
                departamentos.append(Departamento(fila['id_departamento'],fila['nombre'], fila['gerente']))
        except sqlite3.Error as e:
            print(f"Error al obtener departamentos: {e}")
        finally:
            if conn:
                conn.close()
        return departamentos

    @staticmethod
    def obtener_por_id(id_departamento: int) -> Departamento | None:
        conn = None
        departamento = None
        try:
            conn = Database().get_connection()
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "SELECT id_departamento, nombre, gerente FROM departamento WHERE id_departamento = ?",
                (id_departamento,)
            )
            fila = cursor.fetchone()
            if fila:
                departamento = Departamento(fila['id_departamento'], fila['nombre'], fila['gerente'])
        except sqlite3.Error as e:
            print(f"Error al obtener el departamento: {e}")
        finally:
            if conn:
                conn.close()
        return departamento

    @staticmethod
    def actualizar(departamento: Departamento) -> bool:
        if departamento.id_departamento is None:
            return False
        conn = None
        try:
            conn = Database().get_connection()
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "UPDATE departamento SET nombre = ?, gerente = ? WHERE id_departamento = ?",
                (departamento.nombre, departamento.gerente, departamento.id_departamento)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            print("Error: ya existe otro departamento con ese nombre.")
            return False
        except sqlite3.Error as e:
            print(f"Error al actualizar departamento: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def eliminar(id_departamento: int) -> bool:
        conn = None
        try:
            conn = Database().get_connection()
            cursor: Cursor = conn.cursor()
            # Los empleados del departamento quedan sin departamento (ON DELETE SET NULL).
            cursor.execute("DELETE FROM departamento WHERE id_departamento = ?", (id_departamento,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar departamento: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def contar_empleados(id_departamento: int) -> int:
        conn = None
        try:
            conn = Database().get_connection()
            cursor: Cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM empleado WHERE id_departamento = ?", (id_departamento,))
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error al contar empleados: {e}")
            return 0
        finally:
            if conn:
                conn.close()

    @staticmethod
    def contar_departamentos() -> int:
        conn = None
        try:
            conn = Database().get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM departamento")
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error al contar departamentos: {e}")
            return 0
        finally:
            if conn:
                conn.close()

    @staticmethod
    def obtener_nombre(nombre: str) -> Departamento | None:
        """Busca un departamento por su nombre."""

        conn = None

        try:
            conn = Database().get_connection()
            cursor: Cursor = conn.cursor()

            cursor.execute("""
                SELECT id_departamento, nombre, gerente
                FROM departamento
                WHERE nombre = ? COLLATE NOCASE
            """, (nombre.strip(),))

            fila = cursor.fetchone()

            if fila:
                return Departamento(
                    id_departamento=fila["id_departamento"],
                    nombre=fila["nombre"],
                    gerente=fila["gerente"]
                )

            return None

        except sqlite3.Error as error:
            raise RuntimeError(
                f"Error al buscar departamento: {error}"
            ) from error

        finally:
            if conn:
                conn.close()

    
    @staticmethod
    def obtener_gerente(gerente: str) -> list[dict]:
        """Busca los departamentos asociados a un gerente."""

        conn = None

        try:
            conn = Database().get_connection()
            cursor: Cursor = conn.cursor()

            cursor.execute("""
                SELECT id_departamento, nombre
                FROM departamento
                WHERE gerente = ? COLLATE NOCASE
                ORDER BY nombre
            """, (gerente.strip(),))

            filas = cursor.fetchall()

            return [
                {
                    "id_departamento": fila["id_departamento"],
                    "nombre": fila["nombre"]
                }
                for fila in filas
            ]

        except sqlite3.Error as error:
            raise RuntimeError(
                f"Error al buscar departamentos por gerente: {error}"
            ) from error

        finally:
            if conn:
                conn.close()

    
    @staticmethod
    def verificar_depa_gerente(
        nombre: str,
        gerente: str
    ) -> tuple[bool, list]:

        conn = None

        try:
            conn = Database().get_connection()
            cursor: Cursor = conn.cursor()

            # Verificar que exista el departamento y coincida su gerente.
            cursor.execute("""
                SELECT id_departamento
                FROM departamento
                WHERE nombre = ? COLLATE NOCASE
                AND gerente = ? COLLATE NOCASE
            """, (nombre.strip(), gerente.strip()))

            fila = cursor.fetchone()

            if fila is None:
                return False, []

            id_departamento = fila["id_departamento"]

            # Recuperar los empleados asociados.
            cursor.execute("""
                SELECT *
                FROM empleado
                WHERE id_departamento = ?
                ORDER BY nombre
            """, (id_departamento,))

            filas = cursor.fetchall()

            empleados = [
                Empleado(
                    sueldo=fila["sueldo"],
                    inicio_contrato=fila["inicio_contrato"],
                    estado=fila["estado"],
                    rut=fila["rut"],
                    nombre=fila["nombre"],
                    direccion=fila["direccion"],
                    telefono=fila["telefono"],
                    correo=fila["correo"],
                    id_departamento=fila["id_departamento"]
                )
                for fila in filas
            ]

            return True, empleados

        except sqlite3.Error as error:
            raise RuntimeError(
                f"Error al verificar departamento y gerente: {error}"
            ) from error

        finally:
            if conn:
                conn.close()
