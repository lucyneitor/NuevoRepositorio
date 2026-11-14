from views.utils import leer_numero, confirmar
from models.usuario import Usuario
from views.utils import pwinput
class AuthView:
    """
    Vista de consola para el Inicio de Sesión y la Gestión de Usuarios con Credenciales Encriptadas.
    """

    @staticmethod
    def mostrar_banner_login(intento_actual: int, max_intentos: int) -> None:
        print("\n" + "=" * 55)
        print("   SISTEMA DE ECOTECH - INICIO DE SESIÓN SEGURO (SHA-256)")
        print("=" * 55)
        print(f"Intento {intento_actual} de {max_intentos} (Por defecto: admin / admin1234)")
        print("-" * 55)

    @staticmethod
    def solicitar_credenciales() -> dict:
        username = input("Usuario    : ").strip()
        clave = pwinput.pwinput("Contraseña : ").strip()
        return {
            "username": username,
            "clave": clave
        }

    @staticmethod
    def mostrar_bienvenida(usuario: Usuario) -> None:
        print("\n" + "*" * 55)
        print(f"  [ACCESO CONCEDIDO] Bienvenido/a, {usuario.nombre_completo}")
        print(f"  Usuario: {usuario.username} | Rol: {usuario.rol}")
        print("*" * 55)

    @staticmethod
    def mostrar_menu_usuarios() -> int:
        print("\n" + "-" * 45)
        print("   GESTIÓN DE USUARIOS Y CREDENCIALES")
        print("-" * 45)
        print("1.- Registrar nuevo usuario (Encriptar clave)")
        print("2.- Listar usuarios y verificar hashes SHA-256")
        print("3.- Eliminar usuario")
        print("0.- Volver al menú principal")
        print("-" * 45)
        return leer_numero("Seleccione una opción: ")

    @staticmethod
    def formulario_nuevo_usuario(rut:str|None, nom:str|None, rol:str|None) -> dict:
        print("\n--- Registrar Nuevo Usuario ---")
        username = input("Ingrese nombre de usuario (mín. 3 caracteres, sin espacios): ").strip()
        if nom is None:
            nom = input("Ingrese nombre completo del funcionario: ").strip()
        clave = pwinput.pwinput("Ingrese contraseña (mín. 4 caracteres, se encriptará con SHA-256): ",mask="*").strip()
        confirmacion = pwinput.pwinput("Confirme la contraseña: ").strip()
        if rol is None:
            print("Roles disponibles: 1.- Administrador, 2.- Empleado")
            opcion_rol = leer_numero("Seleccione un rol (1-2): ")
            mapa_roles = {1: "Administrador", 2: "Empleado"}
            rol = mapa_roles.get(opcion_rol, "")
        if rut is None:
            rut = input("Ingrese el RUT del empleado registrado: ").strip()

        return {
            "username": username,
            "nombre_completo": nom,
            "clave": clave,
            "confirmacion": confirmacion,
            "rol": rol,
            "rut_empleado": rut,
        }

    @staticmethod
    def mostrar_lista_usuarios(usuarios: list[Usuario]) -> None:
        print("\n--- Lista de Usuarios Registrados (Credenciales Encriptadas) ---")
        if not usuarios:
            print("No hay usuarios registrados.")
        else:
            for u in usuarios:
                print(u)
        print("-" * 64)

    @staticmethod
    def solicitar_id_usuario() -> int:
        return leer_numero("Ingrese el ID del usuario a eliminar: ")

    @staticmethod
    def confirmar_eliminacion(username: str) -> bool:
        return confirmar(f"¿Está seguro que desea eliminar al usuario '{username}'?")

    @staticmethod
    def mostrar_mensaje(mensaje: str) -> None:
        print(f"\n[AUTENTICACIÓN] {mensaje}")

    @staticmethod
    def mostrar_error(error: str) -> None:
        print(f"\n[ERROR DE CREDENCIALES] {error}")