from models.empleado import Empleado

class Departamento:
    def __init__(self, id_departamento=None, nombre=None, gerente=None):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.gerente = gerente
        self.empleados: list[Empleado] = [] 

    @property
    def nombre(self)->str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre:str)->None:
        self.__nombre = nombre

    @property
    def gerente(self)->str:
        return self.__gerente

    @gerente.setter
    def gerente(self, gerente:str)->None:
        self.__gerente=gerente

    
        