from views.main_view import MainView #agregar cada controller
from controllers.departamento_controller import DepartamentoController
from controllers.empleado_controller import EmpleadoController
from models.empleado_dao import EmpleadoDAO
from controllers.informe_controller import InformeController
from controllers.tiempo_controller import TiempoController
from controllers.proyecto_controller import ProyectoController
from views.utils import validador_inicial

class MainController:
    def __init__(self):
        self.view = MainView() #listo
        self.empleado_controller = EmpleadoController()
        self.departamento_controller = DepartamentoController()
        self.informe_controller = InformeController()
        self.tiempo_controller = TiempoController()
        self.proyecto_controller = ProyectoController()
        self.empleado_dao = EmpleadoDAO()

    def ejecutar(self):
        opcion = self.view.enunciado_inicio(validador_inicial) # validar antes de la linea 30 (validador_inicial)
        opcion = int(opcion)
        while True:
            if opcion == 0:
                break;
            elif opcion == 1:
                intentos = 3
                while intentos>0:
                    datos = self.view.init_usuario_existente() #Agregar 
                    encontrado = self.empleado_dao.obtener_empleado_por_user(datos)
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


