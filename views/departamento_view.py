from models.departamento_dao import DepartamentoDAO

class DepartamentoView():
    def __init__(self):
        self.departamento_dao = DepartamentoDAO()

    def sub_menu(self):
        print(">" * 40)
        print("Submenú de Gestión de Departamentos")
        print(">"*40)
        print("1. Agregar Departamento")
        print("2. Modificar Departamento")
        print("3. Buscar Departamento")
        print("4. Buscar Gerente")
        print("5. Mostrar departamentos")
        print("0. Volver al menú principal")
        print(">"*40)

    def menu_edit(self) -> None:
        print("=" * 50)
        print("Editar departamento")
        print("=" * 50)
        print("1. Cambiar nombre")
        print("2. Cambiar gerente")
        print("3. Cambiar nombre y gerente")
        print("0. Cancelar y volver")
        print("=" * 50)

    def menu_mostrar_departamentos(self) -> None:
        print("=" * 50)
        print("Mostrar departamentos")
        print("=" * 50)
        print("1. Mostrar todos los departamentos y sus empleados")
        print("2. Mostrar departamento y sus empleados")
        print("3. Mostrar departamentos y nombre de gerente")
        print("4. Mostrar departamento y nombre del gerente")
        print("0. Volver")
        print("=" * 50)

    def mostrar_departamentos(departamentos:list):
        print("Departamentos")
        print(">"*60)
        for departamento in departamentos:
            print(
                f"ID: {departamento.id_departamento} | "
                f"Nombre: {departamento.nombre} | "
                f"Gerente: {departamento.gerente or 'Sin gerente'}"
            )
        print(">"*60)