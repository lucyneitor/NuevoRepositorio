# 🌱 Sistema de Gestión EcoTech Solutions

Aplicación de consola desarrollada en **Python** para la administración integral de los recursos humanos y operativos de EcoTech Solutions. Permite gestionar empleados, departamentos, proyectos, registros de tiempo, usuarios, pagos internacionales e informes, incorporando servicios externos para apoyar la planificación operativa y la gestión financiera de proyectos internacionales.

El sistema implementa una arquitectura **MVC + DAO**, persistencia relacional mediante **SQLite** e integración con APIs externas para consultar información meteorológica y realizar conversiones monetarias. Además, incorpora mecanismos de autenticación, validación de datos, gestión de errores y tolerancia a fallos para mejorar la confiabilidad de la aplicación.

---

## 📌 Estado actual del proyecto

El proyecto se encuentra en una etapa avanzada de desarrollo, con sus principales módulos funcionales y algunas áreas pendientes de completar y consolidar.

| Indicador | Avance estimado |
|---|---:|
| Desarrollo técnico | **92%** |
| Desarrollo funcional | **90%** |
| Seguridad y resiliencia de APIs | **95%** |

### Avance por módulo

| Módulo | Avance | Estado |
|---|---:|---|
| Arquitectura MVC + DAO | 95% | Implementado |
| Configuración y entorno (`.env`) | 95% | Implementado |
| Usuarios y autenticación | 95% | Implementado |
| Integración API del clima | 95% | Implementado |
| Integración API monetaria | 95% | Implementado |
| Proyectos y transacciones internacionales | 92% | Implementado |
| Seguridad, sanitización y manejo de errores | 92% | Implementado |
| Base de datos SQLite y DAOs | 90% | Implementado |
| Modelos y validaciones | 90% | Implementado |
| Gestión de empleados y departamentos | 85% | Implementado |
| Control de tiempos | 80% | Funcional |
| Documentación técnica | 95% | En consolidación |
| Informes | 20% | Estructura base |

*Los porcentajes representan estimaciones del avance de desarrollo y no constituyen resultados de pruebas de cobertura automatizada.*

---

## 🚀 Funcionalidades del sistema

### 1. Gestión administrativa y de recursos humanos

- Inicio de sesión obligatorio.
- Administración de usuarios según roles:
  - Administrador.
  - Empleado.
- Creación inicial del usuario administrador cuando no existen usuarios registrados.
- Gestión de empleados.
- Gestión de departamentos.
- Administración de proyectos.
- Control de estados de proyectos:
  - `Pendiente`.
  - `En proceso`.
  - `Finalizado`.
- Registro y consulta de horas trabajadas por empleado y proyecto.
- Administración de usuarios por parte del administrador:
  - Registrar usuarios.
  - Listar usuarios.
  - Eliminar usuarios.
  - Protección contra la eliminación del usuario con sesión activa.

### 2. Planificación operativa mediante integración climática

El sistema incorpora un servicio de consulta meteorológica que permite evaluar las condiciones ambientales de las ciudades donde se desarrollan los proyectos.

**Tecnología:** `WeatherAPI`.

Funcionalidades:

- Consulta del clima actual.
- Consulta del pronóstico meteorológico de uno a tres días.
- Identificación de temperatura y sensación térmica.
- Consulta de humedad, velocidad del viento y precipitaciones.
- Evaluación de viabilidad operativa.
- Generación de recomendaciones y alertas preventivas.
- Prueba de conectividad con el servicio externo.

El método `evaluar_viabilidad_operativa()` analiza las variables meteorológicas y clasifica las condiciones de trabajo en tres categorías:

- `ÓPTIMO`: condiciones favorables para desarrollar actividades.
- `PRECAUCIÓN`: condiciones que requieren medidas preventivas.
- `RIESGO ALTO`: condiciones que pueden comprometer la ejecución de las actividades.

### 3. Gestión financiera y pagos internacionales

Para facilitar la administración de proyectos desarrollados en diferentes países, se implementó un servicio de identificación y conversión monetaria.

**APIs integradas:**

1. **REST Countries:** identifica el país y su moneda oficial mediante códigos ISO.
2. **Frankfurter:** obtiene tasas de conversión entre el peso chileno (`CLP`) y la moneda de destino.

Funcionalidades:

- Identificación de la moneda correspondiente al país del proyecto.
- Reconocimiento de nombres de países en español e inglés.
- Obtención de tasas de conversión monetaria.
- Conversión de montos desde CLP hacia la moneda de destino.
- Cálculo de pagos para empleados asignados a proyectos.
- Registro de operaciones mediante `Transaccion` y `TransaccionDAO`.
- Generación de reportes consolidados de pagos por proyecto.

Los cálculos monetarios utilizan `decimal.Decimal` y redondeo financiero `ROUND_HALF_UP` para evitar los problemas de precisión asociados a los números de punto flotante.

Las conversiones no disponibles se informan como tales y no deben generar transacciones incompletas.

---

## 🏗️ Arquitectura del proyecto

El repositorio utiliza una separación por responsabilidades basada en los patrones **MVC (Modelo-Vista-Controlador)** y **DAO (Data Access Object)**.

