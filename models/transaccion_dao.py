import logging
import sqlite3
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
            conn.execute("BEGIN IMMEDIATE")
            cursor.execute("""
                SELECT 1 FROM transaccion
                WHERE rut = ? AND id_proyecto = ?
                    AND substr(fecha_transaccion, 1, 7) = ?
                LIMIT 1
            """, (transaccion.rut, transaccion.id_proyecto,
                    transaccion.fecha_transaccion[:7]))
            if cursor.fetchone():
                logger.warning("Este pago ya se registró para el período indicado.")
                conn.rollback()
                return False
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

        except sqlite3.Error as e:
            conn.rollback()
            logger.error("Error al guardar la transacción: %s", e)
            return False
        finally:
            conn.close()