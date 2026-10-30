from views.main_view import MainView

class EmpleadoView():
    def __init__(self):
        self.view = MainView() 

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
    def formulario_empleado(valor): #Hacer funcion validador en cada entrada
        rut = input("Ingrese su rut: ")
        print("-"*50)
        nombre = input("Ingrese su nombre: ")
        print("-"*50)
        direccion = input("Ingrese su dirreción")
        print("-"*50)
        telefono = input("Ingrese su telefono")
        print("-"*50)
        correo = input("Ingrese su correo")
        print("-"*50)
        usuario = input("Ingrese su usuario")
        print("-"*50)
        password = input("Ingrese contraseña")
        print("-"*50)
        sueldo = input("Ingrese su sueldo")
        print("-"*50)
        depa = escoger_departamento() #pendiente
        contrato = input("Ingrese fecha de contrato")
        if valor:
            print("Administrador creado exitosamente")
        else:
            print("Empleado creado exitosamente")
        return {
            "rut": rut, "nombre": nombre, "dirección":direccion, "telefono":telefono,
            "correo":correo, "usuario":usuario, "contraseña":password, "sueldo": sueldo,
            "rol_admi": valor, "contrato":contrato, "departamento":depa
        }

    def menu_edit_estado(self):
        print("="*50)
        self.view.titulo_funcion(2,"estado de Empleado")
        print("="*50)
        print("1. Activo")
        print("2. Inactivo")
        print("3. Vacaciones")
        print("4. Suspendido")