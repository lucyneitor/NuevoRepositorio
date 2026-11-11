from datetime import date, datetime, time, timedelta

class Tiempo:
    """Representa el registro de tiempo trabajado por un empleado en un proyecto."""

    def __init__(
        self,
        id_tiempo: int | None,
        fecha: date | str,
        hora_entrada: time | str,
        hora_salida: time | str,
        rut_empleado: str,
        id_proyecto: int,
        pausa_minutos: int = 0,
    ) -> None:
        self.id_tiempo = id_tiempo
        self.fecha = fecha
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida
        self.rut_empleado = rut_empleado
        self.id_proyecto = id_proyecto
        self.pausa_minutos = pausa_minutos

    @property
    def fecha(self) -> date:
        return self.__fecha

    @fecha.setter
    def fecha(self, valor: date | str) -> None:
        if isinstance(valor, str):
            try:
                valor = date.fromisoformat(valor.strip())
            except ValueError as error:
                raise ValueError("La fecha debe tener formato AAAA-MM-DD.") from error

        if not isinstance(valor, date):
            raise TypeError("La fecha debe ser un objeto date o un texto AAAA-MM-DD.")

        self.__fecha = valor

    @property
    def hora_entrada(self) -> time:
        return self.__hora_entrada

    @hora_entrada.setter
    def hora_entrada(self, valor: time | str) -> None:
        self.__hora_entrada = self._convertir_hora(valor, "entrada")

    @property
    def hora_salida(self) -> time:
        return self.__hora_salida

    @hora_salida.setter
    def hora_salida(self, valor: time | str) -> None:
        self.__hora_salida = self._convertir_hora(valor, "salida")

    @staticmethod
    def _convertir_hora(valor: time | str, nombre: str) -> time:
        if isinstance(valor, str):
            try:
                valor = time.fromisoformat(valor.strip())
            except ValueError as error:
                raise ValueError(
                    f"La hora de {nombre} debe tener formato HH:MM o HH:MM:SS."
                ) from error

        if not isinstance(valor, time):
            raise TypeError(f"La hora de {nombre} debe ser un objeto time o texto.")

        return valor

    @property
    def pausa_minutos(self) -> int:
        return self.__pausa_minutos

    @pausa_minutos.setter
    def pausa_minutos(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
            raise ValueError("La pausa debe ser un número entero de minutos no negativo.")

        self.__pausa_minutos = valor

    @property
    def duracion_trabajada(self) -> timedelta:
        """Devuelve la duración trabajada, descontando la pausa."""

        inicio = datetime.combine(self.fecha, self.hora_entrada)
        fin = datetime.combine(self.fecha, self.hora_salida)

        # Si la salida es anterior a la entrada,
        # significa que la jornada terminó al día siguiente.
        if fin < inicio:
            fin += timedelta(days=1)

        duracion = fin - inicio - timedelta(minutes=self.pausa_minutos)

        if duracion <= timedelta(0):
            raise ValueError(
                "La pausa no puede ser igual o superior "
                "a la duración de la jornada."
            )

        return duracion

    @property
    def rut_empleado(self) -> str:
        """Devuelve el RUT del empleado asociado al registro."""
        return self.__rut_empleado
    
    @rut_empleado.setter
    def rut_empleado(self, valor: str) -> None:
        """Valida y asigna el RUT del empleado."""

        if not isinstance(valor, str):
            raise TypeError("El RUT del empleado debe ser texto.")

        valor = valor.strip().upper()

        if not valor:
            raise ValueError("El RUT del empleado no puede estar vacío.")

        self.__rut_empleado = valor

    

    def __str__(self) -> str:
        return (
            f"Fecha: {self.fecha.isoformat()} | "
            f"Entrada: {self.hora_entrada.isoformat()} | "
            f"Salida: {self.hora_salida.isoformat()} | "
            f"Horas trabajadas: {self.tiempo_trabajado:.2f}"
        )