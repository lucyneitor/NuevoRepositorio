from models.empleado import Empleado

class Tiempo:

    """
    La clase tiempo representa cuanto demoran los trabajadores en realizar un proyecto
    esto despues estara conectado con la base de datos de proyecto para gestionar estos
    """
    
    def __init__(
        self,
        id_tiempo: int | None,
        fecha: str,
        hora_entrada: str,
        hora_salida: str,
        id_empleado: str,
        id_proyecto: int,
    ) -> None:
        self.id_tiempo = id_tiempo
        self.fecha = fecha
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto

    def __str__(self):
        return (
            f"Fecha: {self.fecha}\n"
            f"Tiempo trabajado: {self.tiempo_trabajado} horas\n"
            f"Descripción: {self.descripcion}"
        )

    """Fecha: Representamos la fecha del trabajo"""

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, fecha: str) -> None:
        if not isinstance(fecha, str) or not fecha.strip():
            raise ValueError("La fecha no puede estar vacía")
        self._fecha = fecha.strip()
        return self._fecha

    """Tiempo trabajado: Representamos el tiempo trabajado en horas"""

    @property
    def tiempo_trabajado(self):
        return self._tiempo_trabajado

    @tiempo_trabajado.setter
    def tiempo_trabajado(self, tiempo_trabajado:float) -> None:
        if isinstance(tiempo_trabajado, bool) or not isinstance(
            tiempo_trabajado, (int, float)
        ):
            raise ValueError("El tiempo trabajado debe ser un número")
        if tiempo_trabajado < 0:
            raise ValueError("El tiempo trabajado no puede ser negativo")
        self._tiempo_trabajado = tiempo_trabajado
        return self._tiempo_trabajado

    """Descripcion: Representamos la descripcion del trabajo"""

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ValueError("La descripción no puede estar vacía")
        self._descripcion = descripcion.strip()
        return self._descripcion