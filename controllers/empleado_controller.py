from views.main_view import MainView
from views.empleado_view import EmpleadoView
from models.empleado import Empleado
from models.empleado_dao import EmpleadoDAO
from views.utils import validador_op1, eleccion

class EmpleadoController:
    def __init__(self):
        self.main_view = MainView()
        self.empleado_view = EmpleadoView()

    def ejecutar(self, opcion):
        self.empleado_view.sub_menu
        opcion = input() #te amo mucho mi vida
        eleccion(validador_op1, opcion)
        opcion = int(opcion)
        if opcion == 1:
            activacion = input("Tendrá rol de administrador (si/no): ")
            self.agregar_empleado(activacion)
        elif opcion == 2 or opcion == 3 or opcion == 4:
            rut = input("Ingrese su rut: ")
            if opcion==2:
                self.editar_empleado(rut)
            elif opcion == 3:
                self.eliminar_empleado(rut)
            elif opcion == 4:
                self.imprimir_empleado(rut)
        elif opcion == 5:
            self.imprimir_empleados()
        elif opcion == 0:
            self.view.mostrar_mensaje("Saliendo de la gestión de empleados.")
            self.main_view.mostrar_menu()
        else:
            self.view.mostrar_mensaje("Opción no válida.")

    def agregar_empleado(self, valor):
        nuevo= self.empleado_view.formulario_empleado(valor) #empleado view formulario
        crear_empleado= Empleado( #creo el departamento
            sueldo=nuevo["sueldo"], inicio_contrato=nuevo["contrato"], rol_admi=nuevo['rol_admi'], 
            estado="activo", rut=nuevo["rut"], nombre=nuevo['nombre'], direccion=nuevo['direccion'],
            telefono=nuevo['telefono'], correo=nuevo['correo'], user=nuevo["user"], 
            password=nuevo['password'], selec_depa=nuevo["departamento"]
        )
        if EmpleadoDAO.crear(crear_empleado): # consultar linea (modificar)
            mensaje="Creado exitosamente"
            
    def editar_empleado(self):
        op = self.empleado_view.menu_edit_estado
        estado = self.utils(op)
