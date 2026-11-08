from views.proyecto_view import ProyectoView
from views.utils import pedir,eleccion,validador_op, ValidationError, confirmar
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
                elif op == 2:
                    self.modificar_proyecto()
                #elif op == 3:
                    #self.buscar_proyecto()
                #elif op == 4:
                    #self.eliminar_proyecto()
                #elif op == 5:
                    #self.mostrar_proyectos()

    def agregar_proyecto(self):
        nuevo=self.proyecto_view.formulario()
        crear_proyecto= Proyecto(
            nombre = nuevo["nombre"], descripcion=nuevo["descripcion"], 
            fecha_inicio = nuevo["fecha_inicio"], fecha_fin=nuevo["fecha_fin"],
            estado=nuevo["estado"]
        )
        if self.proyecto_dao.crear_tiempo(crear_proyecto): # consultar linea (modificar)
            mensaje="Empleado creado exitosamente"

    def modificar_proyecto(self):
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
                break

        proyecto = Proyecto(
            id_proyecto=datos["id_proyecto"],
            nombre=datos["nombre"],
            descripcion=datos["descripcion"],
            fecha_inicio=datos["fecha_inicio"],
            fecha_fin=datos["fecha_fin"],
            estado=datos["estado"],
        )
        
        while True:
            self.proyecto_view.menu_modificar()
            op = pedir("opción")
            try: 
                op = int(op)
                eleccion(validador_op,op)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:
                if op == 0:
                    print("Volviendo al menú de proyectos...")
                    break
                elif op == 1:
                    proyecto.nombre = pedir("Nuevo nombre del proyecto")
                elif op == 2:
                    proyecto.descripcion = pedir("Nueva descripción")
                elif op in (3, 4, 5):
                    fecha_inicio = proyecto.fecha_inicio
                    fecha_fin = proyecto.fecha_fin

                    if op in (3, 5):
                        fecha_inicio = pedir(
                            "Nueva fecha de inicio (AAAA-MM-DD)"
                        ).strip()

                    if op in (4, 5):
                        fecha_fin = pedir(
                            "Nueva fecha de término (AAAA-MM-DD)"
                        ).strip()

                    inicio = date.fromisoformat(fecha_inicio)
                    fin = date.fromisoformat(fecha_fin)

                    if fin < inicio:
                        print("La fecha de término no puede ser anterior a la fecha de inicio.")
                        continue

                    proyecto.fecha_inicio = inicio.isoformat()
                    proyecto.fecha_fin = fin.isoformat()
                    proyecto.estado = self.calcular_estado(
                        fecha_inicio,
                        fecha_fin,
                    )
                if confirmar("¿Seguro en editar esto?",self.usuario):
                    if self.proyecto_dao.actualizar_proyecto(proyecto):
                        print("Proyecto actualizado exitosamente.")
                    else:
                        print("No se pudo actualizar el proyecto.")
                else:
                    print("Cambio cancelado.")



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
    #def buscar_proyecto(self):
        #
        #
        #
        #

    #def eliminar_proyecto(self):
        

    #def mostrar_proyecto(self):