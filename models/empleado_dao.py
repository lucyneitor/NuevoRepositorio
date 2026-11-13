from sqlite3 import Cursor
from datetime import date
from typing import Optional

from config.database import Database
from models.empleado import Empleado


class EmpleadoDAO:
    """
    Data Access Object para la entidad Paciente.
    Maneja todas las operaciones CRUD en la base de datos.
    """
    @staticmethod
    def agregar_empleado(empleado: Empleado) -> bool:
        """
        Agrega un nuevo empleado a la base de datos.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO empleado (rut, nombre, direccion, telefono, correo, id_departamento, sueldo, inicio_contrato, rol_admin, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, 
                (
                    empleado.rut, empleado.nombre, empleado.direccion, empleado.telefono,
                    empleado.correo, empleado.id_departamento, 
                    empleado.sueldo, empleado.inicio_contrato, empleado.rol_admin, empleado.estado
                )
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar empleado en BD: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def crear_empleado(fila) -> Empleado:
        inicio_contrato = fila["inicio_contrato"]
        if isinstance(inicio_contrato, str):
            inicio_contrato = date.fromisoformat(inicio_contrato)

        return Empleado(
            fila["id_departamento"],
            fila["sueldo"],
            inicio_contrato,
            fila["rut"],
            fila["nombre"],
            fila["direccion"],
            fila["telefono"],
            fila["correo"],
            bool(fila["rol_admin"]),
            fila["estado"],
        )

    @staticmethod
    def obtener_todos_empleados() -> list[Empleado]:
        """
        Obtiene todos los empleados de la base de datos.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT rut, nombre, direccion, telefono, correo,
                       id_departamento, sueldo, inicio_contrato, rol_admin, estado
                FROM empleado
                ORDER BY nombre
                """
            )
            return [EmpleadoDAO.crear_empleado(fila) for fila in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def obtener_todos_empleado_estado(estado: str) -> list[Empleado]:
        """
        Obtiene todos los empleados de la base de datos por su estado.
        """
        conn = Database().get_connection()
        empleados = []
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT rut, nombre, correo, d.nombre, sueldo, inicio_contrato, estado 
                FROM empleado e, departamento d 
                WHERE e.id_departamento = d.id_departamento 
                AND estado = ?
                """,
                (estado,)
            )
            filas = cursor.fetchall()
            for fila in filas:
                empleados.append(Empleado(fila['rut'], fila['nombre'], fila['correo'], fila['nombre_departamento'], fila['sueldo'], fila['inicio_contrato'])) 
        except Exception as e:
            print(f"Error al obtener empleados por estado de BD: {e}")
        finally:
            conn.close()
        return empleados
    
    @staticmethod
    def obtener_empleado_por_rut(rut: str) -> Optional[Empleado]:
        """
        Obtiene un empleado de la base de datos por su RUT.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT rut, nombre, direccion, telefono, correo,
                       id_departamento, sueldo, inicio_contrato, rol_admin, estado
                FROM empleado
                WHERE rut = ?
                """,
                (rut,),
            )
            fila = cursor.fetchone()
            return EmpleadoDAO.crear_empleado(fila) if fila else None
        finally:
            conn.close()

    @staticmethod
    def obtener_empleado_por_user(credencial: dict) -> bool: #bajo observación de modificarlo
        """
        Retorna True si encuentra el usuario en la base de datos; False si no existe.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 1
                FROM empleado
                WHERE user = ? AND password = ?
                """,
                (credencial["usuario"],credencial["contraseña"]),
            )
            encontrado = cursor.fetchone()
            return encontrado is not None
        finally:
            conn.close()

    @staticmethod
    def obtener_estado(user:str)->bool: #observación de traslado a user
        conn = Database().get_connection()
        try:
            cursor : Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT rol_admin
                FROM empleado
                WHERE user = ?
                """,
                (user,),
            )
            rol = cursor.fetchone()
            return rol
        finally:
            conn.close()
    
    @staticmethod
    def actualizar_empleado(empleado: Empleado) -> bool:
        """
        Actualiza los datos de un empleado en la base de datos.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE empleado
                SET nombre = ?, direccion = ?, telefono = ?, correo = ?,
                    id_departamento = ?, sueldo = ?, inicio_contrato = ?,
                    rol_admin = ?, estado = ?
                WHERE rut = ?
                """,
                (
                    empleado.nombre,
                    empleado.direccion,
                    empleado.telefono,
                    empleado.correo,
                    empleado.id_departamento,
                    empleado.sueldo,
                    empleado.inicio_contrato.isoformat(),
                    empleado.rol_admin,
                    empleado.estado,
                    empleado.rut,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod # revisar
    def eliminar_empleado(empleado:Empleado) -> bool:
        """
        Elimina un empleado de la base de datos por su RUT.
        """
        conn = Database().get_connection()
        cursor: Cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE empleado
                SET estado = 'inactivo'
                WHERE rut = ?
            """, (empleado.rut,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar empleado de BD: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def contar_empleados() -> int:
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM empleado")
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def esta_empleado(rut:str)->bool:
        conn = Database().get_connection()
        cursor: Cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT estado
                FROM empleado
                WHERE rut = ?
            """, (rut,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar empleado de BD: {e}")
            return False
        finally:
            conn.close()