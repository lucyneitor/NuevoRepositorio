#verificar con Postman los url API
import re
from typing import Tuple, Dict, Any

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    requests = None
    REQUESTS_AVAILABLE = False

from config.settings import Settings

class ClimaService:
    """
    Servicio encargado de consumir la API externa de Clima (WeatherAPI).
    Implementa buenas prácticas de seguridad, sanitización y tolerancia a fallos.
    """

    # Datos de contingencia por si falla la red en el laboratorio
    CLIMA_CONTINGENCIA = {
        "chillan": {
            "ciudad": "Chillán",
            "temperatura": 18.5,
            "sensacion_termica": 17.0,
            "condicion": "Parcialmente nublado",
            "humedad": 65,
            "viento_kph": 12.0
        }
    }

    @staticmethod
    def sanitizar_ciudad(ciudad: str) -> str:
        """Valida que el nombre de la ciudad no contenga caracteres maliciosos."""
        if not ciudad or not isinstance(ciudad, str):
            raise ValueError("El nombre de la ciudad debe ser un texto válido.")
        
        limpio = ciudad.strip()
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", limpio):
            raise ValueError("El nombre de la ciudad contiene caracteres no permitidos.")
        
        if len(limpio) < 2:
            raise ValueError("Ingrese al menos 2 caracteres para la ciudad.")
            
        return limpio

    @classmethod
    def obtener_clima_actual(cls, ciudad: str = "Chillan") -> Tuple[Dict[str, Any] | None, str]:
        """Consulta la API externa de clima con la ciudad solicitada."""
        try:
            ciudad_segura = cls.sanitizar_ciudad(ciudad)
        except ValueError as e:
            return (None, str(e))

        if not REQUESTS_AVAILABLE:
            return cls._manejar_contingencia(
                ciudad_segura, 
                "Librería 'requests' no instalada en el entorno."
            )

        # Parámetros obligatorios que exige WeatherAPI (key y q)
        params = {
            "key": Settings.API_KEY_CLIMA,
            "q": ciudad_segura
        }

        try:
            # Petición HTTP usando la URL base y el timeout centralizado en Settings
            response = requests.get(
                Settings.API_BASE_URL_CLIMA,
                params=params,
                timeout=Settings.REQUEST_TIMEOUT
            )

            # Manejo de códigos HTTP comunes de WeatherAPI
            if response.status_code == 400:
                return (None, f"Ciudad '{ciudad_segura}' no encontrada o parámetro inválido.")
            elif response.status_code == 401:
                return (None, "Error 401: API Key de Clima inválida o no autorizada.")
            elif response.status_code == 429:
                return (None, "Error 429: Límite de consultas a WeatherAPI excedido.")
            
            response.raise_for_status()

            # Deserialización del JSON devuelto por WeatherAPI
            data = response.json()
            location = data.get("location", {})
            current = data.get("current", {})
            condition = current.get("condition", {})

            resultado_clima = {
                "ciudad": location.get("name", ciudad_segura),
                "pais": location.get("country", ""),
                "temperatura": current.get("temp_c", 0.0),
                "sensacion_termica": current.get("feelslike_c", 0.0),
                "condicion": condition.get("text", "Desconocido"),
                "humedad": current.get("humidity", 0),
                "viento_kph": current.get("wind_kph", 0.0)
            }

            return (resultado_clima, f"Clima obtenido exitosamente para {resultado_clima['ciudad']}.")

        except requests.exceptions.Timeout:
            return cls._manejar_contingencia(
                ciudad_segura, 
                f"El servicio de clima tardó más de {Settings.REQUEST_TIMEOUT}s en responder (Timeout)."
            )
        except requests.exceptions.ConnectionError:
            return cls._manejar_contingencia(
                ciudad_segura, 
                "No hay conexión a internet o el servidor de WeatherAPI está caído."
            )
        except requests.exceptions.RequestException as e:
            return cls._manejar_contingencia(ciudad_segura, f"Falla en la petición: {str(e)}")

    @classmethod
    def _manejar_contingencia(cls, ciudad: str, causa_error: str) -> Tuple[Dict[str, Any] | None, str]:
        """Si la conexión falla, permite respaldar con datos locales si está habilitado."""
        if not Settings.ENABLE_OFFLINE_FALLBACK:
            return (None, f"{causa_error} (El modo offline está deshabilitado).")

        ciudad_key = ciudad.lower()
        datos_local = cls.CLIMA_CONTINGENCIA.get(ciudad_key, cls.CLIMA_CONTINGENCIA["chillan"])

        msg = (
            f"[MODO CONTINGENCIA CLIMA] {causa_error}\n"
            f"Se cargaron datos locales de emergencia para {datos_local['ciudad']}."
        )
        return (datos_local, msg)