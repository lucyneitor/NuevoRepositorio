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
    Servicio de EcoTech Solutions para consumir indicadores económicos (Frankfurter API v2)
    y calcular el pago de trabajadores ajustado a la moneda del país del proyecto.
    """
    _session = None

    # Plan de contingencia: tasas referenciales por si falla la conexión en terreno/laboratorio
    TASAS_CONTINGENCIA = {
        ("USD", "CLP"): {"fecha": "2026-11-17", "tasa": 950.0},
        ("EUR", "CLP"): {"fecha": "2026-11-17", "tasa": 1030.0},
        ("USD", "PEN"): {"fecha": "2026-11-17", "tasa": 3.75},
        ("USD", "COP"): {"fecha": "2026-11-17", "tasa": 4350.0},
        ("USD", "MXN"): {"fecha": "2026-11-17", "tasa": 20.15},
        ("USD", "ARS"): {"fecha": "2026-11-17", "tasa": 1005.0},
        ("USD", "BRL"): {"fecha": "2026-11-17", "tasa": 5.75},
    }

    @classmethod
    def _get_sesion(cls):
        """
        Inicializa y reutiliza una sesión HTTP con encabezados estándar.
        """
        if cls._session is None and REQUESTS_AVAILABLE:
            cls._session = requests.Session()
            cls._session.headers.update({"Accept": "application/json"})
        return cls._session

    @staticmethod
    def _sanitizar_divisa(codigo: str) -> str:
        """
        Valida que el código de moneda cumpla con el estándar ISO 4217 (3 letras).
        """
        if not codigo or not isinstance(codigo, str):
            raise ValueError("El código de divisa debe ser un texto válido.")

        limpio = codigo.strip().upper()
        if not re.fullmatch(r"[A-Z]{3}", limpio):
            raise ValueError(
                f"Código de divisa '{codigo}' inválido. Use el formato ISO de 3 letras (ej: USD, CLP, EUR)."
            )
        return limpio

    @staticmethod
    def _sanitizar_monto(monto: float | int) -> float:
        """
        Valida que el sueldo o monto a pagar sea un valor numérico positivo.
        """
        try:
            valor = float(monto)
        except (TypeError, ValueError):
            raise ValueError("El monto del pago debe ser un número válido.")

        if valor <= 0:
            raise ValueError("El monto del pago debe ser mayor a cero.")
        return valor

    @classmethod
    def calcular_pago_internacional(
        cls,
        monto_base: float,
        moneda_origen: str,
        moneda_proyecto: str
    ) -> Tuple[str, Dict[str, Any] | None]:
        """
        Consume la API externa de Frankfurter para obtener el tipo de cambio actualizado
        y calcular el pago ajustado a la moneda local donde se ejecuta el proyecto.
        Retorna: (mensaje_estado, diccionario_con_calculo_de_pago)
        """
        try:
            origen_seguro = cls._sanitizar_divisa(moneda_origen)
            destino_seguro = cls._sanitizar_divisa(moneda_proyecto)
            monto_seguro = cls._sanitizar_monto(monto_base)
        except ValueError as e:
            return (str(e), None)

        # Caso donde el pago se realiza en la misma moneda base (sin conversión)
        if origen_seguro == destino_seguro:
            return (
                f"Pago calculado sin conversión requerida ({origen_seguro}).",
                {
                    "fecha_indicador": "N/A",
                    "moneda_origen": origen_seguro,
                    "moneda_proyecto": destino_seguro,
                    "tasa_cambio": 1.0,
                    "monto_base": monto_seguro,
                    "pago_ajustado": round(monto_seguro, 2),
                    "fuente": "Directo (Misma divisa)"
                }
            )

        # Si no está instalada la librería requests, activa el plan de contingencia
        if not REQUESTS_AVAILABLE:
            return cls._manejar_contingencia(
                monto_seguro, origen_seguro, destino_seguro,
                "Librería 'requests' no instalada en el entorno."
            )

        # Endpoint de Frankfurter v2 para par específico: /v2/rate/{base}/{quote}
        url = f"{Settings.API_BASE_URL_MONEDA}/rate/{origen_seguro.lower()}/{destino_seguro.lower()}"

        try:
            session = cls._get_sesion()
            response = session.get(url, timeout=Settings.REQUEST_TIMEOUT)

            # Manejo de errores HTTP de cliente (moneda inexistente o no soportada)
            if response.status_code in (400, 404, 422):
                detalle = response.json().get("message", "Moneda no soportada por el indicador.")
                return (f"Error ({response.status_code}): {detalle}", None)
            elif response.status_code == 429:
                logger.warning("Límite de consultas excedido en Frankfurter API (HTTP 429).")
                return cls._manejar_contingencia(
                    monto_seguro, origen_seguro, destino_seguro,
                    "Límite de peticiones excedido en la API externa (HTTP 429)."
                )
            elif 500 <= response.status_code < 600:
                logger.error("Error interno en servidor de Frankfurter (HTTP %s).", response.status_code)
                return cls._manejar_contingencia(
                    monto_seguro, origen_seguro, destino_seguro,
                    f"El servidor de indicadores económicos no está disponible (HTTP {response.status_code})."
                )

            response.raise_for_status()
            data = response.json()

            tasa = float(data.get("rate", 0.0))
            pago_ajustado = round(monto_seguro * tasa, 2)

            resultado_pago = {
                "fecha_indicador": data.get("date", "Desconocida"),
                "moneda_origen": data.get("base", origen_seguro),
                "moneda_proyecto": data.get("quote", destino_seguro),
                "tasa_cambio": tasa,
                "monto_base": monto_seguro,
                "pago_ajustado": pago_ajustado,
                "fuente": "Frankfurter API (En línea)"
            }

            msg = (
                f"Pago ajustado exitosamente: {monto_seguro} {origen_seguro} = "
                f"{pago_ajustado} {destino_seguro} (Tasa: {tasa})."
            )
            return (msg, resultado_pago)

        except requests.exceptions.RequestException:
            logger.exception("Error de red en MonedaService al consultar indicador económico.")
            return cls._manejar_contingencia(
                monto_seguro, origen_seguro, destino_seguro,
                "Falla de comunicación de red con el servicio de indicadores económicos."
            )

    @classmethod
    def _manejar_contingencia(
        cls,
        monto_base: float,
        moneda_origen: str,
        moneda_proyecto: str,
        causa_error: str
    ) -> Tuple[str, Dict[str, Any] | None]:
        """
        Plan de contingencia: respalda el cálculo de pagos usando tasas referenciales
        locales si la API externa falla y ENABLE_OFFLINE_FALLBACK está habilitado.
        """
        if not Settings.ENABLE_OFFLINE_FALLBACK:
            return (f"{causa_error} (El modo contingencia offline está deshabilitado).", None)

        respaldo = cls.TASAS_CONTINGENCIA.get((moneda_origen, moneda_proyecto))

        # Si no está el par directo, intenta calcular la tasa inversa si existe en el diccionario
        if not respaldo:
            inverso = cls.TASAS_CONTINGENCIA.get((moneda_proyecto, moneda_origen))
            if inverso and inverso["tasa"] > 0:
                respaldo = {
                    "fecha": inverso["fecha"],
                    "tasa": round(1.0 / inverso["tasa"], 6)
                }

        if not respaldo:
            return (
                f"[MODO CONTINGENCIA] {causa_error} No existe tasa de respaldo local "
                f"para el par {moneda_origen} -> {moneda_proyecto}.",
                None
            )

        tasa = respaldo["tasa"]
        pago_ajustado = round(monto_base * tasa, 2)

        resultado_local = {
            "fecha_indicador": respaldo["fecha"],
            "moneda_origen": moneda_origen,
            "moneda_proyecto": moneda_proyecto,
            "tasa_cambio": tasa,
            "monto_base": monto_base,
            "pago_ajustado": pago_ajustado,
            "fuente": "Contingencia Local (Offline)"
        }

        msg = (
            f"[MODO CONTINGENCIA] {causa_error}\n"
            f"Pago calculado con tasa referencial local ({tasa}): "
            f"{monto_base} {moneda_origen} = {pago_ajustado} {moneda_proyecto}."
        )
        return (msg, resultado_local)

    @classmethod
    def probar_conectividad(cls) -> Tuple[bool, str]:
        """
        Verifica si la API externa de indicadores económicos (Frankfurter) está operativa.
        """
        if not REQUESTS_AVAILABLE:
            return (
                False,
                "Librería 'requests' no instalada. Ejecute 'pip install requests'."
            )

        try:
            session = cls._get_sesion()
            # Consulta un par estándar y ligero (USD a EUR) para validar disponibilidad
            url = f"{Settings.API_BASE_URL_MONEDA}/rate/usd/eur"
            resp = session.get(url, timeout=Settings.REQUEST_TIMEOUT)

            if resp.status_code == 200:
                return (
                    True,
                    f"Conexión exitosa con Frankfurter API (Código HTTP: {resp.status_code})."
                )

            return (
                False,
                f"El servidor de indicadores respondió con código HTTP inesperado: {resp.status_code}."
            )

        except requests.exceptions.Timeout:
            return (False, "Timeout al intentar contactar el servicio de indicadores económicos.")
        except requests.exceptions.ConnectionError:
            return (False, "Sin conexión de red hacia el servidor de Frankfurter API.")
        except requests.exceptions.RequestException as e:
            logger.error("Error de red al probar conectividad con Frankfurter: %s", str(e))
            return (False, "Ocurrió un problema de comunicación con el servicio externo. Intente más tarde.")