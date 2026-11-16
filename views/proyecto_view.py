from views.main_view import MainView
from datetime import date, datetime
from views.utils import pedir
from models.proyecto import Proyecto
class ProyectoView():
    def sub_menu(self):
        print("Submenú de Gestión de Proyectos")
        print(">"*40)
        print("1. Agregar Proyecto")
        print("2. Modificar Proyecto")
        print("3. Buscar Proyecto")
        print("4. Eliminar Proyecto")
        print("5. Mostrar proyectos")
        print("6. Planificar proyecto")
        print("0. Volver al menú principal")
        print(">"*40)

    def menu_modificar(self):
        print("-" * 45)
        print("Opciones de edición")
        print("-" * 45)
        print("1. Nombre")
        print("2. Descripción")
        print("3. Fecha de inicio") #sujeto a editar automatico estado y obligar declarar fecha termino
        print("4. Fecha de término") #validar que no sea antes de la fecha_inicio
        print("0. Volver")
        print("-" * 45)
        
    def formulario(self) -> dict:
        print(">"*50)
        print("FICHA DE PROYECTO")
        print(">"*50)
        nombre = pedir("Nombre del proyecto").strip()
        descripcion = pedir("Descripción").strip()

        while True:
            try:
                fecha_inicio_texto = pedir("Fecha de inicio (DD-MM-AAAA)").strip()
                fecha_inicio = datetime.strptime(
                    fecha_inicio_texto,
                    "%d-%m-%Y"
                ).date()

                fecha_fin_texto = pedir("Fecha de término (DD-MM-AAAA)").strip()
                fecha_fin = datetime.strptime(
                    fecha_fin_texto,
                    "%d-%m-%Y"
                ).date()

                if fecha_fin < fecha_inicio:
                    print("La fecha de término no puede ser anterior a la fecha de inicio.")
                    continue

                break
            except ValueError:
                print("Ingresa las fechas con el formato DD-MM-AAAA.")

        hoy = date.today()

        if hoy < fecha_inicio:
            estado = "Pendiente"
        elif hoy > fecha_fin:
            estado = "Finalizado"
        else:
            estado = "En proceso"

        return {
            "nombre": nombre,
            "descripcion": descripcion,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat(),
            "estado": estado,
        }

    def mostrar_proyecto(self, proyecto:Proyecto):
        print("\n--- Datos del proyecto ---")
        print(f"ID: {proyecto.id_proyecto}")
        print(f"Nombre: {proyecto.nombre}")
        print(f"Descripción: {proyecto.descripcion}")
        print(f"Fecha de inicio: {proyecto.fecha_inicio}")
        print(f"Fecha de término: {proyecto.fecha_fin}")
        print(f"Estado: {proyecto.estado}")
        print("--------------------------\n")

    def menu_mostrar(self):
        print("\n¿Qué datos quieres mostrar?")
        print("1. Todos los detalles")
        print("2. Solo datos especificos")
        print("0. Volver")


    def menu_op2(self):
        print("\n¿Qué datos quieres mostrar?")
        print("1. Nombre")
        print("2. Descripción")
        print("3. Fecha de inicio")
        print("4. Fecha de término")
        print("5. Estado")
        print("6. Listo los seleccionados")
        print("0. Volver")

    def mostrar_detalle(self, opciones: list[str], proyectos: list[Proyecto]):
        campos_disponibles = {
            "id": ("ID Proyecto", "id_proyecto"),
            "nombre": ("Nombre", "nombre"),
            "descripción": ("Descripción", "descripcion"),
            "fecha inicio": ("Inicio", "fecha_inicio"),
            "fecha fin": ("Término", "fecha_fin"),
            "estado": ("Estado", "estado"),
        }

        campos = [
            campos_disponibles[opcion]
            for opcion in opciones
            if opcion in campos_disponibles
        ]

        encabezados = [titulo for titulo, _ in campos]

        filas = [
            [
                str(getattr(proyecto, atributo))
                for _, atributo in campos
            ]
            for proyecto in proyectos
        ]

        anchos = [
            max(
                len(encabezados[indice]),
                *(len(fila[indice]) for fila in filas)
            )
            for indice in range(len(encabezados))
        ]

        borde = "+" + "+".join(
            "-" * (ancho + 2)
            for ancho in anchos
        ) + "+"

        def imprimir_fila(valores):
            print(
                "|"
                + "|".join(
                    f" {valor:<{anchos[indice]}} "
                    for indice, valor in enumerate(valores)
                )
                + "|"
            )

        print(borde)
        imprimir_fila(encabezados)
        print(borde)

        for fila in filas:
            imprimir_fila(fila)

        print(borde)

    def menu_planificacion(self):
        print("="*60)
        print("   MÓDULO DE GESTIÓN Y PLANIFICACIÓN CLIMÁTICA")
        print("="*60)
        print("1. Evaluar Clima Actual y Viabilidad Operativa (Hoy)")
        print("2. Consultar Pronóstico a Futuro (Anticipación de Retrasos)")
        print("3. Probar Conectividad con la API externa")
        print("0. Volver al Menú Principal")
        print("="*60)
            
    def resultado_clima(msg, datos_clima, analisis): # crear una funcion en proyecto_controller de clima para mostrar estos resultados
        print(f"\n✅ {msg}")
        print("----------------------------------------------------")
        print(f"🌍 Ubicación:         {datos_clima['ciudad']}, {datos_clima['pais']}")
        print(f"🌡️  Temperatura:       {datos_clima['temperatura']}°C")
        print(f"🤔 Sensación térmica: {datos_clima['sensacion_termica']}°C")
        print(f"☁️  Estado del tiempo: {datos_clima['condicion']}")
        print(f"💧 Humedad:           {datos_clima['humedad']}%")
        print(f"💨 Viento:            {datos_clima['viento_kph']} km/h")
        print("----------------------------------------------------")
        print(f"📊 ESTADO OPERATIVO:  [{analisis['estado_operativo']}]")
        print(f"💡 DECISIÓN SUGERIDA: {analisis['recomendacion']}")
        if analisis["alertas"]:
            print("\n⚠️  ALERTAS DE RIESGO DETECTADAS:")
            for alerta in analisis["alertas"]:
                print(f"   • {alerta}")
            print("====================================================\n")
