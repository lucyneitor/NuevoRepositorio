from sqlite3 import Cursor
from datetime import date
from typing import Optional

from config.database import Database
from models.tiempo import Tiempo


class TiempoDAO:
    """
    Data Access Object para la entidad Tiempo
    Maneja todas las operaciones CRUD en la base de datos.
    """
    @staticmethod
    def agregar_tiempo(tiempo: Tiempo) -> bool:
        """
        Agrega un nuevo tiempo a la base de datos.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tiempo (fecha, hora_entrada, hora_salida, id_empleado, id_proyecto, pausa_minutos)
                VALUES (?, ?, ?, ?, ?, ?)
                """, 
                (
                    tiempo.fecha, tiempo.hora_entrada, tiempo.hora_salida, tiempo.id_empleado,
                    tiempo.id_proyecto, tiempo.pausa_minutos
                )
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar tiempo en BD: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def crear_tiempo(fila) -> Tiempo:
        
        return Tiempo(
            id_tiempo=fila["id_tiempo"],
            fecha=fila["fecha"],
            hora_entrada=fila["hora_entrada"],
            hora_salida=fila["hora_salida"],
            id_empleado=fila["rut"],
            id_proyecto=fila["id_proyecto"],
            pausa_minutos=fila["pausa_minutos"],
        )


    @staticmethod
    def obtener_todos_tiempos() -> list[Tiempo]: #corregir si hay error
               """
               Obtiene todos los registros de tiempo de la base de datos.
               """
               conn = Database().get_connection()
               try:
                   cursor: Cursor = conn.cursor()
                   cursor.execute(
                       """
                        SELECT t.id_tiempo, t.fecha, t.hora_entrada, t.hora_salida,
                        e.rut, p.nombre, t.pausa_minutos
                        FROM tiempo t
                        JOIN empleado e ON e.id_empleado = t.id_empleado
                        JOIN proyecto p ON p.id_proyecto = t.id_proyecto
                        ORDER BY p.nombre, t.fecha, t.hora_entrada
                       """
                   )
                   return [TiempoDAO.crear_tiempo(fila) for fila in cursor.fetchall()]
               finally:
                   conn.close()
    
    @staticmethod
    def obtener_todos_tiempos_rut(rut:str) -> list[Tiempo]:
        """
        Obtiene todos los registros de tiempo de la base de datos.
        """
        conn = Database().get_connection()
        tiempos = {}
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT t.fecha, t.hora_entrada, t.hora_salida,
                e.rut, p.nombre, t.pausa_minutos
                FROM tiempo t
                JOIN empleado e ON e.id_empleado = t.id_empleado
                JOIN proyecto p ON p.id_proyecto = t.id_proyecto
                ORDER BY t.fecha, t.hora_entrada, p.id_proyecto
                """
            )
            filas = cursor.fetchall()
            for fila in filas:
                tiempos.append(Tiempo(fila['fecha'], fila['hora_entrada'], fila['hora_salida'], fila['rut'], fila['sueldo'], fila['inicio_contrato'])) 
        finally:
            conn.close()

    @staticmethod
    def contar_tiempos() -> int:
        conn = Database().get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tiempo")
            return cursor.fetchone()[0]
        finally:
            conn.close()