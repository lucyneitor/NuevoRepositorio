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
        ):
        super().__init__(rut, nombre, direccion, telefono, correo)
        self.sueldo = sueldo
        self.inicio_contrato = inicio_contrato
        self.estado = estado 

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
        self.__inicio_contrato = inicio_contrato #agregar validación en contrato

    @property
    def estado(self)->str:
        return self.__estado

    @estado.setter
    def estado(self, estado:str)->None:
        self.__estado = estado