Esta organización permite mantener desacopladas las reglas de negocio, la interacción con el usuario, el acceso a la base de datos y las integraciones externas.

### Estructura general

```text
EcoTech-Solutions/
│
├── main.py
│
├── controllers/
│   ├── main_controller.py
│   ├── auth_controller.py
│   ├── empleado_controller.py
│   ├── departamento_controller.py
│   ├── proyecto_controller.py
│   └── ...
│
├── views/
│   ├── main_view.py
│   ├── empleado_view.py
│   ├── departamento_view.py
│   ├── proyecto_view.py
│   └── ...
│
├── models/
│   ├── usuario.py
│   ├── usuario_dao.py
│   ├── empleado.py
│   ├── empleado_dao.py
│   ├── proyecto.py
│   ├── proyecto_dao.py
│   └── ...
│
├── services/
│   ├── clima_service.py
│   └── moneda_service.py
│
├── config/
│   ├── database.py
│   └── settings.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

*La estructura representa la organización general del repositorio; los archivos y módulos pueden variar según la versión actual del proyecto.*

### Responsabilidades de cada capa

| Componente | Responsabilidad |
|---|---|
| `Controllers` | Coordinar el flujo de ejecución y aplicar las reglas de interacción. |
| `Views` | Presentar menús, formularios y resultados en consola. |
| `Models` | Representar las entidades del sistema y sus validaciones. |
| `DAOs` | Gestionar las operaciones CRUD y las consultas SQL. |
| `Services` | Encapsular la comunicación con APIs externas y procesar sus respuestas. |
| `Config` | Centralizar configuraciones y gestionar la conexión e inicialización de SQLite. |

---

## 🔌 Integración de servicios externos mediante APIs

Uno de los principales componentes técnicos del proyecto es la incorporación de servicios externos para ampliar las capacidades de la aplicación.

### 3.1.1 Consumo de servicios externos

Se implementaron mecanismos para realizar solicitudes HTTP y procesar respuestas JSON de forma estructurada.

**Gestión de solicitudes:**

- Utilización de `requests.Session()` para reutilizar conexiones HTTP.
- Configuración de encabezados `Accept: application/json` y `User-Agent`.
- Definición de tiempos máximos de espera mediante `Settings.REQUEST_TIMEOUT`.
- Reintentos automáticos mediante `HTTPAdapter` y `Retry` ante determinados errores transitorios.
- Manejo de respuestas HTTP y validación de estructuras JSON.
- Protección de la importación de dependencias opcionales.

**Optimización de consultas:**

- Uso del parámetro `fields` en REST Countries para solicitar únicamente los campos necesarios.
- Selección de información meteorológica relevante desde WeatherAPI.
- Implementación de cachés en memoria para evitar consultas monetarias repetidas.
- Resolución de la moneda del país una sola vez por proyecto, evitando solicitudes redundantes por empleado.

**Consistencia de datos:**

- Transformación de las respuestas externas en estructuras internas independientes de las APIs.
- Validación de tasas y montos antes de realizar operaciones financieras.
- Uso de aritmética decimal para los cálculos monetarios.
- Separación entre la lógica de consumo HTTP y los controladores de la aplicación.

### 3.1.2 Seguridad y control de acceso

Se incorporaron medidas para proteger el acceso a la aplicación y validar los datos ingresados por los usuarios.

**Autenticación:**

- Inicio de sesión obligatorio antes de acceder al menú principal.
- Gestión de roles `Administrador` y `Empleado`.
- Contraseñas ocultas durante el ingreso mediante `pwinput`.
- Generación de hashes SHA-256 mediante `hashlib`.
- Comparación de hashes mediante `hmac.compare_digest`.
- Límite de intentos de inicio de sesión mediante `MAX_LOGIN_ATTEMPTS`.

**Validación y sanitización:**

- Validación de tipos, longitudes y formatos.
- Uso de expresiones regulares Unicode para validar entradas.
- Sanitización de nombres de ciudades y países.
- Codificación de parámetros de ruta mediante `urllib.parse.quote`.
- Consultas SQL parametrizadas para reducir el riesgo de inyección SQL.

**Configuración y protección de información sensible:**

- Centralización de configuraciones en `config/settings.py`.
- Uso de variables de entorno mediante `.env`.
- Separación de credenciales y API Keys del código fuente.
- Exclusión del archivo `.env` mediante `.gitignore`.
- Disponibilidad de `.env.example` como referencia de configuración.

> Nota de seguridad: SHA-256 permite generar hashes de contraseñas, pero no es una función especializada para almacenarlas. Para un despliegue real se recomienda migrar a algoritmos específicos para contraseñas, como Argon2id, scrypt o bcrypt, con salt individual.

### 3.1.3 Manejo de errores y resiliencia operativa

Se incorporaron mecanismos para evitar que los problemas de conectividad o las respuestas inesperadas de los servicios externos interrumpan abruptamente la aplicación.

**Manejo de excepciones:**

- `ValueError`: parámetros o datos inválidos.
- `Timeout`: tiempo de espera agotado.
- `ConnectionError`: problemas de conectividad.
- `RequestException`: errores asociados