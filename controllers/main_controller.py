from views.main_view import MainView #agregar cada controller
from controllers.departamento_controller import DepartamentoController
from controllers.empleado_controller import EmpleadoController
from models.empleado_dao import EmpleadoDAO
from controllers.informe_controller import InformeController
from controllers.tiempo_controller import TiempoController
from controllers.proyecto_controller import ProyectoController
from views.utils import eleccion, pedir, validador_op_sup, ValidationError, validador_grande,mostrar_mensaje
from controllers.auth_controller import AuthController
from models.usuario_dao import UsuarioDAO

class MainController:
    def __init__(self):
        self.view = MainView() #listo
        self.empleado_controller = None
        self.departamento_controller = DepartamentoController()
        self.informe_controller = InformeController()
        self.tiempo_controller = TiempoController()
        self.proyecto_controller = ProyectoController()
        self.empleado_dao = EmpleadoDAO()
        self.auth_controller = AuthController()
        self.usuario_dao = UsuarioDAO()
        self.usuario = None

    def ejecutar(self):
        self.usuario = self.auth_controller.iniciar_sesion() 
        if self.usuario is None: #login fallido
            mostrar_mensaje("El programa ha finalizado debido a credenciales invalidadas")
            return
        self.empleado_controller = EmpleadoController(self.usuario)

        while True:
            self.view.mostrar_menu(self.usuario.rol == "Administrador") # agregar opcion gestionar usuarios
            opcion = pedir("opción")
            try:
                opcion = int(opcion)
                if self.usuario.rol == "Administrador": #usar el usuario actual para ver si tiene rol a
                    eleccion(validador_grande, opcion) #cambiar validador
                else:
                    eleccion(validador_op_sup, opcion)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:
                if opcion == 0: 
                    print("Hasta luego.")
                    break
                elif opcion == 1:
                    self.empleado_controller.ejecutar()
                elif opcion == 2:
                    self.departamento_controller.ejecutar()
                elif opcion == 3: 
                    self.tiempo_controller.ejecutar() 
                elif opcion == 4:
                    self.proyecto_controller.ejecutar() 
                elif opcion == 5:
                    mostrar_mensaje(f"Cerrando sesión de '{self.usuario.username}'...")
                    self.usuario = None
                    self.ejecutar()
                elif opcion == 6:
                    self.auth_controller.ejecutar()
                elif opcion == 7:
                    self.informe_controller.ejecutar() 
        




