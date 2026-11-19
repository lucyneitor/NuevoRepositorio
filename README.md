# Sistema de Gestión EcoTech Solutions

Aplicación de consola desarrollada en Python para gestionar empleados,
departamentos, proyectos, registros de tiempo, usuarios, pagos internacionales
e informes. La persistencia se realiza en SQLite y el flujo de la aplicación
se organiza mediante controladores, vistas, modelos y DAOs.

## Funcionalidades disponibles

- Inicio de sesión obligatorio con roles `Administrador` y `Empleado`.
- Creación automática del usuario administrador inicial cuando la tabla
  `usuario` está vacía.
- Gestión de empleados y departamentos.
- Gestión de proyectos con estado `Pendiente`, `En proceso` o `Finalizado`.
- Registro de horas trabajadas por empleado y proyecto.
- Consulta del clima actual y pronóstico de hasta tres días mediante WeatherAPI.
- Evaluación de viabilidad operativa a partir de temperatura, viento, humedad,
  lluvia y condición climática.
- Detección de la moneda de un país mediante `countries.dev`.
- Conversión de montos desde CLP mediante Frankfurter.
- Registro de transacciones internacionales y generación de reportes de pago.
- Gestión de usuarios disponible para administradores.
- Módulo de informes accesible desde el menú de administrador.

Las consultas climáticas y monetarias requieren conexión a Internet y sus
respectivas variables de configuración. Si una API falla, el servicio
monetario informa el error y no registra una conversión incompleta.

## Arquitectura

```text
main.py
├── controllers/   Flujo de la aplicación y reglas de interacción
├── views/         Menús, formularios y salida por consola
├── models/        Entidades y objetos de acceso a datos (DAO)
├── services/      Integraciones de clima y moneda
└── config/        Configuración y conexión/inicialización de SQLite
```

La base de datos se crea en `sistema_gestion.db`, en la raíz del proyecto.
`config/database.py` crea las tablas y carga datos iniciales de ejemplo para
departamentos, empleados, proyectos y registros de tiempo. La inicialización
de datos usa inserciones idempotentes para no duplicar los registros de
ejemplo al reiniciar la aplicación.

## Requisitos

- Python 3.10 o superior.
- Dependencias indicadas en `requirements.txt`.
- Una API key de WeatherAPI para consultar el clima.

## Instalación y ejecución

En Windows, desde la raíz del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py main.py
```

Al ejecutar el programa por primera vez se crea la base de datos y, durante el
primer inicio de sesión, se crea el administrador inicial si todavía no existe
ningún usuario.

## Configuración

Copiar `.env.example` como `.env` y completar, al menos, `API_KEY_CLIMA`:

```dotenv
API_BASE_URL_CLIMA=https://api.weatherapi.com/v1
API_KEY_CLIMA=tu_api_key_aqui
REQUEST_TIMEOUT=5
ENABLE_OFFLINE_FALLBACK=False

API_BASE_URL_PAIS=https://countries.dev
API_BASE_URL_MONEDA=https://api.frankfurter.dev/v2

ADMIN_INITIAL_USER=admin
ADMIN_INITIAL_CLAVE=admin1234
MAX_LOGIN_ATTEMPTS=3
```

`config/settings.py` carga estas variables y aplica valores por defecto cuando
no están definidas. No se debe publicar el archivo `.env` ni una API key.

### Modo offline de clima

`ENABLE_OFFLINE_FALLBACK` está desactivado por defecto. Si se activa, el
servicio de clima puede usar datos locales referenciales únicamente para
Chillán cuando WeatherAPI no está disponible. Estos datos se muestran como
`CONTINGENCIA` y su evaluación devuelve `SIN VERIFICAR`; no autorizan labores
en terreno. El modo offline no proporciona cotizaciones monetarias.

## Integraciones externas

### WeatherAPI

`services/clima_service.py` consume:

- `current.json` para el clima actual.
- `forecast.json` para pronósticos de uno a tres días.

Las peticiones usan `requests.Session`, timeout configurable y reintentos para
errores transitorios. La API key se envía mediante parámetros de la petición y
no debe escribirse en el código fuente.

### Países y monedas

`services/moneda_service.py` consulta `API_BASE_URL_PAIS/name/{país}` para
obtener el código ISO de la moneda del proyecto. Después consulta
`API_BASE_URL_MONEDA/rate/CLP/{moneda}` para obtener la tasa y convierte el
monto con `Decimal` y redondeo financiero.

Las respuestas válidas se almacenan en cachés en memoria durante la ejecución.
La tasa se valida antes de guardar una transacción en SQLite.

## Seguridad y validaciones

- Las contraseñas no se almacenan en texto plano: se guardan como hashes
  SHA-256. SHA-256 es un hash, no cifrado reversible.
- La comparación de credenciales usa `hmac.compare_digest`.
- El acceso al menú principal requiere autenticación.
- Las opciones de gestión de usuarios e informes se muestran para
  administradores.
- Los DAOs usan consultas SQL parametrizadas.
- Se validan nombres de usuario, contraseñas, ciudades, países, monedas y
  valores numéricos antes de procesarlos.
- Las solicitudes HTTP usan timeout y manejo específico de errores de red y
  respuestas HTTP.

## Datos iniciales

La inicialización de `config/database.py` crea estas tablas:

`departamento`, `proyecto`, `empleado`, `transaccion`, `tiempo`, `informe` y
`usuario`.

También inserta departamentos, empleados, proyectos y horas de ejemplo. Los
proyectos de ejemplo incluyen destinos en Chile, Argentina, Francia, Estados
Unidos, España, Japón y Brasil; algunos proyectos se dejan sin empleados para
probar ese escenario.

Para reiniciar completamente los datos locales, detener la aplicación y
eliminar de forma manual `sistema_gestion.db`. La próxima ejecución volverá a
crear el esquema y los datos de ejemplo.
