import logging
import re
import unicodedata
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any, Dict, Optional, Tuple
from urllib.parse import quote

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    REQUESTS_AVAILABLE = True
except ImportError:
    requests=None
    REQUESTS_AVAILABLE = False
from config.settings import Settings

logger = logging.getLogger(__name__)

def _normalizar_texto(texto: str) -> str:
    """Elimina tildes y normaliza mayúsculas/minúsculas."""
    nfkd = unicodedata.normalize("NFKD", texto.strip())
    sin_tildes = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sin_tildes.casefold()


class MonedaService:
    """
    Servicio de integración monetaria de EcoTech Solutions.

    APIs:
    1. REST Countries: detecta la moneda oficial del país del proyecto.
    2. Frankfurter: obtiene el tipo de cambio actualizado desde CLP.
    """

    _session = None
    _cache_paises: Dict[str, Dict[str, str]] = {}
    _cache_tasas: Dict[Tuple[str, str], Tuple[Decimal, str]] = {}

    CONTINGENCIA_PAISES = {
        "chile": {"nombre_pais": "Chile", "codigo_moneda": "CLP"},
        "estados unidos": {"nombre_pais": "Estados Unidos", "codigo_moneda": "USD"},
        "espana": {"nombre_pais": "España", "codigo_moneda": "EUR"},
        "alemania": {"nombre_pais": "Alemania", "codigo_moneda": "EUR"},
        "reino unido": {"nombre_pais": "Reino Unido", "codigo_moneda": "GBP"},
        "japon": {"nombre_pais": "Japón", "codigo_moneda": "JPY"},
        "brasil": {"nombre_pais": "Brasil", "codigo_moneda": "BRL"},
        "mexico": {"nombre_pais": "México", "codigo_moneda": "MXN"},
        "canada": {"nombre_pais": "Canadá", "codigo_moneda": "CAD"},
        "australia": {"nombre_pais": "Australia", "codigo_moneda": "AUD"},
    }

    # Tasas referenciales CLP -> Moneda destino solo para contingencia offline
    CONTINGENCIA_TASAS_CLP = {
        "USD": Decimal("0.00105"),
        "EUR": Decimal("0.00097"),
        "GBP": Decimal("0.00083"),
        "JPY": Decimal("0.16"),
        "BRL": Decimal("0.0061"),
        "MXN": Decimal("0.021"),
        "CAD": Decimal("0.00147"),
        "AUD": Decimal("0.00162"),
    }

    # --------------------------------------------------
    # 1. CONEXIÓN HTTP Y SANITIZACIÓN
    # --------------------------------------------------

    @classmethod
    def _get_sesion(cls) -> requests.Session:
        """Crea y reutiliza una sesión HTTP con reintentos."""
        if cls._session is None:
            sesion = requests.Session()
            sesion.headers.update({
                "Accept": "application/json",
                "User-Agent": "EcoTechSolutions/1.0",
            })
            reintentos = Retry(
                total=2,
                backoff_factor=0.3,
                status_forcelist=(502, 503, 504),
                allowed_methods=("GET",),
            )
            adaptador = HTTPAdapter(max_retries=reintentos)
            sesion.mount("https://", adaptador)
            sesion.mount("http://", adaptador)
            cls._session = sesion

        return cls._session

    @classmethod
    def _consultar_api(cls, url: str, mensaje_no_encontrado: str = "Recurso no encontrado."):
        """Ejecuta una petición GET diferenciando errores de datos (4xx) de red."""
        response = cls._get_sesion().get(
            url,
            timeout=Settings.REQUEST_TIMEOUT,
        )

        if response.status_code in (400, 404, 422):
            raise ValueError(mensaje_no_encontrado)

        response.raise_for_status()

        try:
            return response.json()
        except ValueError as error:
            raise ValueError("La API devolvió una respuesta JSON inválida.") from error

    @staticmethod
    def _sanitizar_pais(nombre_pais: str) -> str:
        """Valida que el nombre del país sea texto válido."""
        if not isinstance(nombre_pais, str) or not nombre_pais.strip():
            raise ValueError("Debes ingresar un nombre de país válido.")

        limpio = nombre_pais.strip()
        if len(limpio) < 2 or not re.fullmatch(r"[^\W\d_]+(?:[ '\-\.][^\W\d_]+)*", limpio, re.UNICODE):
            raise ValueError("El nombre del país contiene caracteres no permitidos.")

        return limpio

    # --------------------------------------------------
    # 2. DETECCIÓN DE MONEDA (REST COUNTRIES)
    # --------------------------------------------------

    @classmethod
    def _coincide_pais(cls, item: Dict[str, Any], pais_buscado: str) -> bool:
        """Compara el país ingresado con nombres oficiales/comunes en inglés y español."""
        objetivo = _normalizar_texto(pais_buscado)
        name_data = item.get("name", {})
        spa_data = item.get("translations", {}).get("spa", {})

        candidatos = [
            name_data.get("common", ""),
            name_data.get("official", ""),
            spa_data.get("common", ""),
            spa_data.get("official", ""),
        ]
        return any(_normalizar_texto(c) == objetivo for c in candidatos if c)

    @classmethod
    def _obtener_detalle_pais(
        cls,
        nombre_pais: str,
        moneda_preferida: Optional[str] = None,
    ) -> Dict[str, str]:
        """Obtiene el nombre oficial y el código ISO de moneda para un país."""
        pais = cls._sanitizar_pais(nombre_pais)
        pref = (moneda_preferida or "").strip().upper()
        clave_cache = f"{_normalizar_texto(pais)}:{pref}"

        if clave_cache in cls._cache_paises:
            return cls._cache_paises[clave_cache].copy()

        base_url = (Settings.API_BASE_URL_PAIS or "https://restcountries.com/v3.1").rstrip("/")
        encoded = quote(pais, safe="")
        fields = "fields=name,translations,currencies"

        try:
            try:
                data = cls._consultar_api(
                    f"{base_url}/name/{encoded}?{fields}",
                    f"No se encontró información para '{pais}'.",
                )
            except ValueError:
                data = cls._consultar_api(
                    f"{base_url}/translation/{encoded}?{fields}",
                    f"No se encontró información para '{pais}'.",
                )
        except requests.exceptions.RequestException:
            if Settings.ENABLE_OFFLINE_FALLBACK:
                clave_offline = _normalizar_texto(pais)
                if clave_offline in cls.CONTINGENCIA_PAISES:
                    logger.warning("Modo contingencia activo para país '%s'.", pais)
                    return cls.CONTINGENCIA_PAISES[clave_offline].copy()
            raise

        if not isinstance(data, list) or not data:
            raise ValueError(f"No se encontró información para '{pais}'.")

        coincidencias = [item for item in data if cls._coincide_pais(item, pais)]

        if len(coincidencias) == 1:
            informacion = coincidencias[0]
        elif len(data) == 1:
            informacion = data[0]
        else:
            raise ValueError(f"La búsqueda del país '{pais}' es ambigua.")

        nombre_oficial = (
            informacion.get("translations", {}).get("spa", {}).get("common")
            or informacion.get("name", {}).get("common", pais)
        )
        monedas = informacion.get("currencies", {})

        if not monedas:
            raise ValueError(f"No se encontró moneda para {nombre_oficial}.")

        codigos = sorted(monedas.keys())

        if len(codigos) > 1:
            if pref and pref in codigos:
                codigo_elegido = pref
            else:
                raise ValueError(
                    f"{nombre_oficial} posee varias monedas: {', '.join(codigos)}. "
                    "Debes seleccionar la correspondiente."
                )
        else:
            codigo_elegido = codigos[0]

        resultado = {
            "nombre_pais": nombre_oficial,
            "codigo_moneda": codigo_elegido,
        }
        cls._cache_paises[clave_cache] = resultado.copy()
        return resultado

    @classmethod
    def obtener_moneda_por_pais(
        cls,
        nombre_pais: str,
        moneda_preferida: Optional[str] = None,
    ) -> str:
        """Retorna el código ISO de la moneda correspondiente al país (ej. 'USD', 'EUR')."""
        return cls._obtener_detalle_pais(nombre_pais, moneda_preferida)["codigo_moneda"]

    # --------------------------------------------------
    # 3. CONVERSIÓN MONETARIA (FRANKFURTER)
    # --------------------------------------------------

    @classmethod
    def convertir_clp(
        cls,
        monto_clp: float,
        codigo_moneda: str,
    ) -> Dict[str, Any]:
        """Convierte un monto desde CLP a la moneda ISO de destino."""
        if isinstance(monto_clp, bool):
            raise ValueError("El monto no es válido.")

        try:
            monto = Decimal(str(monto_clp))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError("El monto debe ser numérico.")

        if not monto.is_finite() or monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")

        if (
            not isinstance(codigo_moneda, str)
            or len(codigo_moneda.strip()) != 3
            or not codigo_moneda.strip().isalpha()
        ):
            raise ValueError("El código monetario debe contener tres letras.")

        destino = codigo_moneda.strip().upper()
        fecha_hoy = date.today().isoformat()

        if destino == "CLP":
            monto_norm = monto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            return {
                "moneda_origen": "CLP",
                "moneda_destino": "CLP",
                "tasa": 1.0,
                "monto_convertido": float(monto_norm),
                "fecha": fecha_hoy,
            }

        clave_tasa = (destino, fecha_hoy)
        if clave_tasa in cls._cache_tasas:
            tasa, fecha_api = cls._cache_tasas[clave_tasa]
        else:
            base_url = (Settings.API_BASE_URL_MONEDA or "https://api.frankfurter.dev/v2").rstrip("/")
            url = f"{base_url}/rate/CLP/{destino}"

            try:
                data = cls._consultar_api(
                    url,
                    f"La moneda '{destino}' no está disponible en el proveedor de cambio.",
                )
                try:
                    tasa = Decimal(str(data["rate"]))
                except (KeyError, InvalidOperation, TypeError):
                    raise ValueError("No se recibió un tipo de cambio válido.")

                if not tasa.is_finite() or tasa <= 0:
                    raise ValueError("El tipo de cambio recibido es inválido.")

                fecha_api = data.get("date", fecha_hoy)
                cls._cache_tasas[clave_tasa] = (tasa, fecha_api)

            except (requests.exceptions.RequestException, ValueError):
                if Settings.ENABLE_OFFLINE_FALLBACK and destino in cls.CONTINGENCIA_TASAS_CLP:
                    logger.warning("Usando tasa referencial de contingencia para CLP -> %s.", destino)
                    tasa = cls.CONTINGENCIA_TASAS_CLP[destino]
                    fecha_api = fecha_hoy
                else:
                    raise

        bruto = monto * tasa
        monto_convertido = bruto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if monto_convertido == Decimal("0.00"):
            monto_convertido = bruto.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)

        return {
            "moneda_origen": "CLP",
            "moneda_destino": destino,
            "tasa": float(tasa),
            "monto_convertido": float(monto_convertido),
            "fecha": fecha_api,
        }

    # --------------------------------------------------
    # 4. PROCESO COMPLETO (CONSULTA INDIVIDUAL)
    # --------------------------------------------------

    @classmethod
    def calcular_pago_internacional(
        cls,
        monto_base_clp: float,
        pais_proyecto: str,
        moneda_preferida: Optional[str] = None,
    ) -> tuple:
        """Coordina la detección de moneda y conversión desde CLP en un solo paso."""
        try:
            informacion = cls._obtener_detalle_pais(pais_proyecto, moneda_preferida)
            codigo = informacion["codigo_moneda"]
            conversion = cls.convertir_clp(monto_base_clp, codigo)

            resultado = {
                "pais": informacion["nombre_pais"],
                "monto_origen_clp": float(monto_base_clp),
                "moneda_destino": codigo,
                "tasa_aplicada": conversion["tasa"],
                "monto_final_ajustado": conversion["monto_convertido"],
                "fecha_indicador": conversion["fecha"],
                "fuente": (
                    "REST Countries + Frankfurter"
                    if codigo != "CLP"
                    else "REST Countries + cálculo local"
                ),
            }

            return ("Conversión monetaria realizada correctamente.", resultado)

        except requests.exceptions.RequestException:
            logger.exception("Error de conexión al consumir las APIs monetarias.")
            return ("No fue posible conectar con los servicios externos.", None)

        except ValueError as error:
            return (str(error), None)

        except Exception:
            logger.exception("Error inesperado en MonedaService.")
            return ("Ocurrió un error inesperado en el servicio monetario.", None)