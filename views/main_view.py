from views.utils import pedir, pwinput
from models.empleado_dao import EmpleadoDAO

class MainView:
    def __init__(self):
        self.empleado_dao = EmpleadoDAO()

    @staticmethod
    def mostrar_menu(admin:bool):
        print("Bienvenido al sistema de ecotech")
        print(">"*40)
        print("1. Gestionar Empleados")
        print("2. Gestionar Departamentos")
        print("3. Gestionar Tiempo")
        print("4. Gestionar Proyectos")
        print("5. Cerrar Sesión -> Cambiar usuario")
        print("6. Gestionar usuarios y credenciales")

        if admin:
            print("7. Gestionar Informes")

        print("0. Salir del Sistema")
        print(">"*40)    

    @staticmethod
    def titulo_funcion(op: int,objetito:str):
        match op:
            case 1:
                print(f"Agregar nuevo {objetito}...")
            case 2:
                print(f"Modificar {objetito}...")
            case 3:
                print(f"Buscar {objetito}...")
            case 4:
                print(f"Eliminar {objetito}...")
            case 0:
                print("Saliendo del sistema...")
            case _:
                print("Opción no válida. Por favor, seleccione una opción del menú.")
        

    
    

