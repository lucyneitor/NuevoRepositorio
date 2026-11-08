from views.main_view import MainView
from datetime import date
from views.utils import pedir
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
        print("5. Estado") #amarrar para declara a que fecha se mueve volver preguntar fecha_inicio y fecha final
        print("0. Volver")
        print("-" * 45)
        
    def formulario_proyect(self) -> dict:
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

