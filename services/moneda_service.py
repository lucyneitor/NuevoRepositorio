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

class MonedaService:
    """
    Servicio de EcoTech Solutions que integra dos APIs:
    1. REST Countries: Para detectar la moneda oficial a partir del país del proyecto.
    2. Frankfurter API: Para obtener el tipo de cambio actualizado desde CLP.
    """
    _session = None

    # Plan de contingencia local por si falla el internet o alguna de las APIs
    TASAS_CONTINGENCIA = {
        ("CLP", "PEN"): 0.00395,
        ("CLP", "USD"): 0.00105,
        ("CLP", "EUR"): 0.00098,
        ("CLP", "BRL"): 0.00610,
        ("CLP", "ARS"): 1.05000,
        ("CLP", "COP"): 4.45000,
        ("CLP", "MXN"): 0.02100,
    }

    @classmethod
    def _get_sesion(cls):
        """Inicializa y reutiliza una sesión HTTP con encabezados estándar."""
        if cls._session is None and REQUESTS_AVAILABLE:
            cls._session = requests.Session()
            cls._session.headers.update({"Accept": "application/json"})
        return cls._session

    @staticmethod
    def _sanitizar_texto(texto: str, campo: str) -> str:
        """Valida que los textos no estén vacíos."""
        if not texto or not isinstance(texto, str):
            raise ValueError(f"El campo '{campo}' es inválido o está vacío.")
        return texto.strip()

    @classmethod
    def obtener_moneda_por_pais(cls, nombre_pais: str) -> Tuple[str, str]:
        """
        Consulta la API de REST Countries para obtener el código ISO de la moneda 
        y el nombre oficial del país ingresado.
        """
        pais_limpio = cls._sanitizar_texto(nombre_pais, "país")
        
        # Endpoint público de REST Countries v3.1 (sin token obligatorio)
        url = f"https://restcountries.com/v3.1/name/{pais_limpio}"

        session = cls._get_sesion()
        response = session.get(url, timeout=Settings.REQUEST_TIMEOUT)

        if response.status_code == 404:
            raise ValueError(f"No se encontró el país '{nombre_pais}' en el registro internacional.")
        
        response.raise_for_status()
        paises_data = response.json()

        if not paises_data:
            raise ValueError(f"No hay datos disponibles para el país '{nombre_pais}'.")

        # Tomamos el primer resultado de la búsqueda
        info_pais = paises_data[0]
        nombre_oficial = info_pais.get("name", {}).get("common", nombre_pais)
        
        # Extraemos el diccionario de monedas (ej. {'PEN': {'name': 'Peruvian sol', 'symbol': 'S/.'}})
        monedas_dict = info_pais.get("currencies", {})
        if not monedas_dict:
            raise ValueError(f"El país '{nombre_oficial}' no reporta una moneda oficial válida.")

        # Tomamos la primera moneda disponible en la lista del país
        codigo_moneda = list(monedas_dict.keys())[0]

        return nombre_oficial, codigo_moneda

    @classmethod
    def calcular_pago_internacional(
        cls,
        monto_base_clp: float,
        pais_proyecto: str
    ) -> Tuple[str, Dict[str, Any] | None]:
        """
        Método principal:
        1. Usa la API 1 para detectar la moneda destino según el país del proyecto.
        2. Usa la API 2 (Frankfurter) para convertir el sueldo base en CLP a esa moneda.
        """
        try:
            if not isinstance(monto_base_clp, (int, float)) or monto_base_clp <= 0:
                raise ValueError("El monto base del sueldo debe ser mayor a cero.")

            if not REQUESTS_AVAILABLE:
                return ( "Librería 'requests' no instalada.", None )

            # PASO 1: Consultar la API de Países para obtener la moneda destino
            nombre_pais_oficial, moneda_destino = cls.obtener_moneda_por_pais(pais_proyecto)

        except ValueError as e:
            return (str(e), None)
        except requests.exceptions.RequestException:
            logger.warning("Falla de red al consultar REST Countries. Intentando contingencia local.")
            # Si falla la API de países, puedes recurrir a un respaldo o retornar error
            return (f"No se pudo conectar con el servicio de países para '{pais_proyecto}'.", None)

        # Si el proyecto se ejecuta en Chile (CLP), no requiere conversión externa
        if moneda_destino == "CLP":
            return (
                "Proyecto en Chile. Sin conversión requerida.",
                {
                    "monto_origen_clp": float(monto_base_clp),
                    "moneda_destino": "CLP",
                    "tasa_aplicada": 1.0,
                    "monto_final_ajustado": float(monto_base_clp),
                    "fecha_indicador": "N/A",
                    "fuente": "Local (Chile)"
                }
            )

        # PASO 2: Consultar la API de Divisas (Frankfurter) para el tipo de cambio CLP -> Moneda Destino
        url_divisas = f"{Settings.API_BASE_URL_MONEDA}/latest?base=CLP&symbols={moneda_destino}"

        try:
            session = cls._get_sesion()
            response = session.get(url_divisas, timeout=Settings.REQUEST_TIMEOUT)

            if response.status_code in (400, 404, 422):
                return cls._manejar_contingencia(float(monto_base_clp), "CLP", moneda_destino, f"Moneda '{moneda_destino}' no soportada en el conversor.")
            elif response.status_code == 429:
                return cls._manejar_contingencia(float(monto_base_clp), "CLP", moneda_destino, "Límite de peticiones excedido en API de divisas (HTTP 429).")
            elif 500 <= response.status_code < 600:
                return cls._manejar_contingencia(float(monto_base_clp), "CLP", moneda_destino, f"Servidor de divisas no disponible (HTTP {response.status_code}).")

            response.raise_for_status()
            data = response.json()

            # Extraemos la tasa de cambio desde el diccionario 'rates' de Frankfurter
            rates = data.get("rates", {})
            tasa = float(rates.get(moneda_destino, 0.0))

            if tasa == 0.0:
                return cls._manejar_contingencia(float(monto_base_clp), "CLP", moneda_destino, "La tasa retornada fue cero.")

            monto_ajustado = round(monto_base_clp * tasa, 2)

            resultado = {
                "monto_origen_clp": float(monto_base_clp),
                "moneda_destino": moneda_destino,
                "tasa_aplicada": tasa,
                "monto_final_ajustado": monto_ajustado,
                "fecha_indicador": data.get("date", "Desconocida"),
                "fuente": "APIs Externas (REST Countries + Frankfurter)"
            }

            msg = f"Pago calculado con éxito para {nombre_pais_oficial} (Tasa: {tasa} {moneda_destino}/CLP)."
            return (msg, resultado)

        except requests.exceptions.RequestException:
            logger.warning("Falla de red con la API de divisas. Activando contingencia.")
            return cls._manejar_contingencia(float(monto_base_clp), "CLP", moneda_destino, "Falla de red con la API de conversión.")

    @classmethod
    def _manejar_contingencia(
        cls,
        monto_base_clp: float,
        origen: str,
        destino: str,
        causa_error: str
    ) -> Tuple[str, Dict[str, Any] | None]:
        """Plan de contingencia offline usando tasas referenciales locales si fallan las APIs."""
        if not Settings.ENABLE_OFFLINE_FALLBACK:
            return (f"{causa_error} (El modo contingencia offline está deshabilitado).", None)

        tasa = cls.TASAS_CONTINGENCIA.get((origen, destino))
        if not tasa:
            return (f"[CONTINGENCIA] {causa_error} No existe tasa de respaldo local para CLP -> {destino}.", None)

        monto_ajustado = round(monto_base_clp * tasa, 2)
        resultado_local = {
            "monto_origen_clp": monto_base_clp,
            "moneda_destino": destino,
            "tasa_aplicada": tasa,
            "monto_final_ajustado": monto_ajustado,
            "fecha_indicador": "Referencia local almacenada",
            "fuente": "Modo Contingencia (Offline)"
        }

        msg = f"[CONTINGENCIA] {causa_error} Usando tasa referencial local: 1 CLP = {tasa} {destino}"
        return (msg, resultado_local)