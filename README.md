# Sistema de Gestión EcoTech Solutions

Aplicación de consola desarrollada en Python para la administración integral de empleados, departamentos, proyectos, registros de tiempo, usuarios e informes, ampliada con **integración de servicios externos en tiempo real** para la planificación operativa y la gestión financiera internacional.

Implementa una arquitectura **MVC + DAO** con persistencia relacional en **SQLite**, seguridad basada en credenciales encriptadas (`SHA-256`), externalización de configuraciones mediante variables de entorno (`.env`) y mecanismos de tolerancia a fallos.

---

## Estado actual del proyecto

| Indicador | Avance |
|---|---:|
| Avance técnico | **92%** |
| Avance funcional | **90%** |
| Seguridad y resiliencia API | **95%** |

### Avance por módulo

| Módulo | Avance | Estado |
|---|---:|---|
| Arquitectura MVC + DAO | 95% | Implementado |
| Configuración y entorno (`.env` / `Settings`) | 95% | Implementado |
| Usuarios y autenticación (`SHA-256`) | 95% | Implementado |
| API del Clima (`WeatherAPI` + viabilidad operativa) | 95% | Implementado |
| API de Moneda (`REST Countries` + `Frankfurter`) | 95% | Implementado |
| Proyectos y transacciones internacionales | 92% | Implementado |
| Seguridad, sanitización y manejo de errores | 92% | Implementado |
| Base de datos SQLite y DAOs | 90% | Implementado |
| Modelos de dominio y validaciones | 90% | Implementado |
| Empleados y Departamentos | 85% | Implementado |
| Control de tiempos | 80% | Funcional |
| Documentación técnica y trazabilidad IA | 95% | Implementado |
| Informes | 20% | Estructura base |

---

## Problemáticas de EcoTech Solutions y Solución Implementada

### 1. Planificación operativa de proyectos (Integración Climática)
* **Problemática:** Los proyectos de tecnologías sostenibles en terreno sufrían retrasos por condiciones climáticas no previstas al carecer de variables meteorológicas externas en la planificación.
* **Solución en el repositorio:**
  * Se desarrolló `ClimaService` (`services/clima_service.py`) conectado a **WeatherAPI** (`current.json` y `forecast.json`).
  * Desde `ProyectoController.servicio_clima()` y `ProyectoView`, los usuarios autenticados consultan el clima actual y el pronóstico a futuro (hasta 3 días) de la ciudad de operación.
  * El método `evaluar_viabilidad_operativa()` analiza automáticamente temperatura, humedad, viento y precipitaciones para clasificar la jornada en **`ÓPTIMO`**, **`PRECAUCIÓN`** o **`RIESGO ALTO`**, entregando recomendaciones operativas y alertas preventivas.

### 2. Gestión de pagos internacionales (Integración Monetaria)
* **Problemática:** Al expandir proyectos a distintos países, el sistema calculaba sueldos únicamente en pesos chilenos (`CLP`) sin detectar la moneda local ni aplicar tasas de cambio actualizadas.
* **Solución en el repositorio:**
  * Se desarrolló `MonedaService` (`services/moneda_service.py`) integrando dos APIs externas:
    1. **REST Countries (`/v3.1`):** identifica automáticamente el código ISO de la moneda oficial del país donde se ejecuta el proyecto (soportando nombres en español e inglés).
    2. **Frankfurter (`/v2/rate/CLP/{destino}`):** obtiene el tipo de cambio actualizado desde `CLP` hacia la moneda destino.
  * En `ProyectoController.ejecutar_trans()`, el sistema calcula el sueldo convertido para cada empleado asignado al proyecto, registra cada operación en SQLite mediante `Transaccion` / `TransaccionDAO` y genera un reporte consolidado en `ProyectoView.reporte_pago()`.

