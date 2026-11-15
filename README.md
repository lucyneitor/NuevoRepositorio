# Sistema de Gestión EcoTech

Aplicación de consola en Python con arquitectura **MVC + DAO** y persistencia en **SQLite**, orientada a la gestión de empleados, departamentos, proyectos, control de tiempos, informes y servicios externos.

## Avance actual del proyecto

| Indicador | Avance |
|---|---:|
| Avance técnico general | **76%** |
| Avance funcional general | **71%** |
| Pruebas automatizadas | **0%** |

## Avance por módulo

| Módulo | Avance | Estado |
|---|---:|---|
| Estructura MVC y DAO | 90% 🟢 | Avanzado |
| Configuración y entorno | 90% 🟢 | Avanzado |
| Base de datos SQLite | 88% 🟢 | Avanzado |
| Usuarios y autenticación 🛡️ | 85% 🟢 | Casi terminado |
| Proyectos | 85% 🟢 | Casi terminado |
| API del clima | 85% 🟢 | Casi terminado |
| Departamentos | 82% 🟢 | Avanzado |
| Modelos de dominio | 82% 🟢 | Avanzado |
| Empleados | 80% 🟢 | Avanzado |
| Documentación | 80% 🟢 | En progreso |
| Validaciones | 75% 🟢 | En progreso |
| Control de tiempos | 62% 🟡 | En progreso |
| Seguridad | 58% 🟡 | Parcial |
| Informes | 15% 🔴 | Inicial |
| API de moneda | 0% 🔴 | Pendiente |
| Pruebas automatizadas | 0% 🔴 | Pendiente |

## ✨ Avances recientes

- **Autenticación y sesiones:** Se reemplazó la llamada recursiva al cerrar sesión por un ciclo exterior de autenticación en `MainController` y se activó el bloqueo para impedir que un administrador elimine su propia sesión activa.
- **Protección de integridad:** Se corrigió `AuthController.eliminar_usuario()` para administradores sin ficha de empleado asociada (`rut_empleado = None`) y `DepartamentoController` para listar empleados que aún no tienen cuenta de usuario.
- **Empleados y configuración:** Se corrigió la conversión de sueldo a entero en el registro de empleados y se incorporaron `.env.example` y `.gitignore` al repositorio.
- **Módulo de tiempos:** Se corrigió la búsqueda por fecha única e intervalo de fechas en `TiempoController`, además de los métodos de inserción, actualización y conteo en `TiempoDAO`.

## 📍 Pendientes inmediatos del módulo de tiempos

- [ ] Agregar la propiedad `tiempo_trabajado` (en horas) en `models/tiempo.py` a partir de `duracion_trabajada`.
- [ ] Agregar el parámetro `self` a los métodos de `TiempoView` (`mostrar_registros_empleado`, `mostrar_registros_proyecto` y `mostrar_registros_esp_pro_em`).
- [ ] Corregir la firma y las variables indefinidas (`negativo`, `proyecto`) en `TiempoView.mostrar_registros_proyecto()`.
- [ ] Completar los argumentos enviados a `TiempoView.mostrar_registros_por_fecha()` desde `TiempoController`.
- [ ] Implementar la visualización del listado en `TiempoController.listar_registros_rango_fecha()`.
- [ ] Validar formato de fecha, horas y minutos de pausa en `TiempoView.formulario_tiempo()`.
- [ ] Probar flujo completo de creación, listado, búsqueda y actualización con los datos semilla de `database.py`.

## 📎 Pendientes generales

- [ ] Cambiar `break` por `return` en la opción `0` de `MainController.ejecutar()` para cerrar la aplicación directamente.
- [ ] Implementar las opciones 1 a 5 en `InformeController` y corregir las consultas SQL de `InformeDAO` (`t.rut_empleado` y columnas reales de `departamento`).
- [ ] Implementar `services/moneda_service.py` y conectar los servicios de clima y moneda al menú.
- [ ] Crear suite de pruebas automatizadas con `pytest`.
- [ ] Evaluar migración de hashing de contraseñas a `bcrypt` o `argon2` y mejorar la autorización en `confirmar()`.

## Próximo orden recomendado

1. Completar `tiempo_trabajado` en `Tiempo` y corregir las firmas/variables de `TiempoView`.
2. Ejecutar pruebas manuales de tiempos usando los registros semilla en `Database.init_db()`.
3. Implementar `InformeController` y ajustar `InformeDAO`.
4. Desarrollar `moneda_service.py` e integrar las APIs al flujo de usuario.
5. Agregar pruebas automatizadas con `pytest` y reforzar seguridad.