from views.proyecto_view import ProyectoView
from views.utils import pedir,eleccion, validador_op1, validador_dia, validador_op_sup, validador_inicial, validador_time, mostrar_mensaje, ValidationError, confirmar, pedir_texto_valido, validacion_fechas, validador_grande
from models.proyecto import Proyecto
from models.proyecto_dao import ProyectoDAO
from datetime import date
from services.clima_service import ClimaService
from services.moneda_service import MonedaService
from models.tiempo_dao import TiempoDAO
from models.empleado_dao import EmpleadoDAO
from models.transaccion import Transaccion
from models.transaccion_dao import TransaccionDAO

try:
    import requests
    REQUEST_ERROR = requests.exceptions.RequestException
except ImportError:
    REQUEST_ERROR = OSError

class ProyectoController:
    def __init__(self):
        self.proyecto_view = ProyectoView()
        self.proyecto_dao = ProyectoDAO()

    def ejecutar(self):
        while True:
            self.proyecto_view.sub_menu()
            op = pedir("opción")
            try:
                op = int(op)
                eleccion(validador_grande,op)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
            else:
                if op == 0:
                    mostrar_mensaje("Volver al menú de gestiones de empresa")
                    return
                elif op == 1: #Exitoso
                    self.agregar_proyecto()
                elif op in (2,3,4):
                    while True:
                        nom = pedir("nombre del proyecto a modificar")
                        id = ProyectoDAO.obtener_id_por_nombre(nom)
                        try:
                            if not self.proyecto_dao.existe_proyecto(id):
                                raise LookupError("No existe un proyecto con ese ID.")
                        except ValueError:
                            print("Ingresar id entero")
                            continue
                        except LookupError as error:
                            print(error)
                            return
                        else:
                            proyecto=self.proyecto_dao.obtener_proyecto_id(id)
                            if proyecto is None:
                                mostrar_mensaje("Proyecto no se encontro")
                                continue
                            if op == 2:   
                                self.modificar_proyecto(proyecto)
                                break
                            elif op == 3:
                                self.buscar_proyecto(proyecto)
                                break
                            elif op == 4:
                                self.eliminar_proyecto(proyecto)
                                break
                elif op == 5: #Exitoso
                    self.mostrar_proyecto() #todos
                elif op == 6:
                    self.servicio_clima()
                else:
                    nom = pedir("nombre del proyecto a procesar pagos")
                    list_proyect = ProyectoDAO.obtener_ids_y_pais_por_nombre(nom)
                    listado=[]
                    for item in list_proyect:
                        list_empleados = TiempoDAO.obtener_ruts_por_proyecto(item["id_proyecto"])
                        proyecto_paises = {
                            "id": item["id_proyecto"],
                            "pais": item["pais"],
                            "lista de empleados": list_empleados
                        }
                        listado.append(proyecto_paises)  

                    resultados= self.ejecutar_trans(listado)
                    self.proyecto_view.reporte_pago(nom,resultados)

    def agregar_proyecto(self):
        nuevo=self.proyecto_view.formulario()
        crear_proyecto= Proyecto(
            id_proyecto=None, nombre = nuevo["nombre"], descripcion=nuevo["descripcion"], 
            pais_ejecut=nuevo["país"],fecha_inicio = nuevo["fecha_inicio"], fecha_fin=nuevo["fecha_fin"],
            estado=nuevo["estado"]
        )
        if self.proyecto_dao.agregar_proyecto(crear_proyecto): # consultar linea (modificar)
            mostrar_mensaje("Proyecto creado exitosamente")

    def modificar_proyecto(self,proyecto:Proyecto):
        while True:
            self.proyecto_view.menu_modificar()
            op = pedir("opción")
            try: 
                op = int(op)
                eleccion(validador_time,op)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:
                if op == 0:
                    print("Volviendo al menú de proyectos...")
                    return
                
                nombre = proyecto.nombre
                descripcion = proyecto.descripcion
                fecha_inicio = proyecto.fecha_inicio
                fecha_fin = proyecto.fecha_fin
                estado = proyecto.estado

                if op == 1:
                    nombre = pedir_texto_valido("Nuevo nombre del proyecto")
                elif op == 2:
                    descripcion = pedir_texto_valido("Nueva descripción")
                elif op in (3, 4):
                    fecha_inicio = proyecto.fecha_inicio
                    fecha_fin = proyecto.fecha_fin

                    if op == 3:
                        fecha_inicio = pedir(
                            "Nueva fecha de inicio (DD-MM-AAAA)"
                        ).strip()

                    if op == 4:
                        fecha_fin = pedir(
                            "Nueva fecha de término (DD-MM-AAAA)"
                        ).strip()
                    
                    try:
                        fecha_inicio, fecha_fin = validacion_fechas( #validar DD-MM-YYYY
                            fecha_inicio,
                            fecha_fin,
                            "La fecha de término no puede ser anterior a la fecha de inicio.",
                        )
                        
                        estado = self.calcular_estado( #calcular estado
                            fecha_inicio.isoformat(),
                            fecha_fin.isoformat()
                        )
                        
                        fecha_inicio = fecha_inicio.isoformat()
                        fecha_fin = fecha_fin.isoformat()
                    except ValueError as error:
                        print(error)
                        continue  # vuelve al menú de edición
                    mostrar_mensaje("Estado actual del proyecto asignado")
                    
                if confirmar("¿Seguro en editar esto?"):
                    proyecto.nombre = nombre
                    proyecto.descripcion = descripcion
                    proyecto.fecha_inicio = fecha_inicio
                    proyecto.fecha_fin = fecha_fin
                    proyecto.estado = estado
                    if self.proyecto_dao.actualizar_proyecto(proyecto):
                        mostrar_mensaje("Proyecto actualizado exitosamente.")  
                    else:
                        mostrar_mensaje("No se pudo actualizar el proyecto.")
                else:
                    mostrar_mensaje("Cambio cancelado.")
                    

    def calcular_estado(self, fecha_inicio: str, fecha_fin: str) -> str:
        inicio = date.fromisoformat(fecha_inicio)
        fin = date.fromisoformat(fecha_fin)

        if fin < inicio:
            raise ValueError("La fecha de término no puede ser anterior a la de inicio.")

        hoy = date.today()

        mostrar_mensaje("Procesando estado actual del proyecto")

        if hoy < inicio:
            return "Pendiente"
        elif hoy > fin:
            return "Finalizado"
        else:
            return "En proceso"
        
    def buscar_proyecto(self, proyecto:Proyecto):
        self.proyecto_view.mostrar_proyecto(proyecto)

    def eliminar_proyecto(self, proyecto:Proyecto):
        if confirmar(f"¿Esta seguro en eliminar proyecto {proyecto.nombre}?"):
            if self.proyecto_dao.eliminar_proyecto(proyecto.id_proyecto):
                mostrar_mensaje("Proyecto eliminado existosamente")

    def mostrar_proyecto(self):
        proyectos = self.proyecto_dao.obtener_proyectos()

        if proyectos is False:
            mostrar_mensaje("Ocurrió un error al consultar los proyectos.")
            return

        if not proyectos:
            mostrar_mensaje("No hay proyectos registrados.")
            return

        while True:
            self.proyecto_view.menu_mostrar()
            opcion = pedir("opción")

            try:
                opcion = int(opcion)
                eleccion(validador_inicial, opcion)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:
                if opcion == 0:
                    return

                if opcion == 1:
                    opciones = [
                        "id",
                        "nombre",
                        "descripción",
                        "fecha inicio",
                        "fecha fin",
                        "estado",
                    ]

                    self.proyecto_view.mostrar_detalle(opciones, proyectos)
                    mostrar_mensaje("Tabla impresa exitosamente")
                    return

                opciones = []
                seleccionadas = set()

                while True:
                    self.proyecto_view.menu_op2()
                    op = pedir("opción")

                    try:
                        op = int(op)
                        eleccion(validador_op_sup, op)
                    except (TypeError, ValueError, ValidationError) as e:
                        print(e)
                        continue
                    else:
                        if op == 0:
                            mostrar_mensaje("Volver a la gestion de Proyecto")
                            return

                        campos = {
                            1: "nombre",
                            2: "descripción",
                            3: "fecha inicio",
                            4: "fecha fin",
                            5: "estado",
                        }

                        if op in campos:
                            if op in seleccionadas:
                                mostrar_mensaje("Ese campo ya fue seleccionado.")
                                continue

                            opciones.append(campos[op])
                            seleccionadas.add(op)
                            mostrar_mensaje("Campo agregado.")

                        elif op == 6:
                            if not opciones:
                                mostrar_mensaje("Debes seleccionar al menos un campo.")
                                continue

                            self.proyecto_view.mostrar_detalle(
                                opciones,
                                proyectos
                            )

                            return

    def servicio_clima(self):
        while True:
            self.proyecto_view.menu_planificacion()
            op = pedir("opción")
            try:
                op = int(op)
                eleccion(validador_op1, op)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:
                if op == 0:
                    mostrar_mensaje("Volver a la gestion de Proyecto")
                    return

                if op == 1 or op == 2:
                    ciudad = pedir("ciudad de operación terreno")
                    
                    if op == 1:
                        # Opción 1: Clima Actual -> Retorna (msg, resultado, analisis)
                        msg, resultado, analisis = ClimaService.obtener_clima_actual(ciudad)
                        
                        if resultado and analisis:
                            self.proyecto_view.resultado_clima(msg, resultado, analisis)
                        else:
                            print(f"\n❌ {msg}")
                            
                    else: 
                        # Opción 2: Pronóstico a Futuro
                        while True:
                            dias = pedir("días deseados a proyectar (max. 3 días): ")
                            try:
                                dias = int(dias)
                                eleccion(validador_dia, dias)
                            except (TypeError, ValueError, ValidationError) as e:
                                print(e)
                                continue
                            else: 
                                break
                                
                        # Retorna los tres valores específicos del pronóstico: (msg, pronostico, evaluaciones)
                        msg, resultado_pronostico, evaluaciones_pronostico = ClimaService.obtener_pronostico(ciudad, dias)
                        
                        if resultado_pronostico and evaluaciones_pronostico:
                            # Llamamos a su vista exclusiva para pronósticos múltiples
                            self.proyecto_view.resultado_pronostico(msg, resultado_pronostico, evaluaciones_pronostico)
                        else:
                            print(f"\n❌ {msg}")

                else:
                    conexion, msg = ClimaService.probar_conectividad()
                    self.proyecto_view.mostrar_resultado_conectividad(conexion,msg)

    
    def ejecutar_trans(self,listado: list) -> list:
        """
        Calcula los pagos internacionales por proyecto y registra las transacciones en BD.
        """
        preparar_datos = []

        for pago in listado:
            id_proyecto = pago["id"]
            pais_proyecto = pago["pais"]
            ruts_empleados = pago["lista de empleados"]

            print(f"\nProcesando proyecto #{id_proyecto} ({pais_proyecto})...")

            if not ruts_empleados:
                mostrar_mensaje(f"El proyecto #{id_proyecto} no tiene empleados registrados.")
                continue

            # 1. Se resuelve la moneda UNA SOLA VEZ por proyecto (fuera del ciclo)
            try:
                cod_moneda = MonedaService.obtener_moneda_por_pais(pais_proyecto)
            except ValueError as error:
                mostrar_mensaje(f"Dato inválido para {pais_proyecto}: {error}")
                continue
            except (REQUEST_ERROR, RuntimeError) as error:
                mostrar_mensaje(f"Error de conexión al consultar moneda de '{pais_proyecto}': {error}")
                continue

            detalles_empleados = []

            # 2. Dentro del ciclo solo se convierten los sueldos usando esa moneda fija
            for rut in ruts_empleados:
                empleado = EmpleadoDAO.obtener_empleado_por_rut(rut)
                if not empleado:
                    mostrar_mensaje(f"Empleado con RUT {rut} no encontrado. Se omite.")
                    continue

                try:
                    resultado = MonedaService.convertir_clp(empleado.sueldo, cod_moneda)
                except ValueError as error:
                    mostrar_mensaje(f"Error en datos de conversión para {rut} a {cod_moneda}: {error}")
                    continue
                except (REQUEST_ERROR, RuntimeError) as error:
                    mostrar_mensaje(f"Error de red al convertir sueldo de {rut}: {error}")
                    continue

                transaccion = Transaccion(
                    rut=rut,
                    id_proyecto=id_proyecto,
                    sueldo_emp=empleado.sueldo,
                    moneda_origen_clp="CLP",
                    sueldo_pagado=resultado["monto_convertido"],
                    moneda_destino=resultado["moneda_destino"],
                    tasa_cambio=resultado["tasa"],
                    fecha_transaccion=resultado["fecha"],
                )

                if not TransaccionDAO.guardar(transaccion):
                    mostrar_mensaje(f"Advertencia: no se pudo guardar en BD la transacción de {rut}.")

                detalles_empleados.append({
                    "rut": rut,
                    "sueldo_clp": empleado.sueldo,
                    "resultado": resultado,
                })

            if detalles_empleados:
                preparar_datos.append({
                    "pais": pais_proyecto,
                    "codigo_moneda": cod_moneda,
                    "detalles_empleados": detalles_empleados,
                })

        return preparar_datos

        
                

