from views.main_view import MainView
from views.empleado_view import EmpleadoView
from models.empleado import Empleado
from models.empleado_dao import EmpleadoDAO
from views.utils import validador_op1, eleccion, pwinput, pedir, validador_op_sup,ValidationError,confirmar
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
        self.empleado_view.sub_menu
        opcion = input() #te amo mucho mi vida
        eleccion(validador_op1, opcion)
        opcion = int(opcion)
        if opcion == 1:
            activacion = input("Tendrá rol de administrador (si/no): ") #el usuario no decide quien es administrador
            autoriza = pwinput.pwinput("Confirmación: ")
            if activacion.lower() == "si":
                if autoriza == self.settings.ADMIN_SHARED_PASSWORD:
                    rol = True
                else:
                    print("Rol Administrador denegada")
                    rol = False
                rol = True
            else:
                rol = False
            self.agregar_empleado(rol)
        elif opcion in (2,3,4):
            rut = input("Ingrese su rut: ")
            if opcion==2:
                self.editar_empleado(self.usuario)
            elif opcion == 3:
                self.eliminar_empleado(rut)
            elif opcion == 4:
                self.imprimir_empleado(rut)
        elif opcion == 5:
            self.imprimir_empleados()
        elif opcion == 0:
            self.main_view.mostrar_mensaje("Saliendo de la gestión de empleados.")
            self.main_view.mostrar_menu()
        else:
            self.main_view.mostrar_mensaje("Opción no válida.")

    def agregar_empleado(self, valor): #crea usuario que no es el
        nuevo= self.empleado_view.formulario_empleado() #empleado view formulario
        depa = self.escoger_depa()
        crear_empleado= Empleado( #creo el departamento
            sueldo=nuevo["sueldo"], inicio_contrato=nuevo["contrato"], estado="activo", 
            rut=nuevo["rut"], nombre=nuevo['nombre'], direccion=nuevo['dirección'],
            telefono=nuevo['telefono'], correo=nuevo['correo'], selec_depa=depa
        )
        if EmpleadoDAO.crear_empleado(crear_empleado): # consultar linea (modificar)
            mensaje="Empleado creado exitosamente"
        crear_usuario = Usuario(
            username=nuevo['usuario'], password_hash=nuevo['contraseña'], 
            nombre_completo=nuevo['nombre'], rol=valor
        )
        if UsuarioDAO.crear(crear_usuario):
            mensaje="Usuario creado exitosamente"
    
    def editar_empleado(self): #usar actualizar aqui 
        self.empleado_view.menu_edit()
        op = pedir("opinión")
        try:
            op = int(op)
            eleccion(validador_op_sup, op)
        except (TypeError, ValueError, ValidationError) as e:
            print(e)
        else:
            autorizado = confirmar("¿Está seguro de editar esto?", self.usuario) #cuestionar si se autorizo o no

    def escoger_depa(self)->int | None:
        cant = self.departamento_dao.contar_departamentos()
        if cant == 1:
            print(f"Fuiste asignado al departamento {self.departamento_dao.obtener_por_id(1)}")
            return cant
        regla_op_depa = Annotated[int, Field(ge=1,le=self.departamento_dao.contar_departamentos())]
        validador_depa = TypeAdapter(regla_op_depa)
        while True:
            self.departamento_controller.mostrar_depa()
            op = pedir("opción")
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
