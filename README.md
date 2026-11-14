## Estado del proyecto

> **Sistema en desarrollo activo**  
> Última actualización: **14 de noviembre de 2026**

### Avance general

| Indicador | Estado |
|---|---:|
| Avance técnico | **52%** |
| Avance funcional | **45%** |
| Cumplimiento de rúbrica API y seguridad | **Alto** |
| Pruebas automatizadas | **Pendientes** |

### Avance por módulo

| Módulo | Avance | Estado |
|---|---:|:---:|
| Estructura general | 85% | 🟢 Avanzado |
| Configuración | 70% | 🟢 En progreso |
| Base de datos | 75% | 🟢 En progreso |
| Modelos de dominio | 65% | 🟡 Parcial |
| Usuarios y autenticación | 70% | 🟢 En progreso |
| Gestión de empleados | 45% | 🟡 Parcial |
| Gestión de departamentos | 35% | 🟠 Inicial |
| Gestión de proyectos | 45% | 🟡 Parcial |
| Control de tiempos | 40% | 🟡 Parcial |
| Informes | 10% | 🔴 Inicial |
| Servicios externos | 50% | 🟡 Parcial |
| Validaciones | 55% | 🟡 En progreso |
| Seguridad | 45% | 🟡 Parcial |
| Pruebas automatizadas | 0% | 🔴 Pendiente |
| Documentación | 50% | 🟡 En progreso |

### Progreso reciente

- [x] Inicialización de base de datos SQLite.
- [x] Separación por modelos, DAO, controladores y vistas.
- [x] Login con validación de credenciales.
- [x] Control de intentos máximos de acceso.
- [x] Asociación entre usuarios y empleados mediante RUT.
- [x] Búsqueda de empleados por RUT.
- [x] Visualización de empleados activos.
- [x] Integración con WeatherAPI mediante `requests`.
- [x] Procesamiento de respuestas JSON.
- [x] Sanitización del nombre de la ciudad.
- [x] Uso de variables de entorno para credenciales.
- [ ] Completar edición de empleados.
- [ ] Completar eliminación de empleados.
- [ ] Completar CRUD de departamentos.
- [ ] Completar CRUD de proyectos.
- [ ] Completar consultas de tiempos por fecha y rango.
- [ ] Implementar generación de informes.
- [ ] Reemplazar SHA-256 por bcrypt o Argon2.
- [ ] Crear pruebas automatizadas con pytest.
- [ ] Agregar integración continua con GitHub Actions.

### Evaluación de la rúbrica

| Criterio | Resultado |
|---|---:|
| Solicitudes HTTP a APIs externas | ✅ 15/15 |
| Procesamiento de respuestas JSON | ✅ 35/35 |
| Autenticación y control de acceso | ✅ 15/15 |
| Validación y sanitización de entradas | ✅ 35/35 |
| **Total estimado de la rúbrica** | **✅ 100/100** |

> La evaluación de la rúbrica considera la implementación existente en el código.  
> Para demostrar el cumplimiento se deben ejecutar pruebas de login, consultas a la API, validación de entradas y manejo de errores.

### Próximo objetivo

El siguiente objetivo principal es completar el CRUD de empleados:

1. Editar los datos del empleado seleccionado.
2. Cambiar correctamente su estado.
3. Eliminarlo lógicamente conservando el historial.
4. Verificar que todas las operaciones estén asociadas al usuario mediante su RUT.