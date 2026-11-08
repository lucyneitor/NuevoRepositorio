from models.empleado import Empleado

class Departamento:
    def __init__(self, id_departamento=None, nombre=None, gerente=None, empleados: list[Empleado] | None = None):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.gerente = gerente
        self.empleados = empleados

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

    @property
    def empleados(self) -> list[Empleado] | None:
        return self.__empleados
    
    @empleados.setter
    def empleados(self, empleados:list[Empleado]) -> None:
        if not isinstance(empleados, list):
            raise TypeError("Los empleados deben entregarse en una lista.")

        if not all(isinstance(empleado, Empleado) for empleado in empleados):
            raise TypeError("Cada elemento debe ser un objeto Empleado.")

        self.__empleados = empleados
    
        