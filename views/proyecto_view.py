from views.main_view import MainView
from datetime import date
from views.utils import pedir
from models.proyecto import Proyecto
class ProyectoView():
    def sub_menu(self):
        print("Submenú de Gestión de Proyectos")
        print(">"*40)
        print("1. Agregar Proyecto")
        print("2. Modificar Proyecto")
        print("3. Buscar Proyecto")
        print("4. Eliminar Proyecto")
        print("5. Mostrar proyectos")
        print("0. Volver al menú principal")
        print(">"*40)

    def menu_modificar(self):
        print("Opciones de edición")
        print("-" * 45)
        print("1. Nombre")
        print("2. Descripción")
        print("3. Fecha de inicio") #sujeto a editar automatico estado y obligar declarar fecha termino
        print("4. Fecha de término") #validar que no sea antes de la fecha_inicio
        print("0. Volver")
        print("-" * 45)
        
    def formulario(self) -> dict:
        print(">"*50)
        print(">"*50)
        nombre = pedir("Nombre del proyecto").strip()
        descripcion = pedir("Descripción").strip()

        while True:
            try:
                fecha_inicio_texto = pedir("Fecha de inicio (AAAA-MM-DD)").strip()
                fecha_inicio = date.fromisoformat(fecha_inicio_texto)

                fecha_fin_texto = pedir("Fecha de término (AAAA-MM-DD)").strip()
                fecha_fin = date.fromisoformat(fecha_fin_texto)

                if fecha_fin < fecha_inicio:
                    print("La fecha de término no puede ser anterior a la fecha de inicio.")
                    continue

                break
            except ValueError:
                print("Ingresa las fechas con el formato AAAA-MM-DD.")

        hoy = date.today()

        if hoy < fecha_inicio:
            estado = "Pendiente"
        elif hoy > fecha_fin:
            estado = "Finalizado"
        else:
            estado = "En proceso"

        return {
            "nombre": nombre,
            "descripcion": descripcion,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat(),
            "estado": estado,
        }

    def mostrar_proyecto(proyecto:Proyecto):
        print("\n--- Datos del proyecto ---")
        print(f"ID: {proyecto.id_proyecto}")
        print(f"Nombre: {proyecto.nombre}")
        print(f"Descripción: {proyecto.descripcion}")
        print(f"Fecha de inicio: {proyecto.fecha_inicio}")
        print(f"Fecha de término: {proyecto.fecha_fin}")
        print(f"Estado: {proyecto.estado}")
        print("--------------------------\n")

    def menu_mostrar(self):
        print("\n¿Qué datos quieres mostrar?")
        print("1. Todos los detalles")
        print("2. Solo datos especificos")
        print("0. Volver")

    def menu_op1(self, proyectos: list[Proyecto]) -> None:
        print("| ID | Nombre | Descripción | Fecha inicio | Fecha término | Estado |")

        for proyecto in proyectos:
            print(
                f"| {proyecto.id_proyecto} "
                f"| {proyecto.nombre} "
                f"| {proyecto.descripcion} "
                f"| {proyecto.fecha_inicio} "
                f"| {proyecto.fecha_fin} "
                f"| {proyecto.estado} |"
            )

    def menu_op2(self):
        print("\n¿Qué datos quieres mostrar?")
        print("1. Nombre")
        print("2. Descripción")
        print("3. Fecha de inicio")
        print("4. Fecha de término")
        print("5. Estado")
        print("6. Listo los seleccionados")
        print("0. Volver")

    def mostrar_detalle(self,opciones:list[str],proyectos:list[Proyecto]):
        campos_disponibles = {
            "nombre": ("Nombre", "nombre"),
            "descripción": ("Descripción", "descripcion"),
            "fecha inicio": ("Inicio", "fecha_inicio"),
            "fecha fin": ("Término", "fecha_fin"),
            "estado": ("Estado", "estado"),
        }

        campos = [
            campos_disponibles[opcion]
            for opcion in opciones
            if opcion in campos_disponibles
        ]

        encabezados = [titulo for titulo, _ in campos]
        filas = [
            [str(proyecto[columna]) for _, columna in campos]
            for proyecto in proyectos
        ]

        anchos = [
            max([len(encabezados[i])] + [len(fila[i]) for fila in filas])
            for i in range(len(encabezados))
        ]

        borde = "+" + "+".join("-" * (ancho + 2) for ancho in anchos) + "+"

        def imprimir_fila(valores):
            celdas = [
                f" {valor.ljust(anchos[i])} "
                for i, valor in enumerate(valores)
            ]
            print("|" + "|".join(celdas) + "|")

            print(borde)
            imprimir_fila(encabezados)
            print(borde)

            for fila in filas:
                imprimir_fila(fila)

            print(borde)
