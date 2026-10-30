def leer_numero(mensaje: str) -> int: #falta un leer texto, leer fecha
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")

def eleccion(validador,op):
        try:
            op = validador.validate_strings(op)
        except TypeError:
            print("Por favor, ingrese la opcion que corresponda")

def conversor(num):
    if num==1:
        return "activo"
    if num==2:
        return "inacativo"
    if num==3:
        return "vacaciones"
    if num==4:
        return "suspendido"