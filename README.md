## Avance actual del proyecto

| Indicador | Avance |
|---|---:|
| Avance técnico general | **70%** |
| Avance funcional general | **64%** |
| Pruebas automatizadas | **0%** |

### Avance por módulo

| Módulo | Avance | Estado |
|---|---:|---|
| Estructura MVC y DAO | 85% | Avanzado |
| Configuración | 75% | En progreso |
| Base de datos | 80% | En progreso |
| Modelos | 78% | En progreso |
| Usuarios y autenticación | 72% | En progreso |
| Empleados | 70% | En progreso |
| Departamentos | 70% | En progreso |
| Proyectos | **82%** | Casi terminado |
| Control de tiempos | 45% | Parcial |
| Informes | 15% | Inicial |
| API del clima | 80% | Avanzado |
| API de moneda | 0% | Pendiente |
| Validaciones | 68% | En progreso |
| Seguridad | 45% | Parcial |
| Pruebas automatizadas | 0% | Pendiente |
| Documentación | 65% | En progreso |

### Pendientes inmediatos

- [ ] Eliminar el `else` duplicado en `modificar_proyecto()`.
- [ ] Probar edición de nombre, descripción, fecha de inicio y fecha de término.
- [ ] Probar fechas ingresadas como `DD-MM-YYYY`.
- [ ] Confirmar que SQLite guarde las fechas como `YYYY-MM-DD`.
- [ ] Manejar cuando `obtener_id_por_nombre()` devuelva `None`.
- [ ] Completar el módulo de control de tiempos.
- [ ] Implementar el módulo de informes.
- [ ] Implementar `moneda_service.py`.
- [ ] Crear pruebas automatizadas con `pytest`.
- [ ] Mejorar el almacenamiento de contraseñas usando bcrypt o Argon2.
- [ ] Revisar transacciones y manejo de errores en los DAO.

### Próximo orden recomendado

1. Finalizar y probar proyectos.
2. Completar control de tiempos.
3. Implementar informes.
4. Agregar pruebas automatizadas.
5. Completar moneda y mejorar seguridad.