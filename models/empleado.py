from datetime import date

class Empleado():
    @staticmethod
    def __init__(self, sueldo:int, inicio_contrato:date, rol_admi:bool, estado:str):
        self.sueldo = sueldo
        self.inicio_contrato = inicio_contrato
        self.rol_admi = rol_admi
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
    def rol_admi(self)->bool:
        return self.__rol_admi

    @rol_admi.setter
    def rol_admi(self, rol_admi:bool)->None:
        self.__rol_admi = rol_admi #agregar validacion en admi

    @property
    def estado(self)->str:
        return self.__estado

    @estado.setter
    def estado(self, estado:str)->None:
        self.__estado = estado
