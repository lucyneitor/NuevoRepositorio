from views.proyecto_view import ProyectoView
from views.utils import pedir,eleccion, validador_op_sup, validador_inicial, validador_time, validador_op, ValidationError, confirmar, pedir_texto_valido, validacion_fechas
from models.proyecto import Proyecto
from models.proyecto_dao import ProyectoDAO
from datetime import date

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
                eleccion(validador_op,op)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
            else:
                if op == 0:
                    break
                elif op == 1:
                    self.agregar_proyecto()
                elif op in (2,3,4):
                    while True:
                        id = pedir("ID del proyecto a modificar")
                        try:
                            id = int(id)
                            if not self.proyecto_dao.existe_proyecto(id):
                                raise LookupError("No existe un proyecto con ese ID.")
                        except ValueError:
                            print("Ingresar id entero")
                            continue
                        except LookupError as error:
                            print(error)
                            continue
                        else:
                            datos=self.proyecto_dao.obtener_proyecto_id(id)
                            proyecto = Proyecto(
                                id_proyecto=datos["id_proyecto"],
                                nombre=datos["nombre"],
                                descripcion=datos["descripcion"],
                                fecha_inicio=datos["fecha_inicio"],
                                fecha_fin=datos["fecha_fin"],
                                estado=datos["estado"],
                            )
                            if op == 2:   
                                self.modificar_proyecto(proyecto)
                            elif op == 3:
                                self.buscar_proyecto(proyecto)
                            elif op == 4:
                                self.eliminar_proyecto(proyecto)
                elif op == 5:
                    self.mostrar_proyectos()

    def agregar_proyecto(self):
        nuevo=self.proyecto_view.formulario()
        crear_proyecto= Proyecto(
            nombre = nuevo["nombre"], descripcion=nuevo["descripcion"], 
            fecha_inicio = nuevo["fecha_inicio"], fecha_fin=nuevo["fecha_fin"],
            estado=nuevo["estado"]
        )
        if self.proyecto_dao.crear_tiempo(crear_proyecto): # consultar linea (modificar)
            mensaje="Empleado creado exitosamente"

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
                    break
                
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
                        fecha_inicio, fecha_fin = validacion_fechas(
                            fecha_inicio,
                            fecha_fin,
                            "La fecha de término no puede ser anterior a la fecha de inicio.",
                        )
                    except ValueError as error:
                        print(error)
                        continue  # vuelve al menú de edición

                    
                if confirmar("¿Seguro en editar esto?",self.usuario):
                    proyecto.nombre = nombre
                    proyecto.descripcion = descripcion
                    proyecto.fecha_inicio = fecha_inicio
                    proyecto.fecha_fin = fecha_fin
                    proyecto.estado = estado
                    if self.proyecto_dao.actualizar_proyecto(proyecto):
                        print("Proyecto actualizado exitosamente.")
                        
                    else:
                        print("No se pudo actualizar el proyecto.")
                    break
                else:
                    print("Cambio cancelado.")
                    break



    def calcular_estado(self, fecha_inicio: str, fecha_fin: str) -> str:
        inicio = date.fromisoformat(fecha_inicio)
        fin = date.fromisoformat(fecha_fin)

        if fin < inicio:
            raise ValueError("La fecha de término no puede ser anterior a la de inicio.")

        hoy = date.today()

        if hoy < inicio:
            return "Pendiente"
        elif hoy > fin:
            return "Finalizado"
        else:
            return "En proceso"
        
    def buscar_proyecto(self, proyecto:Proyecto):
        self.proyecto_view.mostrar_proyecto(proyecto)

    def eliminar_proyecto(self, proyecto:Proyecto):
        if confirmar(f"¿Esta seguro en eliminar proyecto {proyecto.__nombre}?"):
            self.proyecto_dao.eliminar_proyecto(proyecto.__id_proyecto)

    def mostrar_proyecto(self):
        proyectos = self.proyecto_dao.obtener_proyectos()

        if proyectos is False:
            print("Ocurrió un error al consultar los proyectos.")
            return

        if not proyectos:
            print("No hay proyectos registrados.")
            return

        while True:
            self.proyecto_view.menu_mostrar()
            op = pedir("opción")
            try:
                op= int(op)
                eleccion(validador_inicial,op)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:
                if op == 0:
                    break
                elif op == 1:
                    self.proyecto_view.mostrar_proyectos(proyectos)
                    return
                else:
                    opciones = []
                    registro = []
                    while True:
                        self.proyecto_view.menu_op2()
                        op = pedir("opción")
                        try:
                            op = int(op)
                            eleccion(validador_op_sup,op)
                        except (TypeError, ValueError, ValidationError) as e:
                            print(e)
                            continue
                        else:
                            if op == 0:
                                print("Volviendo al menú de gestiones...")
                                return
                            elif op == 1 and not(op in registro):
                                opciones.append("nombre")
                                registro.append(1)
                            elif op == 2 and not(op in registro):
                                opciones.append("descripción")
                                registro.append(2)
                            elif op == 3 and not(op in registro):
                                opciones.append("fecha inicio")
                                registro.append(3)
                            elif op == 4 and not(op in registro):
                                opciones.append("fecha fin")
                                registro.append(4)
                            elif op == 5 and not(op in registro):
                                opciones.append("estado")
                                registro.append(5)
                            elif op == 6:
                                if len(opciones) == 0:
                                    print("Si quieres mostrar algo especifico")
                                    continue

                                self.proyecto_view.mostrar_detalle(opciones, proyectos)

                                print("Volviendo al menú de proyectos...")
                                break

