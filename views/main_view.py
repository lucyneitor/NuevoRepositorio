

class MainView:
    @staticmethod
    def inicio_seccion(booleano:bool): #en controller se gestiona
        MainView.mostrar_menu() 
        if booleano: #si rol_admi es verdadero le mostrara la opción 5
            print("5. Gestionar Informes")

    def mostrar_menu():
        print("Bienvenido al sistema de ecotech")
        print(">"*40)
        print("1. Gestionar Empleados")
        print("2. Gestionar Departamentos")
        print("3. Gestionar Tiempo")
        print("4. Gestionar Proyectos")
        print("0. Salir")
        print(">"*40)    

    @staticmethod
    def titulo_funcion(op:int,objetito:str):
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
        print(">"*40)

    
    

