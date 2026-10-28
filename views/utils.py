def leer_numero(mensaje: str) -> int:
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