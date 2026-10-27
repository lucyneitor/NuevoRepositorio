

class Departamento:
    @staticmethod
    def __init__(self, id_departamento=None, nombre=None, gerente=None):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.gerente = gerente

    @property
    def nombre(self)->str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre:str)->None:
        self.__nombre = nombre

    def gerente(self)->str:
        return self.__gerente

    def gerente(self, gerente:str)->None:
        self.__gerente=gerente

    
        