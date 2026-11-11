import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / ".env" #archivo local conectado directo a .env
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

class Settings:
    """
    Centraliza las variables de configuración del sistema.
    Evita exponer credenciales hardcodeadas en el código fuente.
    """
    API_BASE_URL_CLIMA: str = os.getenv("API_BASE_URL_CLIMA", "http://api.weatherapi.com/v1/current.json")#(lo que trae, valor por defecto)
    API_KEY_CLIMA: str = os.getenv("API_KEY_CLIMA", "")#(variable,valor por defecto)
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "5")) 
    ENABLE_OFFLINE_FALLBACK: bool = (os.getenv("ENABLE_OFFLINE_FALLBACK", "True").lower() in ("true", "1", "yes"))

    #login del sistema [usuario administrador]
    ADMIN_INITIAL_USER: str = os.getenv("ADMIN_INITIAL_USER","admin")
    ADMIN_INITIAL_CLAVE: str = os.getenv("ADMIN_INITIAL_CLAVE","admin1234")
    MAX_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_LOGIN_ATTEMPTS","3"))