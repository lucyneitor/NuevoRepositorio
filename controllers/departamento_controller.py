from views.main_view import MainView
from views.departamento_view import DepartamentoView
from models.departamento import Departamento
from models.departamento_dao import DepartamentoDAO
from models.empleado_dao import EmpleadoDAO
from views.utils import validador_op, ValidationError, eleccion, pedir, validador_time

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
                eleccion(validador_op, opcion)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:            
                if opcion == 0:
                    self.main_view.mostrar_mensaje("Saliendo de la gestión de empleados.")
                    return
                elif opcion == 1:
                    self.agregar_departamento()
                elif opcion in (2,5): #en proceso (editar o mostrar)
                    pal="editar" if opcion==2 else "mostrar"
                    self.departamento_view.menu_edit_condicion(pal)
                    op = pedir("opcion")
                    try:
                        op = int(op)
                        eleccion(validador_time, op) #corregir validador
                    except (TypeError, ValueError, ValidationError) as e:
                        print(e)
                        continue
                    else:
                        resp=[
                            {"tipo": "nombre", "valor": " "},
                            {"tipo": "gerente", "valor": " "}
                        ]
                        if op == 0: 
                            print("Entendido... Operación cancelada")
                            self.ejecutar()
                        elif op == 1:
                            nom = pedir("nombre del que quiere editar" if opcion==2 else "nombre que quiere mostrar")
                            resp[0]["valor"] = nom
                            if self.busqueda_especifica(op,resp):
                                if opcion == 2:
                                    self.editar_departamento(nom) 
                                else:
                                    self.mostrar_depa_esp(nom)
                            
                        elif op == 2:
                            gerente = pedir("gerente que desea editar" if opcion == 2 else "gerente que quiere mostrar")
                            resp[1]["valor"] = gerente
                            if self.busqueda_especifica(op,resp):
                                if opcion == 2:
                                    self.editar_departamento(gerente)
                                else: 
                                    self.mostrar_direct_gerente(gerente)
                        elif op == 3:
                            nom = pedir("nombre del que quiere editar" if opcion==2 else "nombre que quiere mostrar")
                            resp[0]["valor"] = nom
                            gerente = pedir("gerente que desea editar" if opcion == 2 else "gerente que quiere mostrar")
                            resp[1]["valor"] = gerente
                            if self.busqueda_especifica(op,resp):
                                if opcion == 2:
                                    self.editar_departamento(resp)
                                else:
                                    self.mostrar_empleados(resp)
                        else:
                            if opcion == 2:
                                self.editar_departamento()
                            else:
                                self.mostrar_depa() # falta
                elif opcion in (3,4): # opciones de busqueda

                    self.mostrar_depa()
                    op = pedir("opcion")
                    try:
                        op = int(op)
                        eleccion(validador_op1, opcion)
                    except (TypeError, ValueError, ValidationError) as e:
                        print(e)
                        continue
                    else:
                        if op == 0:
                            print("Entendido... Operación cancelada")
                            return
                        elif op == 1: #buscar por nombre de departamento (devuelve gerente y la lista de empleados que maneja)
                            nom = pedir("nombre")
                            depa_resultados =self.departamento_dao.obtener_nombre(nom)
                        elif op == 2: #buscar por nombre de gerente (devuelve id_departamento y los nom departamentos que maneja)
                            gerente = pedir("gerente")
                            list_dict = self.departamento_dao.obtener_gerente(gerente) 
                            print("Encontrado!!!")
                            self.departamento_view.resultados(list_dict,gerente)
                else:
                    self.main_view.mostrar_mensaje("Opción no válida.")

    def agregar_departamento(self):
        nuevo= self.departamento_view.formulario_departamento() #departamento view formulario falta
        depa = Departamento( 
            nombre= nuevo["nombre de departamento"], 
            gerente= nuevo["nombre del gerente"]
        )
        self.departamento_dao.crear(depa) 

    def editar_departamento(self,elemento:object): #incompleto
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
        departamentos = self.departamento_dao.obtener_todos() #
        self.departamento_view.mostrar_departamentos(departamentos)

    def buscar(self, op):
        self.mostrar_depa()
        if op == 1:
            self.departamento_dao.obtener_por_id()

    def busqueda_especifica(self,alternativa:int,resp)->bool:
        if alternativa == 1: # existencia del nombre de departamento
            objeto = self.departamento_dao.obtener_nombre(resp[0]["valor"])
            if objeto is None:
                return False
            return True
        elif alternativa == 2: #existencia del gerente
            list_resultado = self.departamento_dao.obtener_gerente(resp[1]["valor"])
            if len(list_resultado) == 0:
                return False
            return True
        elif alternativa == 3: #lista empleado
            booleano = self.departamento_dao.verificar_depa_gerente(resp[0]["valor"],resp[1]["valor"])
            return booleano

            
        
        
