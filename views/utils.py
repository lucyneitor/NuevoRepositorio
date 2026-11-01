from pydantic import (TypeAdapter, Field, StringConstraints,ValidationError)
from typing import Annotated

regla_op_inicial = Annotated[int, Field(ge=0,le=2)]
validador_inicial = TypeAdapter(regla_op_inicial)

regla_op = Annotated[int, Field(ge=0, le=4)] #sin rol administrador
validador_op = TypeAdapter(regla_op)

regla_op_sup = Annotated[int, Field(ge=0, le=5)] #con rol administrador
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
            op = validador.validate_strings(op)
        except TypeError:
            print("Por favor, ingrese la opcion que corresponda")

def conversor(num)->str:
    if num==1:
        return "activo"
    if num==2:
        return "inacativo"
    if num==3:
        return "vacaciones"
    if num==4:
        return "suspendido"