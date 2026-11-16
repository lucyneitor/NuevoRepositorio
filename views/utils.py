from pydantic import (TypeAdapter, Field, StringConstraints,ValidationError)
from typing import Annotated
from datetime import date, datetime
import pwinput
from config.settings import Settings

regla_op_inicial = Annotated[int, Field(ge=0,le=2)]
validador_inicial = TypeAdapter(regla_op_inicial)

regla_dia = Annotated[int, Field(ge=1, le=2)]
validador_dia = TypeAdapter(regla_dia)

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
            num = int(input(mensaje))
            return num
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
        return "inactivo"
    if num==3:
        return "vacaciones"
    if num==4:
        return "suspendido"

#crear funcion para confirmar movimiento
def confirmar(mensaje: str) -> bool:
    print(">"*60)
    while True:
        resp = input(f"{mensaje} (si/no): ").strip().lower()
        if resp in ("si", "no"):
            if resp=="si":
                mostrar_mensaje("Confirmar con autorización")
                validar = pwinput.pwinput("<<Ingreso de llave de acceso>> ")
                if validar == Settings.ADMIN_INITIAL_CLAVE:
                    return True
            return False
        print("Respuesta no válida. Por favor, ingrese 'si' o 'no'.")

@staticmethod
def pedir_texto_valido(mensaje: str) -> str:
    while True:
        try:
            entrada = pedir(mensaje)
            return validador_texto.validate_python(entrada)
        except ValidationError:
            print("El texto no puede estar vacío.")

@staticmethod
def validacion_fechas(fecha_inicio: str | date, fecha_fin: str | date, msg: str) -> tuple[str, str]:
    inicio = convertir(fecha_inicio)
    fin = convertir(fecha_fin)

    if inicio > fin:
        raise ValueError(msg)

    return inicio.isoformat(), fin.isoformat()

def valida_fecha(msg:str):
    while True:
        fecha = pedir(msg)
        try:
            fecha = datetime.strptime(fecha, "%d-%m-%Y")
            return fecha.strftime("%Y-%m-%d")
        except ValueError:
            mostrar_mensaje("Formato de fecha inválido. Use DD-MM-YYYY (ej. 26-11-2026)")

def valida_hora(msg):
    while True:
        hora = pedir(msg)
        try:
            hora = datetime.strptime(hora, "%H:%M")
            return hora.strftime("%H:%M")
        except ValueError:
            mostrar_mensaje("Formato de hora inválido. Use HH:MM en formato 24 hrs (ej. 08:30)")
            return

def inter_horas(entrada, salida)-> tuple[str,str]:
    while True:
        if salida > entrada:
            return entrada, salida
        mostrar_mensaje("La hora de salida debe ser posterior a la hora de entrada")
        entrada = valida_hora(pedir("hora de entrada"))
        salida = valida_hora(pedir("hora de salida"))

def obtener_validador_depa(departamentos: list) -> TypeAdapter:
    max_id = max(d.id_departamento for d in departamentos)
    regla_op_depa = Annotated[int, Field(ge=1, le=max_id)]
    validador_depa = TypeAdapter(regla_op_depa)
    return validador_depa

@staticmethod
def mostrar_mensaje(mensaje: str) -> None:
    print(f"\n[SISTEMA] {mensaje}")

@staticmethod
def convertir(valor: str | date) -> date:
        if isinstance(valor, datetime):
            return valor.date()

        if isinstance(valor, date):
            return valor

        valor = valor.strip()

        for formato in ("%d-%m-%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(valor, formato).date()
            except ValueError:
                continue

        raise ValueError(
            "Usa el formato DD-MM-YYYY."
        )