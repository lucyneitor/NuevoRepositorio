from views.utils import pedir

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

    def menu_buscar(self):
        print("Opciones para buscar registros de tiempo")
        print("-" * 50)
        print("1. Buscar por ID del registro")
        print("2. Buscar por RUT del empleado")
        print("3. Buscar por ID del proyecto")
        print("4. Buscar por fecha específica")
        print("5. Buscar por intervalo de fechas")
        print("6. Buscar por RUT y proyecto")
        print("0. Volver")

    def menu_actualizar(self):
        print("Opciones para actualizar registros de tiempo")
        print("-" * 50)
        print("1. Actualizar fecha")
        print("2. Actualizar hora de entrada")
        print("3. Actualizar hora de salida")
        print("4. Actualizar RUT del empleado")
        print("5. Actualizar proyecto")
        print("6. Actualizar minutos de pausa")
        print("7. Actualizar todos los datos")
        print("0. Volver")

    def mostrar_registros(registros:list,tiempos:int,proyecto:int,empleado:int): #Resumen general y despues todo
        print("-"*60)
        print("Listar Resultados")
        print("-"*60)
        if not registros:
            print("No hay registros de tiempo para mostrar.")
            return

        for registro in registros:
            tiempo = registro["tiempo"]
            nombre_proyecto = registro["nombre_proyecto"]

            print(
                f"Registro N.º {tiempo.id_tiempo} | "
                f"Empleado (RUT): {tiempo.id_empleado} | "
                f"Proyecto: {nombre_proyecto} | "
                f"Fecha: {tiempo.fecha} | "
                f"Entrada: {tiempo.hora_entrada} | "
                f"Salida: {tiempo.hora_salida} | "
                f"Pausa: {tiempo.pausa_minutos} min | "
                f"Total trabajado: {tiempo.tiempo_trabajado:.2f} hrs"
            )

        print("-"*60)
        print("RESUMEN GENERAL")
        print(f"Cantidad de registros: {tiempos}")
        print(f"Cantidad de proyectos trabajados: {proyecto}")
        print(f"Cantidad de empleados involucrados en proyectos: {empleado}")
        print("-"*60)

    def mostrar_registros_empleado(registros:list, tiempos:int, realizado:int, negativo:int, proyecto:int, rut:str):
        print("-"*60)
        print(f"Registros del empleado {rut}")
        print("-"*60)
        if not registros:
            print("Este empleado no tiene registros de tiempo.")
            return

        print(
            f"{'N.º':<6} {'Fecha':<12} {'Entrada':<10} {'Salida':<10} "
            f"{'Proyecto':<12} {'Pausa':<10} {'Trabajado':<12}"
        )
        print("-" * 100)

        for tiempo in registros:
            print(
                f"{tiempo.id_tiempo:<6} "
                f"{tiempo.fecha.isoformat():<12} "
                f"{tiempo.hora_entrada.strftime('%H:%M'):<10} "
                f"{tiempo.hora_salida.strftime('%H:%M'):<10} "
                f"{tiempo.id_proyecto:<12} "
                f"{tiempo.pausa_minutos:>5} min   "
                f"{tiempo.tiempo_trabajado:>7.2f} h"
            )

        print("-"*60)
        print("RESUMEN GENERAL")
        print(f"Tiempos registrados: {tiempos}")
        print(f"Tiempo trabajado: {realizado}")
        print(f"Tiempo en pausa: {negativo}")
        print(f"Cantidad de proyectos involucrados: {proyecto}")


    def mostrar_registros_proyecto(registros, cant_tiempo, cant_empleado, nom):
        print("-"*60)
        print(f"Registros del Proyecto {nom}")
        print("-"*60)

        for tiempo in registros:
            print(
                f"{tiempo.fecha.isoformat():<12} "
                f"{tiempo.hora_entrada.strftime('%H:%M'):<10} "
                f"{tiempo.hora_salida.strftime('%H:%M'):<10} "
                f"{tiempo.pausa_minutos:>5} min   "
                f"{tiempo.tiempo_trabajado:>7.2f} h"
            )
        print("-"*60)
        print("RESUMEN GENERAL")
        print(f"Cantidad de empleados: {cant_empleado}")
        print(f"Tiempo trabajado: {cant_tiempo}")
        print(f"Tiempo en pausa: {negativo}")
        print(f"Cantidad de proyectos involucrados: {proyecto}")
        
    #mostrar_registros(fecha especifica) --Resumen general y despues todo
    #mostrar_registros(fecha1,fecha2) --Resumen general y despues todo
    
    def mostrar_registros_esp_pro_em(pro, em, registros, cant_re, tiempo, pausa):
        print("-"*60)
        print(f"Registros del Empledo {em} en Proyecto {pro}")
        print("-"*60)
        for tiempo in registros:
            print(
                f"{tiempo.fecha.isoformat():<12} "
                f"{tiempo.hora_entrada.strftime('%H:%M'):<10} "
                f"{tiempo.hora_salida.strftime('%H:%M'):<10} "
                f"{tiempo.pausa_minutos:>5} min   "
                f"{tiempo.tiempo_trabajado:>7.2f} h"
            )
        print("-"*60)
        print("RESUMEN GENERAL")
        print(f"Cantidad de registros: {cant_re}")
        print(f"Tiempo trabajado: {tiempo}")
        print(f"Tiempo en pausa: {pausa}")


    def formulario_tiempo(self)->dict: #falta validar cada dato
        fecha = pedir("fecha")
        print("-"*50)
        hora_entrada = pedir("hora de entrada")
        print("-"*50)
        hora_salida = pedir("hora de salida")
        print("-"*50)
        minutos = pedir("pausa de minutos")
        print("-"*50)
        return {
            'fecha': fecha, 'hora_entrada': hora_entrada, 
            'hora_salida':hora_salida, 'pausa_minutos': minutos
        }