### Avance general

| Indicador | Estado |
|---|---:|
| Avance técnico | **62%** |
| Avance funcional | **55%** |
| Pruebas automatizadas | **0%** |
| Estado del proyecto | 🟡 En desarrollo activo |

### Avance por módulo

| Módulo | Avance | Estado |
|---|---:|:---:|
| Estructura MVC/DAO | 85% | 🟢 Avanzado |
| Configuración | 75% | 🟢 En progreso |
| Base de datos | 78% | 🟢 En progreso |
| Modelos de dominio | 68% | 🟡 Parcial |
| Usuarios y autenticación | 72% | 🟢 En progreso |
| Gestión de empleados | 70% | 🟢 En progreso |
| Gestión de departamentos | 65% | 🟢 En progreso |
| Gestión de proyectos | 50% | 🟡 Parcial |
| Control de tiempos | 50% | 🟡 Parcial |
| Informes | 15% | 🔴 Inicial |
| API del clima | 80% | 🟢 Avanzado |
| API de moneda | 0% | 🔴 Pendiente |
| Validaciones | 58% | 🟡 En progreso |
| Seguridad | 45% | 🟡 Parcial |
| Pruebas automatizadas | 0% | 🔴 Pendiente |
| Documentación | 55% | 🟡 En progreso |

### Mejoras recientes

- [x] Búsqueda de empleados por RUT.
- [x] Edición y visualización de empleados.
- [x] Eliminación lógica de empleados.
- [x] Eliminación del usuario asociado.
- [x] Reactivación de empleados existentes.
- [x] Asociación entre empleados y departamentos.
- [x] Búsqueda de empleados por departamento.
- [x] Conteo de empleados por departamento.
- [x] CRUD inicial de departamentos.
- [x] Búsqueda de departamentos por nombre.
- [x] Búsqueda de departamentos por gerente.
- [x] Integración con WeatherAPI.
- [x] Procesamiento de respuestas JSON.
- [x] Manejo de errores HTTP y modo contingencia.

### Pendientes prioritarios

- [ ] Evitar duplicación de usuarios al recontratar.
- [ ] Completar edición de departamentos.
- [ ] Validar RUT, sueldo, correo, teléfono y fechas.
- [ ] Corregir completamente el CRUD de proyectos.
- [ ] Completar búsquedas de tiempos por fecha y rango.
- [ ] Implementar informes.
- [ ] Implementar el servicio de moneda.
- [ ] Migrar SHA-256 a bcrypt o Argon2.
- [ ] Crear pruebas automatizadas con pytest.
- [ ] Agregar integración continua con GitHub Actions.

### Evaluación actual

> El proyecto muestra una mejora real en los módulos de empleados y departamentos.  
> La estructura general está bien encaminada, pero los módulos de proyectos, tiempos, informes y servicios todavía necesitan integración y pruebas para considerarse terminados.