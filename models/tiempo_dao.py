import sqlite3
from datetime import date, time
from sqlite3 import Cursor
from typing import Any

from config.database import Database
from models.tiempo import Tiempo


class TiempoDAO:
    """
    Operaciones de acceso a datos para los registros de tiempo.
    """

    @staticmethod
    def _texto_fecha(valor: date | str) -> str:
        return valor.isoformat() if isinstance(valor, date) else str(valor).strip()

    @staticmethod
    def _texto_hora(valor: time | str) -> str:
        return valor.isoformat() if isinstance(valor, time) else str(valor).strip()

    @staticmethod
    def _obtener_id_empleado(cursor: Cursor, rut: str) -> int | None:
        """Busca el ID numérico del empleado a partir de su RUT."""
        cursor.execute(
            "SELECT id_empleado FROM empleado WHERE rut = ?",
            (rut,),
        )
        fila = cursor.fetchone()
        return fila["id_empleado"] if fila else None

    @staticmethod
    def crear_tiempo(fila: Any) -> Tiempo:
        """
        Convierte una fila consultada en un objeto Tiempo.
        """
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
    def _consultar_filas(
        condicion: str = "",
        parametros: tuple = (),
    ) -> list[Any]:
        """
        Consulta registros, incluyendo el nombre del proyecto.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            consulta = """
                SELECT t.id_tiempo, t.fecha, t.hora_entrada, t.hora_salida,
                       t.id_proyecto, e.rut, p.nombre AS nombre_proyecto,
                       t.pausa_minutos
                FROM tiempo AS t
                JOIN empleado AS e ON e.id_empleado = t.id_empleado
                JOIN proyecto AS p ON p.id_proyecto = t.id_proyecto
            """
            if condicion:
                consulta += f" WHERE {condicion}"

            consulta += """
                ORDER BY p.nombre, t.fecha, t.hora_entrada
            """
            cursor.execute(consulta, parametros)
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def agregar_tiempo(tiempo: Tiempo) -> bool:
        """Inserta un registro. SQLite genera id_tiempo automáticamente."""
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()

            id_empleado = TiempoDAO._obtener_id_empleado(
                cursor,
                tiempo.id_empleado,
            )
            if id_empleado is None:
                print(f"No se encontró un empleado con RUT {tiempo.id_empleado}.")
                return False

            cursor.execute(
                """
                INSERT INTO tiempo (
                    fecha, hora_entrada, hora_salida,
                    id_empleado, id_proyecto, pausa_minutos
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    TiempoDAO._texto_fecha(tiempo.fecha),
                    TiempoDAO._texto_hora(tiempo.hora_entrada),
                    TiempoDAO._texto_hora(tiempo.hora_salida),
                    id_empleado,
                    tiempo.id_proyecto,
                    tiempo.pausa_minutos,
                ),
            )

            tiempo.id_tiempo = cursor.lastrowid
            conn.commit()
            return True

        except sqlite3.Error as error:
            conn.rollback()
            print(f"Error al agregar tiempo en BD: {error}")
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_todos_tiempos() -> list[Tiempo]:
        """Obtiene todos los registros como objetos Tiempo."""
        try:
            filas = TiempoDAO._consultar_filas()
            return [TiempoDAO.crear_tiempo(fila) for fila in filas]
        except (sqlite3.Error, KeyError, TypeError, ValueError) as error:
            print(f"Error al consultar tiempos: {error}")
            return []

    @staticmethod
    def obtener_todos_tiempos_con_nombre_proyecto() -> list[dict[str, object]]:
        """
        Obtiene los tiempos junto al nombre del proyecto para mostrarlos.
        El nombre no se guarda en la tabla tiempo: se consulta mediante JOIN.
        """
        try:
            filas = TiempoDAO._consultar_filas()
            return [
                {
                    "tiempo": TiempoDAO.crear_tiempo(fila),
                    "nombre_proyecto": fila["nombre_proyecto"],
                }
                for fila in filas
            ]
        except (sqlite3.Error, KeyError, TypeError, ValueError) as error:
            print(f"Error al consultar tiempos con proyecto: {error}")
            return []

    @staticmethod
    def obtener_todos_tiempos_rut(rut: str) -> list[Tiempo]:
        """Obtiene los registros de tiempo de un empleado identificado por RUT."""
        try:
            filas = TiempoDAO._consultar_filas(
                "e.rut = ?",
                (rut,),
            )
            return [TiempoDAO.crear_tiempo(fila) for fila in filas]
        except (sqlite3.Error, KeyError, TypeError, ValueError) as error:
            print(f"Error al consultar tiempos del empleado: {error}")
            return []

    @staticmethod
    def obtener_tiempos_proyect(id:int) -> list[Tiempo]:
        """
        Obtiene los registros de tiempo de un proyecto especifico."""
        try:
            filas = TiempoDAO._consultar_filas(
                "t.id_proyecto = ?",
                (id,),
            )
            return [TiempoDAO.crear_tiempo(fila) for fila in filas]
        except (sqlite3.Error, KeyError, TypeError, ValueError) as error:
            print(f"Error al consultar tiempos del empleado: {error}")
            return []

    @staticmethod
    def obtener_todos_tiempos_rut_proyect(rut: str, id:int) -> list[Tiempo]:
            """Obtiene los registros de tiempo de un empleado identificado por RUT."""
            try:
                filas = TiempoDAO._consultar_filas(
                    "e.rut = ? AND t.id_proyecto = ?",
                    (rut,id),
                )
                return [TiempoDAO.crear_tiempo(fila) for fila in filas]
            except (sqlite3.Error, KeyError, TypeError, ValueError) as error:
                print(f"Error al consultar tiempos del empleado: {error}")
                return []

    @staticmethod
    def obtener_tiempos_por_fecha(fecha: date | str) -> list[Tiempo]:
        """
        Obtiene los registros de una fecha específica.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            fecha_busqueda = fecha.isoformat() if isinstance(fecha, date) else fecha.strip()

            cursor.execute(
                """
                SELECT t.id_tiempo, t.fecha, t.hora_entrada, t.hora_salida,
                        t.id_proyecto, e.rut, t.pausa_minutos
                FROM tiempo AS t
                JOIN empleado AS e ON e.id_empleado = t.id_empleado
                WHERE t.fecha = ?
                ORDER BY t.hora_entrada
                """,
                (fecha_busqueda,),
            )

            filas = cursor.fetchall()
            return [TiempoDAO.crear_tiempo(fila) for fila in filas]
        finally:
            conn.close()

    @staticmethod
    def obtener_tiempos_por_intervalo(
            fecha_inicio: date | str,
            fecha_fin: date | str,
        ) -> list[Tiempo]:
        """
        Obtiene los registros entre dos fechas, incluyéndolas.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            inicio = (
                fecha_inicio.isoformat()
                if isinstance(fecha_inicio, date)
                else fecha_inicio.strip()
            )
            fin = (
                fecha_fin.isoformat()
                if isinstance(fecha_fin, date)
                else fecha_fin.strip()
            )

            cursor.execute(
                """
                SELECT t.id_tiempo, t.fecha, t.hora_entrada, t.hora_salida,
                    t.id_proyecto, e.rut, t.pausa_minutos
                FROM tiempo AS t
                JOIN empleado AS e ON e.id_empleado = t.id_empleado
                WHERE t.fecha BETWEEN ? AND ?
                ORDER BY t.fecha, t.hora_entrada
                """,
                (inicio, fin),
            )

            filas = cursor.fetchall()
            return [TiempoDAO.crear_tiempo(fila) for fila in filas]
        finally:
            conn.close()

    @staticmethod
    def obtener_tiempo_por_id(id_tiempo: int) -> Tiempo | None:
        """Obtiene un registro por su ID; devuelve None si no existe."""
        try:
            filas = TiempoDAO._consultar_filas(
                "t.id_tiempo = ?",
                (id_tiempo,),
            )
            return TiempoDAO.crear_tiempo(filas[0]) if filas else None
        except (sqlite3.Error, KeyError, TypeError, ValueError) as error:
            print(f"Error al consultar el tiempo: {error}")
            return None

    @staticmethod
    def actualizar_tiempo(tiempo: Tiempo) -> bool:
        """Actualiza un registro existente."""
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()

            id_empleado = TiempoDAO._obtener_id_empleado(
                cursor,
                tiempo.id_empleado,
            )
            if id_empleado is None:
                print(f"No se encontró un empleado con RUT {tiempo.id_empleado}.")
                return False

            cursor.execute(
                """
                UPDATE tiempo
                SET fecha = ?, hora_entrada = ?, hora_salida = ?,
                    id_empleado = ?, id_proyecto = ?, pausa_minutos = ?
                WHERE id_tiempo = ?
                """,
                (
                    TiempoDAO._texto_fecha(tiempo.fecha),
                    TiempoDAO._texto_hora(tiempo.hora_entrada),
                    TiempoDAO._texto_hora(tiempo.hora_salida),
                    id_empleado,
                    tiempo.id_proyecto,
                    tiempo.pausa_minutos,
                    tiempo.id_tiempo,
                ),
            )

            conn.commit()
            return cursor.rowcount > 0

        except sqlite3.Error as error:
            conn.rollback()
            print(f"Error al actualizar tiempo en BD: {error}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar_tiempo(id_tiempo: int) -> bool:
        """Elimina un registro por su ID."""
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM tiempo WHERE id_tiempo = ?",
                (id_tiempo,),
            )
            conn.commit()
            return cursor.rowcount > 0

        except sqlite3.Error as error:
            conn.rollback()
            print(f"Error al eliminar tiempo en BD: {error}")
            return False
        finally:
            conn.close()

    @staticmethod
    def contar_tiempos() -> int:
        """
        Devuelve la cantidad de registros de tiempo.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tiempo")
            return cursor.fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def contar_tiempos_rut(rut:str) -> int:
        """
        Devuelve la cantidad de registros de tiempo.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM tiempo t
                JOIN empleado e ON e.id_empleado = t.id_empleado
                WHERE e.rut = ?
                """,
                (rut,),)
            return cursor.fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def contar_tiempos_nom_proyect(nom:str) -> int:
        """
        Devuelve la cantidad de registros de tiempo.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM tiempo t
                JOIN proyecto p ON p.id_proyecto = t.id_proyecto
                WHERE p.nombre = ?
                """,
                (nom,),)
            return cursor.fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def contar_tiempos_rut_proyect(rut:str,nom:str) -> int:
        """
        Devuelve la cantidad de registros de tiempo.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM tiempo t
                JOIN empleado e ON e.id_empleado = t.id_empleado
                JOIN proyecto p ON p.id_proyecto = t.id_proyecto
                WHERE e.rut = ? AND p.nombre = ?
                """,
                (rut,nom),)
            return cursor.fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def contar_tiempos_por_fecha(fecha: date | str) -> int:
        """
        Cuenta los registros de una fecha específica.
        """
        fecha_busqueda = fecha.isoformat() if isinstance(fecha, date) else fecha.strip()

        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM tiempo WHERE fecha = ?",
                (fecha_busqueda,),
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()


    @staticmethod
    def contar_tiempos_por_intervalo(
        fecha_inicio: date | str,
        fecha_fin: date | str,
    ) -> int:
        """
        Cuenta los registros entre dos fechas, incluyéndolas.
        """
        inicio = fecha_inicio.isoformat() if isinstance(fecha_inicio, date) else fecha_inicio.strip()
        fin = fecha_fin.isoformat() if isinstance(fecha_fin, date) else fecha_fin.strip()

        if inicio > fin:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de término.")

        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM tiempo WHERE fecha BETWEEN ? AND ?",
                (inicio, fin),
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def contar_proyectos_en_tiempos() -> int:
        """
        Cuenta los proyectos distintos que aparecen en la tabla tiempo.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(DISTINCT id_proyecto) FROM tiempo"
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def contar_empleados_en_tiempos() -> int:
        """
        Cuenta los proyectos distintos que aparecen en la tabla tiempo.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(DISTINCT id_empleado) FROM tiempo"
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def contar_pausa_minutos(rut) -> int:
        """
        Cuenta acumulacion de tiempo pausa
        """
        conn = Database().get_connection()
        try:
            cursor = conn.cursor
            cursor.execute("""
                SELECT COALESCE(SUM(pausa_minutos), 0)
                FROM tiempo
                WHERE id_empleado = ?
            """, (rut,)
            )
            
            return cursor.fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def contar_proyectos_por_rut(rut: str) -> int:
        """
        Cuenta los proyectos distintos en los que participa una persona.
        """
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(DISTINCT t.id_proyecto)
                FROM tiempo t
                JOIN empleado e ON e.id_empleado = t.id_empleado
                WHERE e.rut = ?
                """,
                (rut,),
            )
            return cursor.fetchone()[0]
        finally:
            conn.close()