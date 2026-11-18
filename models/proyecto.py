from datetime import datetime, date

ESTADO = ["Pendiente", "En proceso", "Finalizado"]

class Proyecto:
    """
    La clase proyecto representa un proyecto en el que los trabajadores trabajan
    esto despues estara conectado con la base de datos de tiempo para gestionar estos
    """
    
    def __init__(self, nombre:str, descripcion:str, pais_ejecut:str, fecha_inicio:str,fecha_fin:str,estado:str, id_proyecto:int|None=None):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.pais_ejecut = pais_ejecut
        
    def __str__(self):
        return f"{self.nombre}: {self.descripcion}"

    """Nombre: Representamos el nombre del proyecto"""
    
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre: str) -> None:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del proyecto no puede estar vacío")
        self.__nombre = nombre.strip()
        self.__nombre = nombre

    """Descripcion: Representamos la descripcion del proyecto"""

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion: str) -> None:
        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ValueError("La descripción del proyecto no puede estar vacía")
        self.__descripcion = descripcion

    """Fecha de inicio: Representamos la fecha de inicio del proyecto"""
    
    @property
    def fecha_inicio(self):
        return self.__fecha_inicio.strftime("%d-%m-%Y")

    @fecha_inicio.setter
    def fecha_inicio(self, fecha_inicio: str) -> None:
        if isinstance(fecha_inicio, datetime):
            self.__fecha_inicio = fecha_inicio.date()
            return

        if isinstance(fecha_inicio, date):
            self.__fecha_inicio = fecha_inicio
            return
        if isinstance(fecha_inicio, str):
            valor_limpio = fecha_inicio.strip()
            for formato in ("%d-%m-%Y", "%Y-%m-%d"):
                try:
                    self.__fecha_inicio = datetime.strptime(valor_limpio, formato).date()
                    return
                except ValueError:
                    continue

        raise ValueError("La fecha debe tener formato DD-MM-AAAA (ej: 04-05-2026).")
    
    @property
    def fecha_fin(self):
        return self.__fecha_fin.strftime("%d-%m-%Y")
    
    @fecha_fin.setter
    def fecha_fin(self, fecha_fin: str) -> None:
        if isinstance(fecha_fin, datetime):
            self.__fecha_fin = fecha_fin.date()
            return

        if isinstance(fecha_fin, date):
            self.__fecha_fin = fecha_fin
            return
        if isinstance(fecha_fin, str):
            valor_limpio = fecha_fin.strip()
            for formato in ("%d-%m-%Y", "%Y-%m-%d"):
                try:
                    self.__fecha_fin = datetime.strptime(valor_limpio, formato).date()
                    return
                except ValueError:
                    continue

        raise ValueError("La fecha debe tener formato DD-MM-AAAA (ej: 04-05-2026).")

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, estado:str):
        if not isinstance(estado, str):
            raise TypeError("El estado debe ser texto.")

        estado = estado.strip()

        if estado not in ESTADO:
            raise ValueError(
                f"Estado inválido. Debe ser uno de estos: {', '.join(ESTADO)}."
            )

        self.__estado = estado

    @property
    def pais_ejecut(self):
        return self.__pais_ejecut

    @pais_ejecut.setter
    def pais_ejecut(self, pais_ejecut):
        self.__pais_ejecut = pais_ejecut