from views.main_view import MainView #agregar cada controller
from controllers.departamento_controller import DepartamentoController
from controllers.empleado_controller import EmpleadoController
from controllers.informe_controller import InformeController
from controllers.tiempo_controller import TiempoController
from controllers.proyecto_controller import ProyectoController
from pydantic import (TypeAdapter, Field, StringConstraints,ValidationError)
from typing import Annotated

regla_op_inicial = Annotated[int, Field(ge=0,le=2)]
validador_inicial = TypeAdapter(regla_op_inicial)

regla_op = Annotated[int, Field(ge=0, le=4)] #sin rol administrador
validador_op = TypeAdapter(regla_op)

regla_op_sup = Annotated[int, Field(ge=0, le=5)] #con rol administrador
validador_op_sup = TypeAdapter(regla_op_sup)

class MainController:
    def __init__(self):
        self.view = MainView() #listo
        self.empleado_controller = EmpleadoController()
        self.departamento_controller = DepartamentoController()
        self.informe_controller = InformeController()
        self.tiempo_controller = TiempoController()
        self.proyecto_controller = ProyectoController()

    def ejecutar(self):
        opcion = self.view.enunciado_inicio() # validar antes de la linea 30 (validador_inicial)
        opcion = int(opcion)
        while True:
            if opcion == 0:
                break;
            elif opcion == 1:
                intentos = 3
                while intentos>0:
                    encontrado=self.view.init_usuario_existente()
                    if encontrado==False:
                        print("Credenciales no coinciden")
                        intentos -= 1
                        continue #mensaje correspondiente
            elif opcion == 2:
                self.view.titulo_funcion(1,"usuario")
                activacion = input("Tendrá rol de administrador (si/no): ")
                if activacion.lower() == "si":
                    rol = True
                else:
                    rol = False
                self.empleado_controller.agregar_empleado(rol)
            opcion = self.view.mostrar_menu() #validar antes de la linea 41 
            self.view.titulo_funcion(opcion)


