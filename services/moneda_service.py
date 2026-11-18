import logging
import requests

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from urllib.parse import quote
from typing import Dict, Any

from config.settings import Settings


logger = logging.getLogger(__name__)


class MonedaService:
    """
    Servicio de integración monetaria de EcoTech Solutions.

    APIs:
    1. REST Countries: detecta la moneda del país.
    2. Frankfurter: obtiene el tipo de cambio.

    Moneda base del sistema: CLP.
    """

    _session = None

    # --------------------------------------------------
    # 1. CONEXIÓN HTTP
    # --------------------------------------------------

    @classmethod
    def _get_sesion(cls):
        """Crea y reutiliza una sesión HTTP."""

        if cls._session is None:

            cls._session = requests.Session()

            cls._session.headers.update({
                "Accept": "application/json",
                "User-Agent": "EcoTechSolutions/1.0"
            })

        return cls._session

    @classmethod
    def _consultar_api(cls, url: str):
        """Centraliza las solicitudes GET."""

        response = cls._get_sesion().get(
            url,
            timeout=Settings.REQUEST_TIMEOUT
        )

        response.raise_for_status()

        try:
            return response.json()

        except ValueError as error:
            raise ValueError(
                "La API devolvió una respuesta inválida."
            ) from error

    # --------------------------------------------------
    # 2. DETECCIÓN DE MONEDA
    # API: REST COUNTRIES
    # --------------------------------------------------

    @classmethod
    def obtener_moneda_por_pais(
        cls,
        nombre_pais: str
    ) -> str:
        """
        Obtiene el código monetario correspondiente
        al país ingresado.

        Parámetro:
            nombre_pais: país del proyecto.

        Retorna:
            Código de la moneda (ej. 'USD', 'CLP').
        """

        if (
            not isinstance(nombre_pais, str)
            or not nombre_pais.strip()
        ):
            raise ValueError(
                "Debes ingresar un nombre de país válido."
            )

        pais = nombre_pais.strip()

        url = (
            "https://restcountries.com/v3.1/name/"
            f"{quote(pais, safe='')}?fields=name,currencies"
        )

        data = cls._consultar_api(url)

        if not isinstance(data, list) or not data:
            raise ValueError(
                f"No se encontró información para {pais}."
            )

        # Buscar coincidencia exacta cuando sea posible.
        coincidencias = [
            item for item in data
            if item.get("name", {}).get(
                "common", ""
            ).casefold() == pais.casefold()
        ]

        if len(coincidencias) == 1:
            informacion = coincidencias[0]

        elif len(data) == 1:
            informacion = data[0]

        else:
            raise ValueError(
                "La búsqueda del país es ambigua."
            )

        nombre_oficial = informacion.get(
            "name", {}
        ).get("common", pais)

        monedas = informacion.get("currencies", {})

        if not monedas:
            raise ValueError(
                f"No se encontró moneda para {nombre_oficial}."
            )

        codigos = sorted(monedas.keys())

        if len(codigos) > 1:
            raise ValueError(
                f"{nombre_oficial} posee varias monedas: "
                f"{', '.join(codigos)}. "
                "Debes seleccionar la correspondiente."
            )

        # Retornamos únicamente el string con el código de la moneda
        return codigos[0]

    # --------------------------------------------------
    # 3. CONVERSIÓN MONETARIA
    # API: FRANKFURTER
    # --------------------------------------------------

    @classmethod
    def convertir_clp(
        cls,
        monto_clp: float,
        codigo_moneda: str
    ) -> Dict[str, Any]:
        """
        Convierte un monto CLP a la moneda indicada.

        Parámetros:
            monto_clp: monto original en pesos chilenos.
            codigo_moneda: código ISO de destino.

        Retorna:
            moneda_origen
            moneda_destino
            tasa
            monto_convertido
            fecha
        """

        if isinstance(monto_clp, bool):
            raise ValueError("El monto no es válido.")

        try:
            monto = Decimal(str(monto_clp))

        except (InvalidOperation, TypeError, ValueError):
            raise ValueError(
                "El monto debe ser numérico."
            )

        if not monto.is_finite() or monto <= 0:
            raise ValueError(
                "El monto debe ser mayor a cero."
            )

        if (
            not isinstance(codigo_moneda, str)
            or len(codigo_moneda.strip()) != 3
            or not codigo_moneda.strip().isalpha()
        ):
            raise ValueError(
                "El código monetario debe contener tres letras."
            )

        destino = codigo_moneda.strip().upper()

        # No se requiere API si ambas monedas son CLP.

        if destino == "CLP":
            return {
                "moneda_origen": "CLP",
                "moneda_destino": "CLP",
                "tasa": 1.0,
                "monto_convertido": float(monto),
                "fecha": "N/A"
            }

        url = (
            f"https://api.frankfurter.dev/v2/rate/"
            f"CLP/{destino}"
        )

        data = cls._consultar_api(url)

        try:
            tasa = Decimal(str(data["rate"]))

        except (KeyError, InvalidOperation, TypeError):
            raise ValueError(
                "No se recibió un tipo de cambio válido."
            )

        if not tasa.is_finite() or tasa <= 0:
            raise ValueError(
                "El tipo de cambio recibido es inválido."
            )

        monto_convertido = (
            monto * tasa
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        return {
            "moneda_origen": "CLP",
            "moneda_destino": destino,
            "tasa": float(tasa),
            "monto_convertido": float(monto_convertido),
            "fecha": data.get("date", "Desconocida")
        }

    # --------------------------------------------------
    # 4. PROCESO COMPLETO
    # --------------------------------------------------

    @classmethod
    def calcular_pago_internacional(
        cls,
        monto_base_clp: float,
        pais_proyecto: str
    ) -> tuple:

        """
        Coordina la detección y conversión monetaria.

        1. Detecta la moneda del país.
        2. Convierte el monto CLP.
        3. Construye el resultado final.
        """

        try:

            # Primera API: detectar moneda.
            informacion = cls.obtener_moneda_por_pais(
                pais_proyecto
            )

            codigo = informacion["codigo_moneda"]

            # Segunda API: convertir monto.
            conversion = cls.convertir_clp(
                monto_base_clp,
                codigo
            )

            # Resultado consolidado.
            resultado = {
                "pais": informacion["nombre_pais"],
                "monto_origen_clp": float(
                    monto_base_clp
                ),
                "moneda_destino": codigo,
                "tasa_aplicada": conversion["tasa"],
                "monto_final_ajustado": conversion[
                    "monto_convertido"
                ],
                "fecha_indicador": conversion["fecha"],
                "fuente": (
                    "REST Countries + Frankfurter"
                    if codigo != "CLP"
                    else "REST Countries + cálculo local"
                )
            }

            return (
                "Conversión monetaria realizada correctamente.",
                resultado
            )

        except requests.exceptions.RequestException as error:
            logger.exception(
                "Error de conexión al consumir las APIs."
            )

            return (
                "No fue posible conectar con los servicios externos.",
                None
            )

        except ValueError as error:
            return (str(error), None)

        except Exception:
            logger.exception(
                "Error inesperado en MonedaService."
            )

            return (
                "Ocurrió un error inesperado en el servicio monetario.",
                None
            )
