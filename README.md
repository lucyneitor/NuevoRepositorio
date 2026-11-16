# Sistema de Gestión EcoTech

Aplicación de consola desarrollada en Python para gestionar empleados,
departamentos, proyectos, registros de tiempo, usuarios e informes.

Utiliza arquitectura MVC + DAO y persistencia mediante SQLite.

## Estado del proyecto

| Indicador | Avance |
|---|---:|
| Avance técnico | **79%** |
| Avance funcional | **74%** |
| Pruebas automatizadas | **0%** |

## Avance por módulo

| Módulo | Avance | Estado |
|---|---:|---|
| Arquitectura MVC + DAO | 90% | Avanzado |
| Configuración y entorno | 90% | Avanzado |
| Base de datos SQLite | 88% | Avanzado |
| Modelos de dominio | 86% | Avanzado |
| Usuarios y autenticación | 85% | Casi terminado |
| Proyectos | 85% | Casi terminado |
| API del clima | 85% | Casi terminado |
| Departamentos | 82% | Avanzado |
| Validaciones | 82% | En progreso |
| Empleados | 80% | Avanzado |
| Documentación | 80% | En progreso |
| Control de tiempos | 70% | En progreso |
| Seguridad | 58% | Parcial |
| Informes | 15% | Inicial |
| API de moneda | 0% | Pendiente |
| Pruebas automatizadas | 0% | Pendiente |

## Funcionalidades implementadas

- Inicio de sesión y gestión de usuarios.
- Gestión de empleados.
- Gestión de departamentos.
- Gestión de proyectos.
- Registro y actualización de tiempos.
- Búsqueda de tiempos por:
  - ID.
  - RUT del empleado.
  - Proyecto.
  - Fecha.
  - Intervalo de fechas.
- Validación de fechas y horas.
- Cálculo de horas trabajadas descontando pausas.
- Persistencia con SQLite.
- Consulta de estado de proyectos.
- Integración con servicio del clima.

## Pendientes principales

- [ ] Completar el listado por rango de fechas.
- [ ] Corregir funciones pendientes de `TiempoView`.
- [ ] Completar resúmenes de registros de tiempo.
- [ ] Implementar el módulo de informes.
- [ ] Implementar el servicio de moneda.
- [ ] Agregar pruebas automatizadas con `pytest`.
- [ ] Mejorar el hashing de contraseñas con bcrypt o Argon2.
- [ ] Completar documentación de instalación y uso.

## Aplicación de IA en el repositorio
explicacion pendiente
## Tecnologías

- Python
- SQLite
- Pydantic
- Requests
- python-dotenv
- pwinput

## Ejecución

1. Clonar el repositorio.
2. Crear un entorno virtual.
3. Instalar dependencias:

```bash
pip install -r requirements.txt