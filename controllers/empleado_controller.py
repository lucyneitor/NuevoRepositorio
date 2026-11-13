from views.main_view import MainView
from views.empleado_view import EmpleadoView
from models.empleado import Empleado
from models.empleado_dao import EmpleadoDAO
from views.utils import validador_time, eleccion, pwinput, pedir, validador_op_sup,ValidationError,confirmar
from config.settings import Settings
from models.usuario import Usuario
from models.usuario_dao import UsuarioDAO
from models.departamento_dao import DepartamentoDAO
from views.departamento_view import DepartamentoView
from controllers.departamento_controller import DepartamentoController
from views.utils import Annotated, Field, TypeAdapter

class EmpleadoController:
    def __init__(self, usuario:Usuario):
        self.main_view = MainView()
        self.empleado_view = EmpleadoView()
        self.settings = Settings
        self.departamento_dao = DepartamentoDAO()
        self.departamento_view = DepartamentoView()
        self.usuario = usuario
        self.departamento_controller = DepartamentoController()

    def ejecutar(self): #editar
        while True:
            self.empleado_view.sub_menu()
            opcion = pedir("opción") 
            try:
                eleccion(validador_time, opcion)
                opcion = int(opcion)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
            else:
                if opcion == 1:
                    es_admin = confirmar("¿Tendrá rol de administrador?", self.usuario)
                    rol = "Administrador" if es_admin else "Empleado"
                    self.agregar_empleado(rol)
                elif opcion in (2,3,4):
                    rut = input("Ingrese su rut: ") #antes de distribuirse se debe verificar existencia 
                    if opcion==2:
                        self.editar_empleado(self.usuario)
                    elif opcion == 3:
                        self.eliminar_empleado(rut)
                    elif opcion == 4:
                        self.imprimir_empleado(rut)
                elif opcion == 5:
                    self.mostrar_empleados()
                elif opcion == 0:
                    self.main_view.mostrar_mensaje("Saliendo de la gestión de empleados.")
                    return
                else:
                    self.main_view.mostrar_mensaje("Opción no válida.")

    def agregar_empleado(self, valor): #crea usuario que no es el
        nuevo= self.empleado_view.formulario_empleado() #empleado view formulario
        nuevo["contraseña"]=self.usuario.encriptar_credencial(nuevo["contraseña"])
        depa = self.escoger_depa()
        crear_empleado= Empleado( #creo el departamento
            sueldo=nuevo["sueldo"], inicio_contrato=nuevo["contrato"], estado="activo", 
            rut=nuevo["rut"], nombre=nuevo['nombre'], direccion=nuevo['dirección'],
            telefono=nuevo['telefono'], correo=nuevo['correo'], id_departamento=depa
        )
        if not EmpleadoDAO.agregar_empleado(crear_empleado): # consultar linea (modificar)
            print("No se pudo guardar el empleado.")
            return
        
        crear_usuario = Usuario(
            username=nuevo['usuario'], password_hash=nuevo['contraseña'], 
            nombre_completo=nuevo['nombre'], rol=valor
        )
        if UsuarioDAO.crear(crear_usuario):
            print("Empleado y usuario creados exitosamente.")
        else:
            EmpleadoDAO.eliminar_empleado(nuevo["rut"])  # deshacer para no tener inconcruencias
            print("No se pudo crear el usuario; se canceló el registro del empleado.")
    
    def editar_empleado(self): #usar actualizar aqui 
        self.empleado_view.menu_edit()
        op = pedir("opción")
        try:
            op = int(op)
            eleccion(validador_op_sup, op)
        except (TypeError, ValueError, ValidationError) as e:
            print(e)
        else:
            autorizado = confirmar("¿Está seguro de editar esto?", self.usuario) #cuestionar si se autorizo o no
            if autorizado:
                EmpleadoDAO.actualizar_empleado()

    def escoger_depa(self)->int | None:
        departamentos = self.departamento_dao.obtener_todos()
        if not departamentos:
            print("No hay departamentos: el empleado quedará sin departamento temporalmente.")
            return None

        if len(departamentos) == 1:
            unico_dep = departamentos[0]
            print(f"Fuiste asignado al departamento {unico_dep.nombre}")
            return unico_dep.id_departamento
        
        regla_op_depa = Annotated[int, Field(ge=1,le={d.id_departamento for d in departamentos})]
        validador_depa = TypeAdapter(regla_op_depa)

        while True:
            self.departamento_controller.mostrar_depa()
            op = pedir("ID del departamento")
            eleccion(validador_depa,op)
            try:
                op = int(op)
                eleccion(validador_depa,op)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:
                if confirmar("¿Está seguro de pertenecer a este departamento?", self.usuario):
                    print("Operación exitosa")
                    return op
                print("Operación fallida: No estas autorizado")
                return None

    def eliminar_empleado(self, rut:str): #cambia solo el estado
        empleados=EmpleadoDAO.obtener_todos_empleado_estado("activo")
        EmpleadoDAO.obtener_empleado_por_rut
        if EmpleadoDAO.eliminar_empleado(rut):
            print("Usuario eliminado de contrato")
    
    def imprimir_empleado(self,rut):
        existe=EmpleadoDAO.obtener_empleado_por_rut(rut)
        if existe is not None:
            self.empleado_view.mostrar_empleado(existe)
        else:
            print("No se encontró ningún empleado con el RUT ingresado.")
            print("=" * 50)
            return

    def mostrar_empleados(self):
        empleados = EmpleadoDAO.obtener_todos_empleado_estado("activo") #los que estan contratados
        self.empleado_view.mostrar_empleados(empleados)

