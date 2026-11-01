from sqlite3 import Cursor
from config.database import Database
from models.proyecto import Proyecto

class ProyectoDAO:
    @staticmethod
    def agregar_proyecto(proyecto_obj: Proyecto):
        conn = Database().get_connection()
        try: 
            cursor : Cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO proyecto (
                id_proyecto, 
                nombre, 
                descripcion, 
                fecha_inicio, 
                fecha_fin)
            VALUES(?,?,?,?,?)"""
            ,(proyecto_obj.id_proyecto, 
              proyecto_obj.nombre,
              proyecto_obj.descripcion,
              proyecto_obj.fecha_inicio,
              proyecto_obj.fecha_fin))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar proyecto en BD: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def obtener_proyectos():
        conn = Database().get_connection()
        try:
            cursor : Cursor = conn.cursor()
            cursor.execute("""SELECT * from proyecto""")
            ob_proyectos = cursor.fetchall()
            return ob_proyectos
        except Exception as e:
            print(f"Error al obtener proyecto en BD: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def obtener_proyecto_id(id_proyecto : int):
        conn = Database().get_connection()
        try:
            cursor : Cursor = conn.cursor()
            cursor.execute("""SELECT * from proyecto WHERE id_proyecto = ?""",(id_proyecto,))
            proyecto_data = cursor.fetchone()
            return proyecto_data
        except Exception as e:
            print(f"Error al obtener proyecto en BD: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def actualizar_proyecto(proyecto_obj:Proyecto):
        conn = Database().get_connection()
        try:
            cursor : Cursor = conn.cursor()
            cursor.execute("""UPDATE proyecto
                           SET nombre = ?, descripcion = ?, fecha_inicio = ?, fecha_fin = ?
                           WHERE id_proyecto = ?""", 
                           (proyecto_obj.nombre,
                            proyecto_obj.descripcion,
                            proyecto_obj.fecha_inicio,
                            proyecto_obj.fecha_fin,
                            proyecto_obj.id_proyecto))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar proyecto en BD: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def eliminar_proyecto(id_proyecto: int):
        conn = Database().get_connection()
        try:
            cursor : Cursor = conn.cursor()
            cursor.execute("""DELETE FROM proyecto WHERE id_proyecto = ?"""
                           ,(id_proyecto,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar proyecto en BD: {e}")
            return False
        finally:
            conn.close()