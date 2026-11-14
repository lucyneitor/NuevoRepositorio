from models.departamento_dao import DepartamentoDAO
from models.departamento import Departamento
from models.empleado import Empleado
from views.utils import pedir, mostrar_mensaje

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
        print("6. Eliminar departamento")
        print("0. Volver al menú principal")
        print(">"*40)

    def menu_edit(self) -> None:
        print("=" * 50)
        print("Editar departamento")
        print("=" * 50)
        print("1. Editar nombre")
        print("2. Editar gerente")
        print("3. Editar todo")
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

    @staticmethod
    def mostrar_departamentos(depas : list[Departamento]):
        print("Departamentos")
        print(">"*60)
        for depa in depas:
            print(
                f"| ID: {depa.id_departamento} | "
                f"Nombre: {depa.nombre} | "
                f"Gerente: {depa.gerente or 'Sin gerente'} | "
                f"Cantidad de empleados: {len(depa.empleados)} |"
            )
            print("-"*60)
        print(">"*60)

    @staticmethod
    def mostrar_departamento(depa: Departamento, empleados:list[Empleado], rol : list[str]):
        print(">"*60)
        print(f"RESULTADOS -> {depa.nombre}")
        print(">"*60)
        print(f"Gerente: {depa.gerente}")
        if len(empleados) == 0:
            mostrar_mensaje("Sin empleados asignados")
        for indice, empleado in enumerate(empleados):
            print(
                f"| RUT: {empleado.rut} | "
                f"Nombre: {empleado.nombre} |"
                f"Rol: {rol[indice]} |"
            )
            print("-"*60)
        print(">"*60)
    
    @staticmethod 
    def formulario_departamento()->dict:
        nom = pedir("nombre del departamento")
        gerente = pedir("el nombre del gerente")
        return{
            "nombre del departamento": nom,
            "gerente a cargo": gerente
        }
    @staticmethod
    def resultados(depa:list, nom:str):
        print("-"*60)
        print(f"Lista de departamentos al mando de {nom}")
        print("-"*60)
        print("| ID | nombre de departamento |")
        for d in depa:
            print("| ",d["id_departamento"], " | ", d["nombre"], " | ")