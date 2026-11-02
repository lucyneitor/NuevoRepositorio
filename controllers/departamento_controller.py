from views.main_view import MainView
from views.departamento_view import DepartamentoView
from models.empleado import Empleado
from models.empleado_dao import EmpleadoDAO
from views.utils import validador_op1, ValidationError, eleccion, pedir

class DepartamentoController:
    def __init__(self):
        self.main_view: MainView = MainView()
        self.departamento_view = DepartamentoView()

    def ejecutar(self, opcion): #corregir todo
        while True:
            self.departamento_view.sub_menu()
            opcion = pedir("opción")
            try:
                opcion = int(opcion)
                eleccion(validador_op1, opcion)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:            
                if opcion == 0:
                    self.view.mostrar_mensaje("Saliendo de la gestión de empleados.")
                    self.main_view.mostrar_menu() 
                elif opcion == 1:
                    self.agregar_departamento(activacion)
                elif opcion == 2 
                    self.editar_empleado()
                elif opcion == 3:
                    self.buscar_empleado(rut)
                elif opcion == 0:
                    self.view.mostrar_mensaje("Saliendo de la gestión de empleados.")
                    self.main_view.mostrar_menu()
                else:
                    self.view.mostrar_mensaje("Opción no válida.")

    def agregar_empleado(self, valor):
        self.main_view.ejecutar()
        nuevo= self.departamento_view.formulario_empleado(valor) #empleado view formulario
        crear_empleado= Empleado( #creo el departamento
            sueldo=nuevo["sueldo"], inicio_contrato=nuevo["contrato"], rol_admi=nuevo['rol_admi'], 
            estado="activo", rut=nuevo["rut"], nombre=nuevo['nombre'], direccion=nuevo['direccion'],
            telefono=nuevo['telefono'], correo=nuevo['correo'], user=nuevo["user"], 
            password=nuevo['password'], selec_depa=nuevo["departamento"]
        )
        if EmpleadoDAO.crear(crear_empleado): # consultar linea (modificar)
            mensaje="Creado exitosamente"
        
        
