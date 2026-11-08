from views.tiempo_view import TiempoView
from views.utils import validador_time, pedir, eleccion, ValidationError

class TiempoController:
    def __init__(self):
        self.tiempo_view = TiempoView()
    
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
                #elif op == 2:
                    #self.agregar_tiempo()
                #elif op == 3:
                    #self.buscar_tiempo()
                #elif op == 4:
                    #self.actualizar_tiempo()
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

    #def listar_registros(): --obtener todos y luego llamar funcion de vista
    #def listar_registros_empleado(rut:str): --obtener todos y luego llamar funcion de vista
    #def listar_registros_proyecto(id:int): --obtener todos y luego llamar funcion de vista
    #def listar_registros_pro_perso(rut:str, id:int):--obtener todos y luego llamar funcion de vista
    #def listar_registros_fecha(fecha:date): --obtener todos y luego llamar funcion de vista
    #def listar_registros_rango_fecha(fecha1:str, fecha2:str): --obtener todos y luego llamar funcion de vista


    #def agregar_tiempos(): --Crear tiempo dao
        
    #def buscar_tiempos(): --buscar en dao
    #def actualizar_tiempo(): -- sub_menu para saber que quiere actualizar