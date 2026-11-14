from views.main_view import MainView
from views.utils import pedir, pwinput
from models.empleado import Empleado

class EmpleadoView():
    @staticmethod
    def sub_menu():
        print("Submenú de Gestión de Empleados")
        print(">"*40)
        print("1. Agregar Empleado")
        print("2. Modificar Empleado")
        print("3. Eliminar empleado")
        print("4. Buscar Empleado")
        print("5. Mostrar Empleados")
        print("0. Volver al menú principal")
        print(">"*40)

    @staticmethod
    def formulario_empleado()->dict: #Hacer funcion validador en cada entrada
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
        contrato = pedir("fecha de contrato 'DD-MM-YYYY'")
        return { #retorno un diccionario
            "nombre": nombre, "dirección":direccion, "telefono":telefono,
            "correo":correo, "usuario":usuario, "contraseña":password, "sueldo": sueldo,
            "contrato":contrato
        }

    @staticmethod
    def menu_edit_estado():
        print("="*50)
        MainView.titulo_funcion(2,"estado de Empleado")
        print("="*50)
        print("1. Activo")
        print("2. Inactivo")
        print("3. Vacaciones")
        print("4. Suspendido")

    @staticmethod
    def menu_edit(rol:str):
        print("="*50)
        MainView.titulo_funcion(2,"Empleado")
        print("="*50)
        print("1. Nombre")
        print("2. Direccion")
        print("3. telefono")
        print("4. correo")
        print("5. sueldo")
        print("6. Desender de Administrador" if rol=="Administrador" else "6. Accender a Administrador")#cambiar a 
        print("0. Volver al menu de gestionar empleados")
        print("="*50)

    @staticmethod
    def mostrar_por_estado(self):
        print("="*50)
        print("Mostrar registros Empleados")
        print("="*50)
        print("1. Contratados")
        print("2. Despedidos")
        print("3. En vacaciones")
        print("4. Suspendidos")
        print("="*50)

    @staticmethod
    def mostrar_empleado(empleado: Empleado) -> None:
        print("=" * 50)
        print("   FICHA DE EMPLEADO")
        print("=" * 50)
        if empleado is None:
            print("No se encontró ningún empleado con el RUT ingresado.")
            print("=" * 50)
            return

        fecha_contrato = (
            empleado.inicio_contrato.strftime("%d-%m-%Y")
            if hasattr(empleado.inicio_contrato, "strftime")
            else str(empleado.inicio_contrato)
        )
        departamento = (
            empleado.id_departamento
            if empleado.id_departamento is not None
            else "Sin departamento asignado"
        )

        print(f"RUT             : {empleado.rut}")
        print(f"Nombre          : {empleado.nombre}")
        print(f"Dirección       : {empleado.direccion}")
        print(f"Teléfono        : {empleado.telefono}")
        print(f"Correo          : {empleado.correo}")
        print(f"Sueldo          : ${empleado.sueldo:,}")
        print(f"Inicio contrato : {fecha_contrato}")
        print(f"Estado          : {empleado.estado.capitalize()}")
        print(f"ID Departamento : {departamento}")
        print("=" * 50)

    @staticmethod
    def mostrar_empleados(empleados):
        print("=" * 50)
        print("Mostrar empleados")
        print("=" * 50)
        for empleado in empleados:   
            print(f"RUT             : {empleado.rut}")
            print(f"Nombre          : {empleado.nombre}")
            print(f"Dirección       : {empleado.direccion}")
            print(f"Teléfono        : {empleado.telefono}")
            print(f"Correo          : {empleado.correo}")
            print(f"Sueldo          : ${empleado.sueldo}")
            print(f"Inicio contrato : {empleado.inicio_contrato}")
            print(f"Estado          : {empleado.estado.capitalize()}")
            print(f"ID Departamento : {empleado.id_departamento}")
            print("=" * 50)