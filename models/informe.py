from datetime import date

class Informe:
    def __init__(self, id_informe:int, fecha:date, formato:str, responsable:str):
        self.id_informe = id_informe #no tienen property ni setter
        self.fecha = fecha
        self.formato = formato
        self.responsable = responsable #rut de empleado con rol admi

    @property
    def fecha(self)->date:
        return self.__fecha

    def fecha(self, fecha:date)->None:
        self.__fecha = fecha

    def formato(self)->str:
        return self.__formato

    def formato(self, formato:str):
        self.__formato = formato

    def responsable(self)-> str:
        return self.__responsable

    def responsable(self, responsable:str)->None:
        self.__responsable = responsable