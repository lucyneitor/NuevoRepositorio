from views.main_view import MainView
from views.departamento_view import DepartamentoView
from models.departamento import Departamento
from models.departamento_dao import DepartamentoDAO
from models.empleado_dao import EmpleadoDAO
from models.usuario_dao import UsuarioDAO
from views.utils import validador_op_sup, ValidationError, eleccion, pedir, validador_op1, obtener_validador_depa, mostrar_mensaje, confirmar

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
                eleccion(validador_op_sup, opcion)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:            
                if opcion == 0:
                    mostrar_mensaje("Saliendo de la gestión de empleados.")
                    return
                elif opcion == 1:
                    self.agregar_departamento()
                elif opcion in (2,3,6): #en proceso (editar o mostrar)
                    nom = pedir("nombre del departamento")
                    depa = DepartamentoDAO.obtener_nombre(nom)

                    if depa is None:
                        mostrar_mensaje("No existe departamento")
                        return

                    if opcion == 2:
                        self.editar_departamento(depa)
                    elif opcion==3: #mostrar un departamento
                        empleados = EmpleadoDAO.obtener_por_departamento(depa.id_departamento)
                        roles=[]
                        for empleado in empleados:
                            user=UsuarioDAO.obtener_por_rut_empleado(empleado.rut)
                            roles.append(user.rol if user is not None else "Sin usuario")
                        self.departamento_view.mostrar_departamento(depa,empleados,roles)
                    else: #eliminar el departamento
                        if self.departamento_dao.eliminar(depa.id_departamento):
                            mostrar_mensaje("Se elimino departamento exitosamente")
                            continue
                elif opcion == 4:
                    gerente = pedir("nombre del gerente")
                    resultado=self.departamento_dao.obtener_gerente(gerente)
                    self.departamento_view.resultados(resultado,gerente)
                elif opcion == 5:
                    cant_depas = self.mostrar_depa()
                    if cant_depas is None:
                        mostrar_mensaje("Departamento maldito")
                        continue
                    mostrar_mensaje(f"Empresa Ecotech tiene {cant_depas} departamentos")
                else: #agregar opcion eliminar departamento
                    mostrar_mensaje("Opción no válida.")

    def agregar_departamento(self): #falta formulario en view
        nuevo= self.departamento_view.formulario_departamento() #departamento view formulario falta
        depa = Departamento( 
            nombre = nuevo["nombre del departamento"], 
            gerente = nuevo["gerente a cargo"]
        )
        if self.departamento_dao.crear(depa):
            mostrar_mensaje("Se creo departamento exitosamente")
            return
        mostrar_mensaje("Operación fallida en creación de Departamento")

    def editar_departamento(self,depa:Departamento): #incompleto nada creado
        while True:
            self.departamento_view.menu_edit()
            op = pedir("opción")
            try:
                op = int(op)
                eleccion(validador_op1,op)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:
                if op == 0:
                    mostrar_mensaje("Volver al menú principal")
                    return
                
                if op == 1 or op == 3:
                    nom = pedir("nombre nuevo")
                    if confirmar(f"Seguro de este cambio {depa.nombre} -> {nom}"):
                        depa.nombre = nom
                
                if op == 2 or op == 3:
                    gerente = pedir("nuevo gerente")
                    if confirmar(f"Seguro de este cambio {depa.gerente} -> {gerente}"):
                        depa.gerente = gerente

                if DepartamentoDAO.actualizar(depa):
                    mostrar_mensaje("Sección editada exitosamente")
                    return

    def mostrar_depa(self)->int|None:
        if self.departamento_dao.contar_departamentos() == 0:
            print("No hay Departamentos")
            return
        departamentos = self.departamento_dao.obtener_todos() #
        for depa in departamentos:
            depa.empleados = EmpleadoDAO.obtener_por_departamento(
                depa.id_departamento
            )
        self.departamento_view.mostrar_departamentos(departamentos)
        return len(departamentos)

    

            
        
        