### 3. Problemáticas técnicas iniciales resueltas
* **Consumo deficiente de APIs:** Se reemplazaron peticiones aisladas por sesiones HTTP persistentes (`requests.Session`) con reintentos automáticos (`HTTPAdapter` + `Retry`), timeouts configurables y filtrado de campos (`?fields=`).
* **Falta de control de acceso:** Se impuso autenticación obligatoria antes de acceder al menú principal y a cualquier servicio externo.
* **Validación insuficiente de entradas:** Se incorporó sanitización mediante expresiones regulares Unicode y validación estricta de tipos y formatos en modelos y servicios.
* **Interrupciones ante caídas de red:** Se implementó manejo jerárquico de excepciones y respaldo automático mediante tablas de contingencia offline (`ENABLE_OFFLINE_FALLBACK=True`).
* **Exposición de datos sensibles:** Se aislaron API keys, URLs y credenciales iniciales en `.env`, evitando mostrar trazas internas en consola.

---

## Cumplimiento Técnico por Área (Objetivos 3.1.1 – 3.1.4)

### 3.1.1 Consumo de Servicios Externos mediante APIs
* **Solicitudes HTTP óptimas y seguras:** Implementadas mediante la librería oficial `requests` utilizando `requests.Session`, encabezados estándar (`Accept: application/json`, `User-Agent`), `timeout=Settings.REQUEST_TIMEOUT` y política de reintentos (`Retry`) ante errores transitorios `502`, `503` y `504`. Además, la importación de `requests` está protegida (`REQUESTS_AVAILABLE`) para evitar fallos abruptos si la dependencia no está instalada.
* **Procesamiento estructurado de respuestas JSON:** Las respuestas obtenidas con `response.json()` son validadas y transformadas en diccionarios limpios y desacoplados (`resultado_clima`, `resultado_pronostico`, `resultado` de conversión), aislando la estructura externa de las vistas y controladores.
* **Selección y filtrado preciso de datos:**
  * En **REST Countries** se envía el parámetro `fields=name,translations,currencies` para descargar únicamente los campos necesarios y descartar metadatos irrelevantes.
  * En **WeatherAPI** se solicita `lang=es` y solo se extraen temperatura, sensación térmica, condición, humedad, viento y probabilidad de lluvia.
  * En `ProyectoController.ejecutar_trans()` se consulta la moneda del país **una sola vez por proyecto** fuera del ciclo de empleados, apoyado por caché en memoria (`_cache_paises` y `_cache_tasas`) para evitar consultas N+1 redundantes.
* **Integración y consistencia lógica:** Los cálculos monetarios emplean aritmética decimal exacta (`decimal.Decimal` con redondeo financiero `ROUND_HALF_UP`) para evitar imprecisiones de punto flotante, validando que tasas y montos sean finitos y mayores a cero antes de persistirlos en la tabla `transaccion`.

### 3.1.2 Mecanismos Básicos de Seguridad y Control de Acceso
* **Autenticación con credenciales encriptadas:** `AuthController`, `Usuario` (`models/usuario.py`) y `UsuarioDAO` gestionan el inicio de sesión ocultando la contraseña en consola con `pwinput`, encriptando claves con **SHA-256** (`hashlib.sha256`) y verificándolas en tiempo constante mediante `hmac.compare_digest` para mitigar ataques de temporización. Incluye bloqueo por máximo de intentos (`MAX_LOGIN_ATTEMPTS`) y protección contra auto-eliminación del usuario activo.
* **Validaciones exhaustivas de entrada:**
  * `ClimaService.sanitizar_ciudad()` y `MonedaService._sanitizar_pais()` validan longitud, tipo y caracteres permitidos mediante expresiones regulares Unicode (`re.fullmatch`), codificando parámetros de ruta con `urllib.parse.quote` para evitar inyección en URLs.
  * `Usuario.validar_credenciales_ingreso()` bloquea campos vacíos, longitudes mínimas incumplidas y caracteres no permitidos.
  * Todos los DAOs utilizan consultas SQL parametrizadas (`?`) para prevenir inyección SQL.
