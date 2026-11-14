### Avance general

| Indicador | Estado |
|---|---:|
| Avance técnico | **66%** |
| Avance funcional | **59%** |
| Pruebas automatizadas | **0%** |
| Estado del proyecto | 🟡 En desarrollo activo |

### Avance por módulo

| Módulo | Avance | Estado |
|---|---:|:---:|
| Estructura MVC/DAO | 85% | 🟢 Avanzado |
| Configuración | 75% | 🟢 En progreso |
| Base de datos | 80% | 🟢 En progreso |
| Modelos de dominio | 72% | 🟢 En progreso |
| Usuarios y autenticación | 72% | 🟢 En progreso |
| Gestión de empleados | 70% | 🟢 En progreso |
| Gestión de departamentos | 70% | 🟢 En progreso |
| Gestión de proyectos | 62% | 🟡 Parcial |
| Control de tiempos | 45% | 🟡 Parcial |
| Informes | 15% | 🔴 Inicial |
| API del clima | 80% | 🟢 Avanzado |
| API de moneda | 0% | 🔴 Pendiente |
| Validaciones | 60% | 🟡 En progreso |
| Seguridad | 45% | 🟡 Parcial |
| Pruebas automatizadas | 0% | 🔴 Pendiente |
| Documentación | 65% | 🟡 En progreso |

### Mejoras recientes

- [x] Crear proyectos.
- [x] Buscar proyectos por nombre.
- [x] Mostrar todos los proyectos.
- [x] Mostrar campos específicos de proyectos.
- [x] Convertir filas SQLite a objetos `Proyecto`.
- [x] Eliminar proyectos mediante su ID.
- [x] Validar fechas al crear proyectos.
- [x] Buscar empleados por RUT.
- [x] Gestionar empleados por departamento.
- [x] Crear, editar y eliminar departamentos.
- [x] Integrar WeatherAPI con procesamiento JSON.

### Pendientes prioritarios

- [ ] Unificar formatos de fecha al editar proyectos.
- [ ] Permitir crear `Proyecto` sin ID inicial.
- [ ] Actualizar automáticamente el estado al modificar fechas.
- [ ] Eliminar código repetido en `ProyectoView`.
- [ ] Completar el módulo de control de tiempos.
- [ ] Implementar informes.
- [ ] Implementar el servicio de moneda.
- [ ] Completar validaciones de formularios.
- [ ] Migrar SHA-256 a bcrypt o Argon2.
- [ ] Crear pruebas automatizadas con pytest.
- [ ] Agregar integración continua con GitHub Actions.

### Evaluación actual

> El proyecto muestra una mejora sostenida en empleados, departamentos y proyectos.  
> El siguiente gran objetivo es estabilizar la edición de proyectos y completar el módulo de tiempos antes de aumentar nuevamente el porcentaje general.