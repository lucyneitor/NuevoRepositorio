from pydantic import (TypeAdapter, Field, StringConstraints,ValidationError)
from models.usuario import Usuario
from typing import Annotated
from datetime import date
import pwinput
from config.settings import Settings

regla_op_inicial = Annotated[int, Field(ge=0,le=2)]
validador_inicial = TypeAdapter(regla_op_inicial)

regla_op = Annotated[int, Field(ge=0, le=5)] #sin rol administrador
validador_op = TypeAdapter(regla_op)

regla_op1 = Annotated[int, Field(ge=0, le=3)]
validador_op1 = TypeAdapter(regla_op1)

regla_op_sup = Annotated[int, Field(ge=0, le=6)] #con rol administrador
validador_op_sup = TypeAdapter(regla_op_sup)

regla_op_time = Annotated[int, Field(ge=0, le=4)]
validador_time = TypeAdapter(regla_op_time)

regla_op_gran = Annotated[int, Field(ge=0, le=7)]
validador_grande = TypeAdapter(regla_op_gran)

TextoNoVacio = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
validador_texto = TypeAdapter(TextoNoVacio)

def leer_numero(mensaje: str) -> int: #falta un leer texto, leer fecha
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")
def pedir(msg :str):
    variable=input(f"Ingrese su {msg}: ")
    return variable

def eleccion(validador,op):
    try:
        op = int(op)
        op = validador.validate_python(op)
    except ValueError:
        raise ValueError("Debe ingresar un número entero válido.")
    except ValidationError:
        raise ValidationError("Debe ingresar un número dentro del rango permitido.")
    except TypeError:
        raise TypeError(f"Por favor ingrese la opción en numeros no en {type(op)}.")

def conversor(num)->str:
    if num==1:
        return "activo"
    if num==2:
        return "inacativo"
    if num==3:
        return "vacaciones"
    if num==4:
        return "suspendido"

#crear funcion para confirmar movimiento
def confirmar(mensaje: str, usuario:Usuario) -> bool:
    while True:
        resp = input(f"{mensaje} (si/no): ").strip().lower()
        if resp in ("si", "no"):
            if resp=="si":
                mostrar_mensaje("Confirmar con autorización")
                validar = pwinput.pwinput("Ingreso de llave de acceso: ")
                if validar == Settings.ADMIN_INITIAL_CLAVE:
                    return True
            return False
        print("Respuesta no válida. Por favor, ingrese 'si' o 'no'.")

def pedir_texto_valido(self, mensaje: str) -> str:
    while True:
        try:
            entrada = pedir(mensaje)
            return validador_texto.validate_python(entrada)
        except ValidationError:
            print("El texto no puede estar vacío.")

def validacion_fechas(fecha_inicio: str, fecha_fin: str, msg: str) -> tuple[str, str]:
    try:
        inicio = date.fromisoformat(fecha_inicio.strip())
        fin = date.fromisoformat(fecha_fin.strip())
    except (TypeError, ValueError) as error:
        raise ValueError("Usa el formato de fecha AAAA-MM-DD.") from error

    if inicio > fin:
        raise ValueError(msg)

    return inicio.isoformat(), fin.isoformat()

def obtener_validador_depa(departamentos: list) -> TypeAdapter:
    max_id = max(d.id_departamento for d in departamentos)
    regla_op_depa = Annotated[int, Field(ge=1, le=max_id)]
    validador_depa = TypeAdapter(regla_op_depa)
    return validador_depa

@staticmethod
def mostrar_mensaje(mensaje: str) -> None:
    print(f"\n[SISTEMA] {mensaje}")