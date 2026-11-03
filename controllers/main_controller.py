from views.main_view import MainView #agregar cada controller
from controllers.departamento_controller import DepartamentoController
from controllers.empleado_controller import EmpleadoController
from models.empleado_dao import EmpleadoDAO
from controllers.informe_controller import InformeController
from controllers.tiempo_controller import TiempoController
from controllers.proyecto_controller import ProyectoController
from views.utils import validador_inicial, eleccion, validador_op, pedir, validador_op_sup, ValidationError


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
        self.view.enunciado_inicio() # validar antes de la linea 30 (validador_inicial)
        while True:
            opcion = pedir("usuario")
            try:
                opcion = int(opcion)
                eleccion(validador_inicial, opcion)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
            else:
                if opcion == 0:
                    print("Hasta luego.")
                    break
                elif opcion == 1:
                    intentos = 3
                    while intentos>0:
                        datos = self.view.init_usuario_existente() #Agregar 
                        encontrado = self.empleado_dao.obtener_empleado_por_user(datos)
                        if encontrado==False:
                            print("Credenciales no coinciden")
                            intentos -= 1
                            continue #mensaje correspondiente
                    #falta cuestionar si existe o no
                    if encontrado == False:
                        return
                    rol = self.empleado_dao.obtener_estado(datos["usuario"])
                    break
                elif opcion == 2:
                    self.view.titulo_funcion(1,"usuario")
                    activacion = input("Tendrá rol de administrador (si/no): ")
                    if activacion.lower() == "si":
                        rol = True
                    else:
                        rol = False
                    self.empleado_controller.agregar_empleado(rol)
                    break

        if opcion != 0: #mecanismo inicial
            while True:
                self.view.mostrar_menu()
                opcion = pedir("opción")
                try:
                    opcion = int(opcion)
                    if rol:
                        eleccion(validador_op_sup, opcion)
                    else:
                        eleccion(validador_op, opcion)
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
                        self.informe_controller.ejecutar() 




