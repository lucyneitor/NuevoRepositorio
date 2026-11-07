from models.departamento_dao import DepartamentoDAO

class DepartamentoView():
    def __init__(self):
        self.departamento_dao = DepartamentoDAO()

    def sub_menu(self):
        print("Submenú de Gestión de Departamentos")
        print(">"*40)
        print("1. Agregar Departamento")
        print("2. Modificar Departamento")
        print("3. Buscar Departamento")
        print("4. Mostrar departamentos")
        print("0. Volver al menú principal")
        print(">"*40)

    def menu_edit():
        print("Opciones de edición")
        print("="*50)
        print("1. Nombre del departamento")
        print("2. Gerente")
        print("0. Volver")
        print("="*50)

    def mostrar_departamentos(departamentos:list):
        print("\nDepartamentos")
        print(">"*60)
        for departamento in departamentos:
            print(
                f"ID: {departamento.id_departamento} | "
                f"Nombre: {departamento.nombre} | "
                f"Gerente: {departamento.gerente or 'Sin gerente'}"
            )
        print(">"*60)