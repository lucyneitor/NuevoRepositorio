from views.main_view import MainView
from views.departamento_view import DepartamentoView
from models.departamento import Departamento
from models.departamento_dao import DepartamentoDAO
from models.empleado_dao import EmpleadoDAO
from views.utils import validador_op1, ValidationError, eleccion, pedir

class DepartamentoController:
    def __init__(self):
        self.main_view = MainView()
        self.departamento_view = DepartamentoView()
        self.departamento_dao = DepartamentoDAO()

    def ejecutar(self): #corregir todo
        while True:
            self.departamento_view.sub_menu()
            opcion = pedir("opción")
            try:
                opcion = int(opcion)
                eleccion(validador_op1, opcion)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:            
                if opcion == 0:
                    self.view.mostrar_mensaje("Saliendo de la gestión de empleados.")
                    self.main_view.mostrar_menu() 
                elif opcion == 1:
                    self.agregar_departamento()
                elif opcion in (2,3):
                    elemento = pedir("hichisbvsbc")
                    if opcion == 2:
                        self.editar_departamento(elemento)
                    else:
                        self.buscar_departamento(elemento)
                elif opcion == 4:
                    self.mostrar_departamentos()
                elif opcion == 0:
                    self.view.mostrar_mensaje("Saliendo de la gestión de empleados.")
                    self.main_view.mostrar_menu()
                else:
                    self.view.mostrar_mensaje("Opción no válida.")

    def agregar_departamento(self, valor):
        self.main_view.ejecutar()
        nuevo= self.departamento_view.formulario_departamento() #empleado view formulario
        depa = Departamento( 
            nombre= nuevo["nombre de departamento"], 
            gerente= nuevo["nombre del gerente"]
        )
        self.departamento_dao.crear_departamento(depa)

    def editar_departamento(self,elemento:object): #falva confirmacion
        while True:
            self.departamento_view.menu_edit()
            opcion = pedir("opcion")
            try:
                opcion = int(opcion)
                eleccion(validador_op1, opcion)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:
                if opcion == 0: 
                    print("Entendido... Operación cancelada")
                    return
                elif opcion in (1,2):
                    if opcion == 1:
                        pal = "nombre del departamento"
                    else:
                        pal = "gerente"
                    self.main_view.titulo_funcion(2,pal)
                    nuevo = pedir(pal) #crear una función de confirmación
                    if opcion == 1:
                        elemento.nombre = nuevo
                    else:
                        elemento.gerente = nuevo
                self.departamento_dao.actualizar(elemento)
                print(f"{pal} editado exitosamente")

    def mostrar_depa(self):
        if self.departamento_dao.contar_departamentos() == 0:
            print("No hay Departamentos")
            return
        departamentos = self.departamento_dao.obtener_todos()
        self.departamento_view.mostrar_departamentos(departamentos)
               
            
            
        
        
