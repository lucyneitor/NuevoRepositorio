class persona():
    def __init__(self,rut:str,nombre:str,direccion:str,telefono:str,
                 correo:str,user:str,password:str):
        self.rut = rut
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.user = user
        self.password = password

    @property
    def rut(self)->str:
        return self.__rut

    @rut.setter
    def rut(self,rut:str)->None:
        self.__rut = rut #agregar validacion de rut

    @property
    def nombre(self)->str:  
        return self.__nombre

    @nombre.setter
    def nombre(self,nombre:str)->None:
        self.__nombre = nombre #agregar validacion de nombre

    @property
    def direccion(self)->str:
        return self.__direccion

    @direccion.setter
    def direccion(self,direccion:str)->None:
        self.__direccion = direccion #agregar validación de dirección

    @property
    def telefono(self)->str:
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono:str)->None:
        self.__telefono = telefono #agregar validación de telefono

    @property
    def correo(self)->str:
        return self.__correo 

    @correo.setter
    def correo(self, correo: str)->None:
        self.__correo = correo #agregar validación de correo

    @property
    def user(self)->str:
        return self.__user

    @user.setter
    def user(self, user:str)->None:
        self.__user = user #agregar validación de user

    @property
    def password(self)->str:
        return self.__password

    @password.setter
    def password(self, password:str)->None:
        self.__password = password

    