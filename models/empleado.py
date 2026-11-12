from datetime import date
from models.persona import Persona

ESTADO = ["activo", "inactivo", "vacaciones", "suspendido"]

class Empleado(Persona):
    def __init__(
        self, 
        sueldo:int, 
        inicio_contrato:date, 
        estado:str, 
        rut:str,
        nombre:str,
        direccion:str,
        telefono:str,
        correo:str,
        id_departamento:int | None = None,
        ):
        super().__init__(rut, nombre, direccion, telefono, correo)
        self.sueldo = sueldo
        self.inicio_contrato = inicio_contrato
        self.estado = estado 
        self.id_departamento = id_departamento

    @property
    def sueldo(self)->int:
        return self.__sueldo

    @sueldo.setter
    def sueldo(self, sueldo:int)->None:
        self.__sueldo = sueldo # agregar validacion en sueldo

    @property
    def inicio_contrato(self)->date:
        return self.__inicio_contrato

    @inicio_contrato.setter
    def inicio_contrato(self, inicio_contrato:date)->None:
        """Valida y asigna la fecha de inicio del contrato."""

        if isinstance(inicio_contrato, str):
            try:
                inicio_contrato = date.strptime(
                    inicio_contrato.strip(),
                    "%d-%m-%Y"
                )
            except ValueError as error:
                raise ValueError(
                    "La fecha de inicio de contrato debe tener formato DD-MM-YYYY."
                ) from error

        if not isinstance(inicio_contrato, date):
            raise TypeError(
                "La fecha de inicio de contrato debe ser un objeto date o texto."
            )

        self.__inicio_contrato = inicio_contrato
    @property
    def estado(self)->str:
        return self.__estado

    @estado.setter
    def estado(self, estado:str)->None:
        self.__estado = estado
