from views.tiempo_view import TiempoView
from models.tiempo_dao import TiempoDAO
from models.tiempo import Tiempo #ocupar al agregar un tiempo
from views.utils import validador_time, pedir, eleccion, ValidationError, validador_op_sup
from models.empleado_dao import EmpleadoDAO
from models.proyecto_dao import ProyectoDAO
from datetime import date

class TiempoController:
    def __init__(self):
        self.tiempo_view = TiempoView()
        self.tiempo_dao = TiempoDAO()
        self.empleado_dao = EmpleadoDAO()
        self.proyecto_dao = ProyectoDAO()

    def ejecutar(self):
        while True:
            self.tiempo_view.sub_menu()
            op = pedir("opción")
            try:
                op = int(op)
                eleccion(validador_time,op)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
            else:
                if op == 0:
                    print("Volviendo al menú principal...")
                    break
                elif op == 1:
                    self.listar_tiempos()
                elif op == 2:
                    rut = pedir("RUT del empleado")
                    proyecto = pedir("nombre del proyecto")
                    self.agregar_tiempos(rut,proyecto) #creo que listo
                elif op == 3:
                    self.buscar_tiempo()
                elif op == 4:
                    self.actualizar_tiempo()
                else:
                    print("Opción no válida. Ingrese un número del 0 al 4.")

    def listar_tiempos(self):
        while True:
            self.tiempo_view.menu_listar()
            op = pedir("opción")
            try:
                op = int(op)
                eleccion(validador_time,op)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
            else:
                if op == 0:
                    print("Volviendo al menú principal...")
                    break
                elif op == 1:
                    self.listar_registros()
                elif op in (2,3,6):
                    su_rut = pedir("RUT que busca") if op in (2, 6) else None
                    id_proyect = pedir("ID del proyecto") if op in (3, 6) else None
                    if op == 2:
                        self.listar_registros_empleado(su_rut)
                    elif op == 3:
                        self.listar_registros_proyecto(id_proyect)
                    else:
                        self.listar_registros_pro_perso(su_rut, id_proyect)
                elif op in (4, 5):
                    fecha_inicio = pedir("fecha" if op == 4 else "fecha inicial")
                    if op == 4:
                        self.listar_registros_fecha(fecha_inicio)
                    else: 
                        fecha_fin = pedir("fecha límite")
                        self.listar_registros_rango_fecha(fecha_inicio, fecha_fin)
                else:
                    print("Opción no válida. Ingrese un número del 0 al 4.")

    def listar_registros(self): 
        """
        Busca y muestra todos los registros de tiempo, incluido el nombre del proyecto.
        """
        registros = self.tiempo_dao.obtener_todos_tiempos_con_nombre_proyecto()
        cant_tiempo = self.tiempo_dao.contar_tiempos()
        cant_proyect = self.tiempo_dao.contar_proyectos_en_tiempos()
        cant_empleado = self.tiempo_dao.contar_empleados_en_tiempos()
        self.tiempo_view.mostrar_registros(registros,cant_tiempo,cant_proyect,cant_empleado)

    def listar_registros_empleado(self, rut:str): 
        """
        Busca y muestra todos los registros de tiempo del empleado.
        """
        registros = self.tiempo_dao.obtener_todos_tiempos_rut(rut)
        cant_tiempo_registrados = len(registros)# pendiente
        cant_trabajo = sum(registro.tiempo_trabajado for registro in registros)
        cant_basura_tiempo = sum(t.pausa_minutos for t in registros)
        cant_proyect = self.tiempo_dao.contar_proyectos_por_rut(rut)
        self.tiempo_view.mostrar_registros_empleado(
            registros, cant_tiempo_registrados, cant_trabajo,
            cant_basura_tiempo,cant_proyect,rut)

    
    def listar_registros_proyecto(self,id:int): 
        nom = self.proyecto_dao.obtener_proyecto_id(id)
        estado = self.proyecto_dao.obtener_estado(id) # pendiente
        registros = self.tiempo_dao.obtener_tiempos_proyect(id)
        cant_empleado = self.tiempo_dao.contar_empleados_por_proyecto(id)
        cant_tiempo = self.tiempo_dao.sumar_tiempo(id)
        self.tiempo_view.mostrar_registros_proyecto(
            registros, cant_tiempo, cant_empleado, nom)

    
    def listar_registros_pro_perso(self, rut:str, id:int):
        nom_pro = self.proyecto_dao.obtener_proyecto_id(id)
        nom_em = self.empleado_dao.obtener_empleado_por_rut(rut)
        registros = self.tiempo_dao.obtener_todos_tiempos_rut_proyect(rut,id)
        cant_tiempo_registrados = len(registros)
        cant_trabajo = sum(registro.tiempo_trabajado for registro in registros)
        cant_basura_tiempo = self.tiempo_dao.contar_pausa_minutos(rut)
        self.tiempo_view.mostrar_registros_esp_pro_em(nom_pro, nom_em, registros, 
                                                      cant_tiempo_registrados,cant_trabajo, cant_basura_tiempo)

    
    def listar_registros_fecha(self, fecha:date): 
        pass
        registros = self.tiempo_dao.obtener_tiempos_por_fecha(fecha)
        cant_tiempo_registrados = len(registros)
        cant_trabajo = sum(registro.tiempo_trabajado for registro in registros)
        cant_proyectos = self.tiempo_dao.contar_proyectos_en_tiempos()
        self.tiempo_view.mostrar_registros_por_fecha(registros, fecha)

    def listar_registros_rango_fecha(self, fecha1:str, fecha2:str):
        pass
        registros = self.tiempo_dao.contar_tiempos_por_intervalo(fecha1,fecha2)

    
    def agregar_tiempos(self, rut:str, proyect=str):
        """
        Crea registro de tiempo, en base a lo que se registre en formulario y la los datos parametros validarlos
        """
        nuevo= self.tiempo_view.formulario_tiempo() #empleado view formulario
        empleado = self.empleado_dao.obtener_empleado_por_rut(rut) #pendiente
        proyecto = self.proyecto_dao.obtener_id_por_nombre(proyect) #retorna id
        crear_tiempo= Tiempo(
            fecha = nuevo["fecha"], hora_salida=nuevo["hora_salida"], 
            id_empleado=empleado, id_proyecto=proyecto,
            pausa_minutos = nuevo["pausa_minutos"]
        )
        if self.tiempo_dao.crear_tiempo(crear_tiempo): # consultar linea (modificar)
            mensaje="Empleado creado exitosamente"

    def buscar_tiempos(self):
        while True:
            self.tiempo_view.menu_buscar()
            op = pedir("opción")
            try:
                op = int(op)
                eleccion(validador_op_sup,op)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
            else:
                if op == 0:
                    print("Volviendo al menú principal...")
                    break
                elif op in (1,2,3,4,5,6):
                    rut = pedir("RUT del empleado") if op in (2, 6) else None
                    id_proyecto = pedir("ID del proyecto") if op in (3, 6) else None
                    if op == 1:
                        id_tiempo = int(pedir("ID del registro"))
                        registro = self.tiempo_dao.obtener_tiempo_por_id(id_tiempo)
                        registros = [registro] if registro else []
                    elif op == 2:
                        registros = self.tiempo_dao.obtener_todos_tiempos_rut(rut)
                    elif op == 3:
                         registros = self.tiempo_dao.obtener_tiempos_proyect(
                            int(id_proyecto)
                        )
                    elif op == 4:
                        fecha = pedir("Fecha (AAAA-MM-DD)")
                        registros = self.tiempo_dao.obtener_tiempos_por_fecha(fecha)
                    elif op == 5:
                        fecha_inicio = pedir("Fecha inicial (AAAA-MM-DD)")
                        fecha_fin = pedir("Fecha final (AAAA-MM-DD)")
                        registros = self.tiempo_dao.obtener_tiempos_por_intervalo(
                            fecha_inicio,
                            fecha_fin,
                        )
                    else:
                        registros = self.tiempo_dao.obtener_todos_tiempos_rut_proyect(
                            rut,
                            int(id_proyecto),
                        )   
                else:
                    print("Opción no válida. Ingrese un número del 0 al 6.")

                self.tiempo_view.vista_busqueda(registros)

    def actualizar_tiempo(self): 
        """
        Solicita el ID de un registro de tiempo, valida su existencia 
        y actualiza sus datos utilizando el formulario y el DAO.
        """
        try:
            id_tiempo = int(pedir("ID del registro de tiempo a actualizar"))
        except (TypeError, ValueError):
            print("El ID ingresado debe ser un número entero.")
            return

        # Verificar si el registro existe en la base de datos
        registro_existente = self.tiempo_dao.obtener_tiempo_por_id(id_tiempo)
        if registro_existente is None:
            print(f"No se encontró ningún registro de tiempo con el ID {id_tiempo}.")
            return

        print(f"Registro encontrado (ID: {id_tiempo}). Ingrese los nuevos datos:")
        nuevo = self.tiempo_view.formulario_tiempo()

        # Creamos la instancia actualizada (puedes conservar los valores anteriores si alguno viene vacío)
        tiempo_actualizado = Tiempo(
            id=id_tiempo,  # Asegúrate de que tu modelo Tiempo acepte el ID si es necesario para la actualización
            fecha=nuevo.get("fecha", registro_existente.fecha),
            hora_salida=nuevo.get("hora_salida", registro_existente.hora_salida),
            id_empleado=registro_existente.id_empleado,
            id_proyecto=registro_existente.id_proyecto,
            pausa_minutos=nuevo.get("pausa_minutos", registro_existente.pausa_minutos)
        )

        # Llamada al DAO para actualizar (asumiendo que tu DAO tiene un método actualizar_tiempo)
        if self.tiempo_dao.actualizar_tiempo(tiempo_actualizado):
            print("¡Registro de tiempo actualizado exitosamente!")
        else:
            print("Ocurrió un error al intentar actualizar el registro en la base de datos.")