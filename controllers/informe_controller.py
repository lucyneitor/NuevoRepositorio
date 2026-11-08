from views.informe_view import InformeView
from views.utils import pedir, validador_op, eleccion, ValidationError
class InformeController:
    def __init__(self):
        self.informe_view = InformeView()

    def ejecutar(self):
        while True:
            self.informe_view.sub_menu()
            op = pedir("opción")
            try:
                op = int(op)
                eleccion(validador_op, op)
            except (TypeError, ValueError, ValidationError) as e:
                print(e)
                continue
            else:
                if op == 0:
                    print("Volver a la gestion de sistema")
                    return
                
