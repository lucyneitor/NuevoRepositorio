from sqlite3 import Cursor
from config.database import Database
from models.empleado import Empleado #
from models.departamento import Departamento # 
from models.proyecto import Proyecto #
from models.tiempo import Tiempo #
from models.informe import Informe #

class InformeDAO:
    @staticmethod
    def obtener_empleado():
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("""SELECT e.nombre, e.sueldo, e.inicio_contrato,d.nombre
            from empleado e, departamento d
            where e.id_departamento = d.id_departamento;""")
            inf_empleado = cursor.fetchall()
            return inf_empleado
        except Exception as e:
            print(f"Error al obtener informe en BD: {e}")
            return False
        finally:
            conn.close()
    @staticmethod
    def obtener_departamento():
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("""SELECT nombre, gerente, presupuesto
                           from departamento;""")
            inf_departamento = cursor.fetchall()
            return inf_departamento
        except Exception as e:
            print(f"Error al obtener informe en BD: {e}")
            return False
        finally:
            conn.close()
    @staticmethod
    def obtener_tiempo_proyecto():
        conn = Database().get_connection()
        try:
            cursor: Cursor = conn.cursor()
            cursor.execute("""SELECT e.nombre, e.rut, t.hora_entrada, t.hora_salida,
                           p.nombre, p.fecha_inicio, p.fecha_fin
                           from empleado e
                           join tiempo t on e.rut = t.id_empleado
                           join proyecto p on t.id_proyecto = p.id_proyecto""")
            inf_tiempo_proyecto = cursor.fetchall()
            return inf_tiempo_proyecto
        except Exception as e:
            print(f"Error al obtener informe en BD: {e}")
            return False
        finally:
            conn.close()