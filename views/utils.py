from pydantic import (TypeAdapter, Field, StringConstraints,ValidationError)
from models.usuario import Usuario
from typing import Annotated
import pwinput

regla_op_inicial = Annotated[int, Field(ge=0,le=2)]
validador_inicial = TypeAdapter(regla_op_inicial)

regla_op = Annotated[int, Field(ge=0, le=5)] #sin rol administrador
validador_op = TypeAdapter(regla_op)

regla_op1 = Annotated[int, Field(ge=0, le=3)]
validador_op1 = TypeAdapter(regla_op1)

regla_op_sup = Annotated[int, Field(ge=0, le=6)] #con rol administrador
validador_op_sup = TypeAdapter(regla_op_sup)

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
        validar = pwinput.pwinput("Confirmar: ")
        if resp in ("si", "no"):
            if usuario.verificar_credencial(validar):
                return True
            return False
        print("Respuesta no válida. Por favor, ingrese 'si' o 'no'.")