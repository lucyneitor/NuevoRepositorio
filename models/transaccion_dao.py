import logging
from config.database import Database
from models.transaccion import Transaccion

logger = logging.getLogger(__name__)

class TransaccionDAO:
    @staticmethod
    def guardar(transaccion: Transaccion) -> bool:
        """
        Inserta un nuevo registro de transacción de pago internacional en SQLite.
        """
        db = Database()
        conn = db.get_connection()
        if not conn:
            logger.error("No se pudo establecer conexión con la base de datos para guardar la transacción.")
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transaccion (
                    rut, id_proyecto, sueldo_emp, moneda_origen_clp,
                    sueldo_pagado, moneda_destino, tasa_cambio, fecha_transaccion
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                transaccion.rut,
                transaccion.id_proyecto,
                transaccion.sueldo_emp,
                transaccion.moneda_origen_clp,
                transaccion.sueldo_pagado,
                transaccion.moneda_destino,
                transaccion.tasa_cambio,
                transaccion.fecha_transaccion
            ))
            
            conn.commit()
            return True

        except Exception as e:
            logger.error(f"Error al guardar la transacción en la base de datos: {e}")
            return False
        finally:
            conn.close()