* **Gestión de información sensible:** `config/settings.py` carga las variables desde `.env` (ignorado en Git mediante `.gitignore` y documentado en `.env.example`), desacoplando `API_KEY_CLIMA`, endpoints base, timeouts y credenciales iniciales del código fuente.
* **Control de flujo inquebrantable:** En `MainController.ejecutar()`, el flujo del programa exige superar `AuthController.iniciar_sesion()` antes de desplegar el menú principal o permitir el acceso a `ProyectoController`, garantizando que **ningún usuario no autenticado** pueda consumir `ClimaService` ni `MonedaService`. Adicionalmente, las opciones administrativas se restringen según el rol (`Administrador` vs `Empleado`).

### 3.1.3 Manejo de Errores, Excepciones y Resiliencia Operativa
* **Manejo jerárquico de excepciones:** En `MonedaService`, `ClimaService` y `ProyectoController` se aislaron los errores según su naturaleza: `ValueError` para datos o parámetros inválidos, `Timeout` / `ConnectionError` / `RequestException` (`REQUEST_ERROR`) para fallos de red y `RuntimeError` para dependencias faltantes o límites de cuota, evitando bloques `except Exception` genéricos que oculten fallos de programación.
* **Gestión de red, desconexiones y timeouts:** Todas las llamadas HTTP definen un tiempo máximo de espera (`Settings.REQUEST_TIMEOUT`) y capturan caídas de red o DNS sin detener la ejecución del sistema.
* **Tratamiento específico por categoría HTTP:**
  * `200 OK`: validación de estructura JSON y extracción de indicadores.
  * `400 / 404 / 422`: recurso inexistente o parámetro inválido (ciudad, país o moneda no soportada).
  * `401 / 403`: alerta controlada de API Key inválida o no autorizada sin exponer credenciales.
  * `429`: detección explícita de límite de peticiones excedido (rate limit).
  * `500–599`: detección de indisponibilidad del servidor externo y activación de contingencia.
* **Continuidad operativa y mensajes seguros:** Si ocurre un fallo de conectividad o de servidor externo y `ENABLE_OFFLINE_FALLBACK=True`, los servicios activan automáticamente respaldos locales (`CLIMA_CONTINGENCIA`, `CONTINGENCIA_PAISES` y `CONTINGENCIA_TASAS_CLP`). Los detalles técnicos se registran internamente mediante `logging`, mostrando al usuario final únicamente mensajes claros y seguros.

---

## 3.1.4 Evaluación, Análisis Crítico y Refactorización con Apoyo de IA

Durante el desarrollo se emplearon herramientas de inteligencia artificial (**GitHub Copilot** y **Gemini**) como apoyo para acelerar el diseño de servicios, vistas de consola y diagnóstico de errores, sometiendo cada fragmento generado a revisión técnica antes de integrarlo al repositorio.

### 1. Evidencia de Prompts, Respuestas y Componentes Generados
* **Prompt 1 — Diagnóstico de integración monetaria:**
  * *Consulta realizada:* *"Detecta las fallas que tiene el módulo MonedaService y su integración con ProyectoController."*
  * *Respuesta y componentes revisados:* La IA identificó inconsistencias entre el tipo de retorno esperado por `ProyectoController` (`str` con código ISO) y el diccionario retornado inicialmente por el servicio, además de señalar la ausencia de resolución para nombres de países en español (`translations.spa`).
* **Prompt 2 — Refactorización de servicios externos y manejo de errores:**
  * *Consulta realizada:* *"Refactoriza MonedaService para estructurar solicitudes HTTP seguras, manejar categorías de respuesta HTTP, evitar consultas repetidas y soportar contingencia offline."*
  * *Componentes generados:* Estructura base de `_consultar_api()`, sesión HTTP con `HTTPAdapter`/`Retry`, cachés de clase (`_cache_paises`, `_cache_tasas`) y tablas de contingencia offline.
* **Prompt 3 — Estructuración de vistas y diagnóstico de avance:**
  * *Consulta realizada:* *"Estructura vistas en consola para reportes climáticos y pagos internacionales, y audita los errores pendientes en el repositorio."*
  * *Componentes generados:* Formateo tabular de `ProyectoView.resultado_clima