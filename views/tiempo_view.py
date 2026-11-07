
class TiempoView():
    def sub_menu(self):
        print("Gestión de Tiempos")
        print(">"*40)
        print("1. Listar tiempos")
        print("2. Agregar tiempo ")
        print("3. Buscar tiempo")
        print("4. Actualizar tiempo")
        print("0. Volver al menú principal")
        print(">"*40)

    def mostrar(self):
        print("Listar Tiempos realizados")
        print("-"*50)

    def menu_listar(self):
        print("Opciones de listar Tiempos")
        print("-"*50)
        print("1. Mostrar todos")
        print("2. Filtrar por empleado")
        print("3. Filtrar por proyecto")
        print("4. Filtrar por fecha")
        print("5. Filtrar por rango de fechas")
        print("6. Filtrar por empleado y proyecto")
        print("0. Volver")

    #mostrar_registros () --Resumen general y despues todo
    #mostrar_registros(id_empleado) --Resumen general y despues todo
    #mostrar_registros(id_proyecto) --Resumen general y despues todo
    #mostrar_registros(fecha especifica) --Resumen general y despues todo
    #mostrar_registros(fecha1,fecha2) --Resumen general y despues todo
    #Mostrar_registros(id_proyecto, id_empleado) --Resumen general y despues todo

    #formulario_tiempo()->dict

    #