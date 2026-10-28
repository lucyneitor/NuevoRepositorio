from views.main_view import MainView
from models.empleado import Empleado
from pydantic import (TypeAdapter, Field, StringConstraints,ValidationError)
from typing import Annotated

regla_op = Annotated[int, Field(ge=0, le=4)] #sin rol administrador
validador_op = TypeAdapter(regla_op)

regla_op_sup = Annotated[int, Field(ge=0, le=5)] #con rol administrador
validador_op_sup = TypeAdapter(regla_op_sup)

class MainController:
    def iniciar(self):
        while True:
            #ingrese usuario y contraseña existentes
            #user=input("Ingrese el usuario")
            #password=input("Ingrese contraseña")

            #Buscar en la base de datos
            #Encontrado = buscar()

            #Encontrado
            MainView.mostrar_menu(Empleado.rol_admi)
            opcion = leer_numero("Seleccione la opción: ")
            #validador = validador_op_sup if es_admin else validador_op 
            #eleccion(validador,op)

            #No encontrado 
            MainView.titulo_funcion(opcion,"usuario a sistema")
            
            self.procesar_opcion(opcion)

    def procesar_opcion(self, opcion: int):
        if opcion == 1:
            print("Ir a gestionar empleados")#
        elif opcion == 2:
            print("Ir a gestionar departamentos")
        elif opcion == 3:
            print("Ir a gestionar tiempo")
        elif opcion == 4:
            print("Ir a gestionar proyectos")
        elif opcion == 5:
            print("Ir a gestionar informes")
        else:
            self.view.mostrar_error("Opción no válida")