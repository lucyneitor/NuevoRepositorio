#verificar con Postman los url API
import logging
import re
from typing import Tuple, Dict, Any


try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    requests = None
    REQUESTS_AVAILABLE = False

from config.settings import Settings

logger = logging.getLogger(__name__)

class ClimaService:
    """
    Servicio encargado de consumir la API externa de Clima (WeatherAPI).
    Implementa buenas prácticas de seguridad, sanitización y tolerancia a fallos.
    """
    _session = None
    # Datos de contingencia por si falla la red en el laboratorio
    CLIMA_CONTINGENCIA = {
        "chillan": {
            "ciudad": "Chillán", "temperatura": 18.5, "sensacion_termica": 17.0,
            "condicion": "Parcialmente nublado", "humedad": 65, "viento_kph": 12.0
        },
        
    }
    @classmethod
    def _get_seccion(cls):
        """
        Inicializa y reutiliza una sesión HTTP con encabezados estándar
        """
        if cls._session is None and REQUESTS_AVAILABLE:
            cls._session = requests.Session()
            cls._session.headers.update({"Accept": "application/json"})
        return cls._session
    
    @staticmethod
    def sanitizar_ciudad(ciudad: str) -> str:
        """
        Valida que el nombre de la ciudad no contenga caracteres maliciosos.
        """
        if not ciudad or not isinstance(ciudad, str):
            raise ValueError("El nombre de la ciudad debe ser un texto válido.")

        limpio = ciudad.strip()

        if len(limpio) < 2:
                    raise ValueError("Ingrese al menos 2 caracteres para la ciudad.")
        if not re.fullmatch(r"[^\W\d_]+(?:[ '\-][^\W\d_]+)*", limpio, re.UNICODE):
            raise ValueError("El nombre de la ciudad contiene caracteres no permitidos.")
            
        return limpio

    @classmethod
    def obtener_clima_actual(cls, ciudad: str) -> Tuple[str, Dict[str, Any] | None, Dict[str, Any] | None]:
        """
        Consulta la API externa de clima y evalúa la viabilidad operativa automáticamente.
        Retorna: (msg, resultado_clima, analisis_operativo)
        """
        try:
            ciudad_segura = cls.sanitizar_ciudad(ciudad)
        except ValueError as e:
            return (str(e), None, None)

        if not REQUESTS_AVAILABLE:
            res_local, msg_local = cls._manejar_contingencia(
                ciudad_segura, 
                "Librería 'requests' no instalada en el entorno."
            )
            analisis_local = cls.evaluar_viabilidad_operativa(res_local) if res_local else None
            return (msg_local, res_local, analisis_local)

        url = f"{Settings.API_BASE_URL_CLIMA}/current.json"
        params = {
            "key": Settings.API_KEY_CLIMA,
            "q": ciudad_segura,
            "lang": "es"
        }

        try:
            session = cls._get_seccion()
            response = session.get(
                url,
                params=params,
                timeout=Settings.REQUEST_TIMEOUT
            )

            if response.status_code == 400:
                return (f"Ciudad '{ciudad_segura}' no encontrada o parámetro inválido.", None, None)
            elif response.status_code in (401, 403):
                logger.error("Fallo de autenticación con WeatherAPI (HTTP %s).", response.status_code)
                return ("Error 401: API Key de Clima inválida o no autorizada. Verificar configuración", None, None)
            elif response.status_code == 429:
                logger.warning("Límite de peticiones excedido en WeatherAPI (HTTP 429).")
                return ("Error 429: Límite de consultas a WeatherAPI excedido. Intente más tarde.", None, None)
            elif 500 <= response.status_code < 600:
                logger.error("Servidor de WeatherAPI con error interno (HTTP %s).", response.status_code)
                res_local, msg_local = cls._manejar_contingencia(
                    ciudad_segura,
                    f"El servidor externo de clima no está disponible (HTTP {response.status_code})."
                )
                analisis_local = cls.evaluar_viabilidad_operativa(res_local) if res_local else None
                return (msg_local, res_local, analisis_local)
            
            response.raise_for_status()
            
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

            # 🛠️ Evaluamos la viabilidad operativa de inmediato con los datos obtenidos
            analisis = cls.evaluar_viabilidad_operativa(resultado_clima)

            msg = f"Clima obtenido exitosamente para {resultado_clima['ciudad']}."
            return (msg, resultado_clima, analisis)

        except requests.exceptions.RequestException:
            logger.exception("Error de red en ClimaService al obtener clima actual")
            res_local, msg_local = cls._manejar_contingencia(
                ciudad_segura, 
                "Falla en la petición: Ocurrió un problema de comunicación con el servicio de clima."
            )
            analisis_local = cls.evaluar_viabilidad_operativa(res_local) if res_local else None
            return (msg_local, res_local, analisis_local)

    @classmethod
    def _manejar_contingencia(cls, ciudad: str, causa_error: str) -> Tuple[Dict[str, Any] | None, str]:
        """
        Si la conexión falla, permite respaldar con datos locales si está habilitado.
        """
        if not Settings.ENABLE_OFFLINE_FALLBACK:
            return (None, f"{causa_error} (El modo offline está deshabilitado).")

        ciudad_key = ciudad.lower()
        datos_local = cls.CLIMA_CONTINGENCIA.get(ciudad_key, cls.CLIMA_CONTINGENCIA["chillan"])

        msg = (
            f"[MODO CONTINGENCIA CLIMA] {causa_error}\n"
            f"Se cargaron datos locales de emergencia para {datos_local['ciudad']}."
        )
        return (datos_local, msg)

    @classmethod
    def probar_conectividad(cls) -> Tuple[bool, str]:
        """
        Verifica si la API externa de clima está accesible y la key es válida.
        """
        if not REQUESTS_AVAILABLE:
            return (
                False,
                "Librería 'requests' no instalada. Ejecute 'pip install requests'.",
            )

        try:
            # WeatherAPI exige la 'key' y una ubicación 'q' obligatorias
            session = cls._get_seccion()
            url=f"{Settings.API_BASE_URL_CLIMA}/current.json"
            params = {
                "key": Settings.API_KEY_CLIMA, 
                "q": "Chillan"
            }

            resp = session.get(
                url,
                params=params,
                timeout=Settings.REQUEST_TIMEOUT,
            )

            # Si responde 200 (OK), la conexión y la API Key son correctas
            if resp.status_code == 200:
                return (
                    True,
                    f"Conexión exitosa con WeatherAPI (Código HTTP: {resp.status_code})",
                )
            elif resp.status_code in (401,403):
                return (
                    False,
                    f"Error de autentificación: La API Key de Clima es inválida o no está autorizada.",
                )

            return (
                False,
                f"El servidor respondió con código HTTP: {resp.status_code}",
            )

        except requests.exceptions.Timeout:
            return (False, "Timeout al contactar el servicio de clima.")
        except requests.exceptions.ConnectionError:
            return (False, "Sin conexión de red hacia el servidor de WeatherAPI.")
        except requests.exceptions.RequestException as e:
            #detalle técnico y sensible se queda seguro en el archivo de registro (log)
            logger.error("Error de red al conectar con el servicio: %s", str(e))
            #Al usuario se le entrega un mensaje amigable que no revela datos internos
            return (False, "Ocurrió un problema de comunicación con el servicio externo. Intente más tarde.")
    
    @staticmethod
    def evaluar_viabilidad_operativa(
        datos_clima: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analiza las variables climáticas obtenidas y genera una recomendación
        para apoyar la planificación operativa de proyectos en terreno.
        """
        temp = datos_clima.get("temperatura", 0.0)
        humedad = datos_clima.get("humedad", 0)
        viento = datos_clima.get("viento_kph", 0.0)
        condicion = datos_clima.get("condicion", "").lower()

        alertas = []

        # 1. Evaluación de precipitaciones o tormentas (principal causa de retrasos)
        palabras_riesgo = [
            "lluvia",
            "llovizna",
            "tormenta",
            "nieve",
            "granizo",
            "aguacero",
            "rain",
            "storm",
        ]
        if any(palabra in condicion for palabra in palabras_riesgo):
            alertas.append(
                f"Precipitaciones detectadas ({datos_clima['condicion']}): riesgo"
                " de retraso en obras o instalaciones exteriores."
            )

        # 2. Evaluación de humedad crítica (afecta equipos electrónicos, sellados o paneles)
        if humedad > 85:
            alertas.append(
                f"Humedad elevada ({humedad}%): precaución con aislamiento"
                " eléctrico y secado de materiales."
            )

        # 3. Evaluación de temperaturas extremas
        if temp < 5.0:
            alertas.append(
                f"Baja temperatura ({temp}°C): riesgo de escarcha o bajo"
                " rendimiento de baterías/materiales."
            )
        elif temp > 32.0:
            alertas.append(
                f"Alta temperatura ({temp}°C): riesgo de estrés térmico para el"
                " personal en terreno."
            )

        # 4. Evaluación de viento fuerte (crítico para trabajos en altura o estructuras)
        if viento > 35.0:
            alertas.append(
                f"Viento fuerte ({viento} km/h): suspender trabajos en altura o"
                " montaje de estructuras."
            )

        # Definición del estado operativo para la toma de decisiones
        if not alertas:
            estado = "ÓPTIMO"
            recomendacion = (
                "Condiciones favorables. Ejecutar actividades planificadas con"
                " normalidad."
            )
        elif len(alertas) == 1:
            estado = "PRECAUCIÓN"
            recomendacion = (
                "Ejecutar con medidas de mitigación o priorizar tareas bajo techo."
            )
        else:
            estado = "RIESGO ALTO"
            recomendacion = (
                "Reprogramar actividades críticas en exterior para evitar retrasos"
                " o daños."
            )

        return {
            "estado_operativo": estado,
            "recomendacion": recomendacion,
            "alertas": alertas,
        }

    @classmethod
    def obtener_pronostico(
        cls, ciudad: str, dias: int = 3
    ) -> Tuple[str, Dict[str, Any] | None, list[Dict[str, Any]] | None]:
        """
        Consulta el pronóstico a futuro y evalúa la viabilidad operativa día por día.
        Retorna: (msg, resultado_pronostico, lista_de_evaluaciones)
        """
        try:
            ciudad_segura = cls.sanitizar_ciudad(ciudad)
        except ValueError as e:
            return (str(e), None, None)

        if not REQUESTS_AVAILABLE:
            return ("Librería 'requests' no instalada.", None, None)

        url = f"{Settings.API_BASE_URL_CLIMA}/forecast.json"
        params = {
            "key": Settings.API_KEY_CLIMA,
            "q": ciudad_segura,
            "days": dias, 
            "lang": "es",
        }

        try:
            session = cls._get_seccion()
            response = session.get(
                url, params=params, timeout=Settings.REQUEST_TIMEOUT
            )

            if response.status_code == 400:
                return (f"Ciudad '{ciudad_segura}' no encontrada.", None, None)
            elif response.status_code in (401, 403):
                return ("Error 401: API Key inválida o no autorizada.", None, None)

            response.raise_for_status()
            data = response.json()

            location = data.get("location", {})
            forecast_days = data.get("forecast", {}).get("forecastday", [])

            resultado_pronostico = {
                "ciudad": location.get("name", ciudad_segura),
                "pais": location.get("country", ""),
                "dias": [],
            }

            evaluaciones_pronostico = []

            for dia in forecast_days:
                day_info = dia.get("day", {})
                condition = day_info.get("condition", {})

                # 1. Agregamos los datos del día al diccionario de pronóstico
                datos_dia_crudo = {
                    "fecha": dia.get("date"),
                    "temp_max": day_info.get("maxtemp_c"),
                    "temp_min": day_info.get("mintemp_c"),
                    "condicion": condition.get("text"),
                    "prob_lluvia": day_info.get("daily_chance_of_rain", 0),
                    "viento_max_kph": day_info.get("maxwind_kph"),
                }
                resultado_pronostico["dias"].append(datos_dia_crudo)

                # 2. Evaluamos la viabilidad operativa para este día de forma automática
                datos_para_evaluar = {
                    "temperatura": datos_dia_crudo["temp_max"],
                    "humedad": 86 if datos_dia_crudo["prob_lluvia"] >= 60 else 65, # Inferencia preventiva ante lluvia
                    "viento_kph": datos_dia_crudo["viento_max_kph"],
                    "condicion": datos_dia_crudo["condicion"]
                }
                analisis_dia = cls.evaluar_viabilidad_operativa(datos_para_evaluar)
                evaluaciones_pronostico.append(analisis_dia)

            msg = f"Pronóstico obtenido con éxito para {resultado_pronostico['ciudad']}."
            # Retorna en orden estricto: (mensaje, datos_pronostico, evaluaciones)
            return (msg, resultado_pronostico, evaluaciones_pronostico)

        except requests.exceptions.RequestException:
            return ("Falla de red al consultar el pronóstico.", None, None)