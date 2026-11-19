from config.database import Database
from controllers.main_controller import MainController
from config.settings import Settings

def main() -> None:
    # 1. Inicializar la base de datos (crear tablas si no existen)
    print("Inicializando sistema...")
    faltantes = Settings.validar()
    if faltantes:
        print(f"Falta configurar en .env: {', '.join(faltantes)}")
        print("El módulo de clima no estará disponible hasta corregirlo.")
        # Si quisieras detener el programa: return
    db = Database()
    db.init_db()
    
    # 2. Iniciar el controlador principal que maneja el flujo de la aplicación
    app = MainController()
    app.ejecutar()

if __name__ == "__main__":
    main()