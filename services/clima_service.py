#verificar con Postman los url API
import logging
import re
import unicodedata
import math

from typing import Tuple, Dict, Any

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    REQUESTS_AVAILABLE = True

except ImportError:
    requests = None
    HTTPAdapter = None
    Retry = None

    REQUESTS_AVAILABLE = False

from config.settings import Settings

logger = logging.getLogger(__name__)

class ClimaService:
    """
    Servicio encargado de consumir la API externa de Clima (WeatherAPI).
    Implementa buenas prácticas de seguridad, sanitización y tolerancia a fallos.
    """
    _session = None

    @classmethod
    def _get_session(cls):
        """
        Crea y reutiliza una sesión HTTP para consumir WeatherAPI.

        Configura:
        - Cabeceras HTTP.
        - Reintentos automáticos ante errores temporales.
        - Adaptador HTTP.
        """

        if not REQUESTS_AVAILABLE:
            raise RuntimeError(
                "La librería requests no está instalada."
            )

        # Reutilizamos la sesión si ya fue creada.
        if cls._session is None:

            session = requests.Session()

            # Cabeceras de las peticiones.
            session.headers.update({
                "Accept": "application/json",
                "User-Agent": "EcoTechSolutions/1.0"
            })

            # Configuración de reintentos.
            reintentos = Retry(
                total=2,
                connect=2,
                read=2,
                status=2,
                backoff_factor=0.5,
                status_forcelist=(429, 500, 502, 503, 504),
                allowed_methods=frozenset(["GET"]),
                respect_retry_after_header=True,
                raise_on_status=False
            )

            # Adaptador que administra los reintentos.
            adaptador = HTTPAdapter(
                max_retries=reintentos
            )

            session.mount("https://", adaptador)

            cls._session = session

        return cls._session


    # Datos de contingencia por si falla la red en el laboratorio
    CLIMA_CONTINGENCIA = {
        "chillan": {
            "ciudad": "Chillán", "temperatura": 18.5, "sensacion_termica": 17.0,
            "condicion": "Parcialmente nublado", "humedad": 65, "viento_kph": 12.0
        },
        
    }

    @staticmethod
    def _procesar_json(response : Any) -> dict:
        """
        Comprueba que la respuesta sea un JSON válido
        y que su estructura principal sea un diccionario.
        """
        try:
            data = response.json()

        except ValueError as error:
            logger.error("WeatherAPI devolvió JSON inválido.")
            raise ValueError(
                "El servicio de clima devolvió una respuesta inválida."
            ) from error

        if not isinstance(data, dict):
            raise ValueError(
                "La estructura de respuesta de WeatherAPI no es válida."
            )

        return data


    @staticmethod
    def _validar_seccion(data: dict, nombre: str) -> dict:
        """
        Comprueba que una sección del JSON exista
        y tenga la estructura de un diccionario.
        """
        seccion = data.get(nombre)

        if not isinstance(seccion, dict):
            raise ValueError(
                f"La sección '{nombre}' de WeatherAPI no es válida."
            )

        return seccion

    
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

    @staticmethod
    def sanitizar_dias(dias: Any) -> int:
        """
        Valida y normaliza la cantidad de días del pronóstico.
        Acepta enteros o textos numéricos entre 1 y 3.
        """

        if isinstance(dias, bool):
            raise ValueError(
                "La cantidad de días debe ser un número entero entre 1 y 3."
            )

        if isinstance(dias, str):
            dias = dias.strip()

            if not re.fullmatch(r"[1-3]", dias):
                raise ValueError(
                    "Ingrese una cantidad de días válida entre 1 y 3."
                )

            dias = int(dias)

        elif not isinstance(dias, int):
            raise ValueError(
                "La cantidad de días debe ser un número entero entre 1 y 3."
            )

        if not 1 <= dias <= 3:
            raise ValueError(
                "La cantidad de días debe estar entre 1 y 3."
            )

        return dias

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

        if not Settings.API_KEY_CLIMA:
            logger.error("No se encuentra configurada la API Key de WeatherAPI.")

            return (
                "La API Key del servicio de clima no está configurada.",
                None,
                None
            )
        url = f"{Settings.API_BASE_URL_CLIMA}/current.json"
        params = {
            "key": Settings.API_KEY_CLIMA,
            "q": ciudad_segura,
            "lang": "es"
        }

        try:
            session = cls._get_session()
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
                logger.warning(
                    "Límite de peticiones excedido en WeatherAPI (HTTP 429)."
                )

                res_local, msg_local = cls._manejar_contingencia(
                    ciudad_segura,
                    "Se alcanzó el límite de consultas de WeatherAPI."
                )

                analisis_local = (
                    cls.evaluar_viabilidad_operativa(res_local)
                    if res_local else None
                )

                return (msg_local, res_local, analisis_local)
            elif 500 <= response.status_code < 600:
                logger.error("Servidor de WeatherAPI con error interno (HTTP %s).", response.status_code)
                res_local, msg_local = cls._manejar_contingencia(
                    ciudad_segura,
                    f"El servidor externo de clima no está disponible (HTTP {response.status_code})."
                )
                analisis_local = cls.evaluar_viabilidad_operativa(res_local) if res_local else None
                return (msg_local, res_local, analisis_local)
            
            response.raise_for_status()
            
            data = cls._procesar_json(response)
            location = cls._validar_seccion(data,"location")
            current = cls._validar_seccion(data,"current")
            condition = cls._validar_seccion(current,"condition")

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

        except requests.exceptions.Timeout:
            logger.exception("Timeout al consultar clima actual.")

            res_local, msg_local = cls._manejar_contingencia(
                ciudad_segura,
                "Tiempo de espera agotado."
            )

            analisis = (
                cls.evaluar_viabilidad_operativa(res_local)
                if res_local else None
            )

            return (msg_local, res_local, analisis)

        except requests.exceptions.ConnectionError:
            logger.exception("Error de conexión con WeatherAPI.")

            res_local, msg_local = cls._manejar_contingencia(
                ciudad_segura,
                "No fue posible conectar con WeatherAPI."
            )

            analisis = (
                cls.evaluar_viabilidad_operativa(res_local)
                if res_local else None
            )

            return (msg_local, res_local, analisis)

        except requests.exceptions.RequestException:
            logger.exception("Error HTTP al consultar clima actual.")

            res_local, msg_local = cls._manejar_contingencia(
                ciudad_segura,
                "Error de comunicación con WeatherAPI."
            )

            analisis = (
                cls.evaluar_viabilidad_operativa(res_local)
                if res_local else None
            )

            return (msg_local, res_local, analisis)

        except ValueError:
            logger.exception("Error al procesar respuesta de clima.")

            return (
                "El servicio de clima devolvió información inválida.",
                None,
                None
            )
            

    @classmethod
    def _manejar_contingencia(
        cls,
        ciudad: str,
        causa_error: str
    ) -> Tuple[Dict[str, Any] | None, str]:

        """
        Utiliza datos locales únicamente cuando corresponden
        a la ciudad solicitada.
        """

        if not Settings.ENABLE_OFFLINE_FALLBACK:
            return (
                None,
                f"{causa_error} (El modo offline está deshabilitado)."
            )

        
        ciudad_key = unicodedata.normalize(
            "NFD",
            ciudad.strip().casefold()
        )

        ciudad_key = "".join(
            caracter
            for caracter in ciudad_key
            if unicodedata.category(caracter) != "Mn"
        )


        datos_local = cls.CLIMA_CONTINGENCIA.get(ciudad_key)

        if datos_local is None:
            return (
                None,
                f"{causa_error} No existen datos locales de contingencia "
                f"para {ciudad}."
            )

        resultado = datos_local.copy()

        resultado["fuente"] = "CONTINGENCIA"
        resultado["es_referencial"] = True

        msg = (
            f"[MODO CONTINGENCIA CLIMA] {causa_error}\n"
            f"Se utilizaron datos locales referenciales para "
            f"{resultado['ciudad']}."
        )

        return (resultado, msg)


    @staticmethod
    def _numero_seguro(
        valor: Any,
        minimo: float,
        maximo: float
    ) -> float | None:
        """
        Convierte un valor a número y comprueba que sea finito
        y esté dentro de un rango permitido.

        Retorna None si el dato no es válido.
        """

        if isinstance(valor, bool) or valor is None:
            return None

        try:
            numero = float(valor)

        except (TypeError, ValueError):
            return None

        if not math.isfinite(numero):
            return None

        if not minimo <= numero <= maximo:
            return None

        return numero

    @classmethod
    def probar_conectividad(cls) -> Tuple[bool, str]:
        """
        Comprueba la disponibilidad de WeatherAPI y la validez de la API Key.
        Retorna: (estado_conexion, mensaje).
        """

        # 1. Comprobar que requests esté disponible.
        if not REQUESTS_AVAILABLE:
            return (
                False,
                "Librería 'requests' no instalada. Ejecute 'pip install requests'."
            )

        # 2. Comprobar que exista una API Key.
        api_key = Settings.API_KEY_CLIMA

        if not isinstance(api_key, str) or not api_key.strip():
            logger.error("API Key de WeatherAPI no configurada.")

            return (
                False,
                "La API Key del servicio de clima no está configurada."
            )

        # 3. Preparar la petición.
        url = f"{Settings.API_BASE_URL_CLIMA}/current.json"

        params = {
            "key": api_key.strip(),
            "q": "Chillan",
            "lang": "es"
        }

        try:
            session = cls._get_session()

            response = session.get(
                url,
                params=params,
                timeout=Settings.REQUEST_TIMEOUT
            )

            # 4. Interpretar la respuesta HTTP.
            if response.status_code == 200:
                return (
                    True,
                    "Conexión exitosa con WeatherAPI. API Key válida."
                )

            elif response.status_code in (401, 403):
                logger.error(
                    "Error de autenticación WeatherAPI: HTTP %s",
                    response.status_code
                )

                return (
                    False,
                    "La API Key es inválida o no está autorizada."
                )

            elif response.status_code == 400:
                logger.warning(
                    "WeatherAPI rechazó los parámetros de conectividad."
                )

                return (
                    False,
                    "WeatherAPI respondió, pero rechazó los parámetros enviados."
                )

            elif response.status_code == 429:
                logger.warning(
                    "WeatherAPI alcanzó el límite de consultas."
                )

                return (
                    False,
                    "WeatherAPI está accesible, pero se alcanzó el límite de consultas."
                )

            elif 500 <= response.status_code < 600:
                logger.error(
                    "Error interno de WeatherAPI: HTTP %s",
                    response.status_code
                )

                return (
                    False,
                    "WeatherAPI está temporalmente fuera de servicio."
                )

            return (
                False,
                f"WeatherAPI respondió con código HTTP {response.status_code}."
            )

        except requests.exceptions.Timeout:
            logger.warning("Tiempo de espera agotado al probar WeatherAPI.")

            return (
                False,
                "Tiempo de espera agotado al contactar WeatherAPI."
            )

        except requests.exceptions.ConnectionError:
            logger.warning("No fue posible establecer conexión con WeatherAPI.")

            return (
                False,
                "No fue posible conectar con el servidor de WeatherAPI."
            )

        except requests.exceptions.RequestException:
            logger.exception(
                "Error de comunicación al probar conectividad con WeatherAPI."
            )

            return (
                False,
                "Ocurrió un problema de comunicación con el servicio externo."
            )
    
    
    
    @classmethod
    def evaluar_viabilidad_operativa(cls, datos_clima: Dict[str, Any]) -> Dict[str, str]:
        """
        Evalúa las condiciones climáticas para determinar
        la viabilidad de realizar actividades operativas.
        """

        if not isinstance(datos_clima, dict):
            return {
                "estado": "SIN DATOS",
                "recomendacion": "No fue posible evaluar la información climática."
            }

        # Validación y normalización de datos numéricos.
        temp = cls._numero_seguro(
            datos_clima.get("temperatura"), -100, 70
        )
        humedad = cls._numero_seguro(
            datos_clima.get("humedad"), 0, 100
        )
        viento = cls._numero_seguro(
            datos_clima.get("viento_kph"), 0, 400
        )
        prob_lluvia = cls._numero_seguro(
            datos_clima.get("prob_lluvia"), 0, 100
        )

        condicion = datos_clima.get("condicion")
        condicion = (
            condicion.strip().casefold()
            if isinstance(condicion, str)
            else ""
        )

        # No evaluar si no existe ningún dato útil.
        if all(
            valor is None
            for valor in (temp, humedad, viento, prob_lluvia)
        ) and not condicion:
            return {
                "estado": "SIN DATOS",
                "recomendacion": "No hay información climática válida para evaluar.",
                "alertas":[]
            }

        alertas = []

        # Evaluación de condiciones climáticas.
        if "lluvia" in condicion or "tormenta" in condicion:
            alertas.append("Se detectan condiciones de lluvia.")

        if prob_lluvia is not None and prob_lluvia >= 60:
            alertas.append("Alta probabilidad de lluvia.")

        if humedad is not None and humedad > 85:
            alertas.append("Humedad ambiental elevada.")

        if temp is not None:
            if temp < 5:
                alertas.append("Temperatura demasiado baja.")
            elif temp > 32:
                alertas.append("Temperatura elevada.")

        if viento is not None and viento > 35:
            alertas.append("Vientos fuertes.")

        # Clasificación final.
        if not alertas:
            estado = "ÓPTIMO"
            recomendacion = (
                "Las condiciones disponibles son favorables. "
                "Verifique las variables climáticas que no fueron informadas."
            )
        elif len(alertas) == 1:
            estado = "PRECAUCIÓN"
            recomendacion = " ".join(alertas)
        else:
            estado = "RIESGO ALTO"
            recomendacion = " ".join(alertas)

        return {
            "estado": estado,
            "recomendacion": recomendacion,
            "alertas": alertas
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
            dias_seguros = cls.sanitizar_dias(dias)

        except ValueError as e:
            return (str(e), None, None)

        if not REQUESTS_AVAILABLE:
            return ("Librería 'requests' no instalada.", None, None)

        if not Settings.API_KEY_CLIMA:
            logger.error("No se encuentra configurada la API Key de WeatherAPI.")

            return (
                "La API Key del servicio de clima no está configurada.",
                None,
                None
            )

        url = f"{Settings.API_BASE_URL_CLIMA}/forecast.json"
        params = {
            "key": Settings.API_KEY_CLIMA,
            "q": ciudad_segura,
            "days": dias_seguros, 
            "lang": "es",
        }

        try:
            session = cls._get_session()
            response = session.get(
                url, params=params, timeout=Settings.REQUEST_TIMEOUT
            )

            if response.status_code == 400:
                return (
                    f"Ciudad '{ciudad_segura}' no encontrada.",
                    None,
                    None
                )

            elif response.status_code in (401, 403):
                logger.error(
                    "Error de autenticación WeatherAPI: HTTP %s",
                    response.status_code
                )

                return (
                    "API Key inválida o no autorizada.",
                    None,
                    None
                )

            elif response.status_code == 429:
                logger.warning("Límite de consultas de WeatherAPI excedido.")

                return (
                    "Límite de consultas excedido. Intente más tarde.",
                    None,
                    None
                )

            elif 500 <= response.status_code < 600:
                logger.error(
                    "Error del servidor WeatherAPI: HTTP %s",
                    response.status_code
                )

                return (
                    "El servicio de pronóstico no está disponible.",
                    None,
                    None
                )

            response.raise_for_status()
            data = cls._procesar_json(response)

            location = cls._validar_seccion(data, "location")
            forecast = cls._validar_seccion(data, "forecast")

            forecast_days = forecast.get("forecastday")

            if not isinstance(forecast_days, list) or not forecast_days:
                raise ValueError(
                    "WeatherAPI no devolvió una lista válida de días de pronóstico."
                )

            resultado_pronostico = {
                "ciudad": location.get("name", ciudad_segura),
                "pais": location.get("country", ""),
                "dias": [],
            }

            evaluaciones_pronostico = []

            for dia in forecast_days:
                if not isinstance(dia, dict):
                    raise ValueError("Un registro del pronóstico no tiene una estructura válida.")

                day_info = cls._validar_seccion(dia, "day")
                condition = cls._validar_seccion(day_info, "condition")

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
                    "viento_kph": datos_dia_crudo["viento_max_kph"],
                    "condicion": datos_dia_crudo["condicion"],
                    "prob_lluvia": datos_dia_crudo["prob_lluvia"]
                }
                analisis_dia = cls.evaluar_viabilidad_operativa(datos_para_evaluar)
                evaluaciones_pronostico.append(analisis_dia)

            msg = f"Pronóstico obtenido con éxito para {resultado_pronostico['ciudad']}."
            # Retorna en orden estricto: (mensaje, datos_pronostico, evaluaciones)
            return (msg, resultado_pronostico, evaluaciones_pronostico)

        except requests.exceptions.Timeout:
            logger.exception("Timeout al consultar pronóstico.")

            return (
                "Tiempo de espera agotado al consultar el pronóstico.",
                None,
                None
            )

        except requests.exceptions.ConnectionError:
            logger.exception("Error de conexión al consultar pronóstico.")

            return (
                "No fue posible conectar con WeatherAPI.",
                None,
                None
            )

        except requests.exceptions.RequestException:
            logger.exception("Error HTTP al consultar pronóstico.")

            return (
                "Error de comunicación con el servicio de pronóstico.",
                None,
                None
            )

        except ValueError:
            logger.exception("Error al procesar JSON del pronóstico.")

            return (
                "El servicio devolvió información inválida.",
                None,
                None
            )