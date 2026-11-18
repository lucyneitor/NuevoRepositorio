class Transaccion:
    def __init__(
        self,
        rut: str,
        id_proyecto: int,
        sueldo_emp: float,
        moneda_origen_clp: str,
        sueldo_pagado: float,
        moneda_destino: str,
        tasa_cambio: float,
        fecha_transaccion: str,
        id_transaccion: int | None = None
    ):
        self.id_transaccion = id_transaccion
        self.rut = rut
        self.id_proyecto = id_proyecto
        self.sueldo_emp = sueldo_emp
        self.moneda_origen_clp = moneda_origen_clp
        self.sueldo_pagado = sueldo_pagado
        self.moneda_destino = moneda_destino
        self.tasa_cambio = tasa_cambio
        self.fecha_transaccion = fecha_transaccion

    def __str__(self):
        return (
            f"Transacción #{self.id_transaccion} | RUT: {self.rut} | "
            f"Proyecto ID: {self.id_proyecto} | Pago: {self.sueldo_pagado} {self.moneda_destino} "
            f"(Tasa: {self.tasa_cambio})"
        )