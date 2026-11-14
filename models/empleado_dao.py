from sqlite3 import Cursor
import sqlite3
from datetime import date
from typing import Optional

from config.database import Database
from models.empleado import Empleado


class EmpleadoDAO:
    """
    Data Access Object para la entidad Empleado.
    Maneja todas las operaciones CRUD en la base de datos.
    """
    @staticmethod
    def agregar_empleado(empleado: Empleado) -> bool: # en proceso TO_DATE('variable','DD-MM-YYYY')
        """
        Agrega un nuevo empleado a la base de datos.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO empleado (rut, nombre, direccion, telefono, correo, id_departamento, sueldo, inicio_contrato, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, 
                (
                    empleado.rut, empleado.nombre, empleado.direccion, empleado.telefono,
                    empleado.correo, empleado.id_departamento, 
                    empleado.sueldo, empleado.inicio_contrato, empleado.estado
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

        return  Empleado(
            sueldo=fila["sueldo"],
            inicio_contrato= inicio_contrato,
            estado=fila["estado"],
            rut=fila["rut"],
            nombre=fila["nombre"],
            direccion=fila["direccion"],
            telefono=fila["telefono"],
            correo=fila["correo"],
            id_departamento=fila["id_departamento"],
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
                SELECT sueldo, inicio_contrato, estado, rut, nombre, 
                        direccion, telefono, correo, id_departamento
                FROM empleado
                ORDER BY nombre
                """
            )
            return [EmpleadoDAO.crear_empleado(fila) for fila in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def obtener_todos_empleado_estado(estado: str) -> list[Empleado]:
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT e.sueldo, e.inicio_contrato, e.estado,
                    e.rut, e.nombre, e.direccion,
                    e.telefono, e.correo, e.id_departamento
                FROM empleado AS e
                WHERE e.estado = ?
                ORDER BY e.nombre
                """,
                (estado,),
            )

            return [
                EmpleadoDAO.crear_empleado(fila)
                for fila in cursor.fetchall()
            ]

        except sqlite3.Error as e:
            print(f"Error al obtener empleados: {e}")
            return []
        finally:
            conn.close()
    
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
                SELECT sueldo, inicio_contrato, estado, rut, nombre, direccion, telefono, correo,
                        id_departamento
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
                    estado = ?
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
                WHERE rut = ? AND estado = 'activo'
            """, (empleado.rut,empleado.estado))
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

    @staticmethod
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