from views.main_view import MainView
from views.utils import pedir, pwinput
from controllers.empleado_controller import EmpleadoController
class EmpleadoView():
    def __init__(self):
        self.view = MainView() 
        self.empleado_controlLer = EmpleadoController()

    @staticmethod
    def sub_menu():
        print("Submenú de Gestión de Empleados")
        print(">"*40)
        print("1. Agregar Empleado")
        print("2. Modificar Empleado")
        print("3. Buscar Empleado")
        print("0. Volver al menú principal")
        print(">"*40)

    @staticmethod
    def formulario_empleado(self,valor)->dict: #Hacer funcion validador en cada entrada
        rut = pedir("rut")
        print("-"*50)
        nombre = pedir("nombre")
        print("-"*50)
        direccion = pedir("dirreción")
        print("-"*50)
        telefono = pedir("telefono")
        print("-"*50)
        correo = pedir("correo")
        print("-"*50)
        usuario = pedir("usuario")
        print("-"*50)
        password = pwinput.pwinput("Ingrese su contraseña: ", mask="*")
        print("-"*50)
        sueldo = pedir("sueldo")
        print("-"*50)

        depa = self.empleado_controller.escoger_departamento() #pendiente ("Dejar creado por defecto 2")
        contrato = pedir("Ingrese fecha de contrato")
        if valor:
            print("Administrador creado exitosamente")
        else:
            print("Empleado creado exitosamente")
        return { #retorno un diccionario
            "rut": rut, "nombre": nombre, "dirección":direccion, "telefono":telefono,
            "correo":correo, "usuario":usuario, "contraseña":password, "sueldo": sueldo,
            "contrato":contrato, "departamento":depa, "rol":valor
        }

    def menu_edit_estado(self):
        print("="*50)
        self.view.titulo_funcion(2,"estado de Empleado")
        print("="*50)
        print("1. Activo")
        print("2. Inactivo")
        print("3. Vacaciones")
        print("4. Suspendido")

    def menu_edit(self):
        print("="*50)
        self.view.titulo_funcion(2,"Empleado")
        print("="*50)
        print("1. Nombre")
        print("2. Direccion")
        print("3. telefono")
        print("4. correo")
        print("5. sueldo")
        print("6. Acceder o desender de Administrador")#cambiar