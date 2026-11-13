# Sistema de Gestión Empresarial

Aplicación de consola desarrollada en Python para administrar empleados,
departamentos, proyectos, registros de tiempo, usuarios e informes.

## Estado del proyecto

El proyecto se encuentra en desarrollo.

**Avance funcional estimado: 40%**

La estimación considera la implementación actual, la integración entre módulos
y la posibilidad de ejecutar correctamente los flujos principales.

| Módulo | Avance |
|---|---:|
| Estructura general | 70% |
| Configuración | 55% |
| Base de datos | 65% |
| Modelos de dominio | 55% |
| Usuarios y autenticación | 50% |
| Empleados | 35% |
| Departamentos | 50% |
| Proyectos | 35% |
| Control de tiempos | 30% |
| Informes | 15% |
| Servicios externos | 35% |
| Validaciones | 45% |
| Seguridad | 35% |
| Pruebas automatizadas | 5% |
| Documentación | 40% |

## Funcionalidades previstas

- Autenticación de usuarios.
- Gestión de roles:
  - Administrador.
  - Empleado.
- Gestión de empleados.
- Gestión de departamentos.
- Gestión de proyectos.
- Registro de horas trabajadas.
- Consulta de tiempos por empleado, proyecto y fecha.
- Generación de informes.
- Consulta del clima mediante WeatherAPI.
- Persistencia local mediante SQLite.

## Tecnologías

- Python 3.10 o superior.
- SQLite.
- Pydantic.
- python-dotenv.
- Requests.
- pwinput.

## Estructura del proyecto

```text
config/
  database.py
  settings.py

models/
  modelos de dominio y DAO

controllers/
  lógica de navegación y aplicación

views/
  menús, formularios y presentación por consola

services/
  integraciones con servicios externos

main.py
requirements.txt
.env.example
```

## Instalación

Crear y activar un entorno virtual:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Crear el archivo `.env` a partir de `.env.example`:

### Windows

```bash
copy .env.example .env
```

### Linux/macOS

```bash
cp .env.example .env
```

Configurar las variables:

```dotenv
API_BASE_URL_CLIMA=http://api.weatherapi.com/v1/current.json
API_KEY_CLIMA=tu_api_key
REQUEST_TIMEOUT=5
ENABLE_OFFLINE_FALLBACK=True
ADMIN_INITIAL_USER=admin
ADMIN_INITIAL_CLAVE=cambiar_esta_clave
MAX_LOGIN_ATTEMPTS=3
```

No subir el archivo `.env` al repositorio.

## Ejecución

```bash
python main.py
```

La aplicación inicializa la base de datos SQLite y muestra el flujo de
autenticación antes de acceder al menú principal.

## Base de datos

La base de datos se crea automáticamente en:

```text
sistema_gestion.db
```

Las entidades principales son:

- `usuario`
- `empleado`
- `departamento`
- `proyecto`
- `tiempo`
- `informe`

## Trabajo pendiente

- Corregir la integración entre modelos, DAO, controladores y vistas.
- Completar el CRUD de empleados.
- Completar el CRUD de departamentos.
- Corregir el CRUD de proyectos.
- Completar el registro y consulta de tiempos.
- Implementar los informes.
- Integrar o eliminar el servicio de moneda.
- Corregir la configuración de WeatherAPI.
- Sustituir SHA-256 por un algoritmo seguro para contraseñas.
- Agregar pruebas automatizadas.
- Añadir integración continua con GitHub Actions.
- Mejorar el manejo de errores y los mensajes al usuario.

## Pruebas

Actualmente el proyecto no cuenta con una suite de pruebas automatizadas.

Se recomienda agregar pruebas con `pytest` para:

- Inicialización de la base de datos.
- Creación y consulta de empleados.
- Autenticación de usuarios.
- Gestión de departamentos.
- Gestión de proyectos.
- Registro de tiempos.
- Generación de informes.

## Licencia

La licencia del proyecto aún no ha sido definida.