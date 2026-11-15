# Sistema de gestión EcoTech

## Avance actual del proyecto

| Indicador | Avance |
|---|---:|
| Avance técnico general | **73%** |
| Avance funcional general | **67%** |
| Pruebas automatizadas | **0%** |

## Avance por módulo

| Módulo | Avance | Estado |
|---|---:|---|
| Estructura MVC y DAO | 85% 🟢 | Avanzado 📎 |
| Configuración | 75% 🟢 | En progreso 👩🏻‍💻 |
| Base de datos | 82% 🟢 | En progreso 👩🏻‍💻 |
| Modelos | 82% 🟢 | En progreso 👩🏻‍💻 |
| Usuarios y autenticación 🛡️ | 72% 🟢 | En progreso 👩🏻‍💻 |
| Empleados | 70% 🟢 | En progreso 👩🏻‍💻 |
| Departamentos | 70% 🟢 | En progreso 👩🏻‍💻 |
| Proyectos | 82% 🟢 | Casi terminado 📎 |
| Control de tiempos | 60% 🟢 | En progreso 👩🏻‍💻 |
| Informes | 15% 🔴 | Inicial ⛈️ |
| API del clima | 80% 🟢 | Avanzado |
| API de moneda | 0% 🔴 | Pendiente 🏴‍☠️ |
| Validaciones | 70% 🟢 | En progreso 👩🏻‍💻 |
| Seguridad | 45% 🔴 | Parcial📌 |
| Pruebas automatizadas | 0% | Pendiente 📉|
| Documentación | 70% 🟢 | En progreso 👩🏻‍💻 |

## ✨Avances recientes en el módulo de tiempos✨

- Se corrigió la consulta común del DAO.
- Se corrigió el orden de columnas y valores del `INSERT`.
- Se corrigió el orden de valores del `UPDATE`.
- Se agregó la hora de entrada al crear registros.
- Se corrigió la actualización de la hora de entrada.
- Se validan empleados y proyectos antes de insertar.
- Se agregó el conteo de empleados por proyecto.
- Se agregó una función para acumular horas por trabajador.
- Se incorporaron búsquedas por ID, RUT, proyecto y fechas.
- Se agregó la consulta del estado del proyecto.

## 📍Pendientes inmediatos del módulo de tiempos

- [ ] Agregar la propiedad `tiempo_trabajado` al modelo `Tiempo`.
- [ ] Corregir la suma de horas por proyecto.
- [ ] Separar la suma por trabajador de la suma por proyecto.
- [ ] Corregir la cantidad de argumentos entre controlador y vista.
- [ ] Agregar `self` a las funciones de vista que lo necesitan.
- [ ] Eliminar las variables inexistentes `negativo` y `proyecto`.
- [ ] Completar los argumentos de `mostrar_registros_por_fecha()`.
- [ ] Completar el listado por rango de fechas.
- [ ] Validar fecha, horas y minutos de pausa desde el formulario.
- [ ] Probar crear, buscar, listar y actualizar registros.
- [ ] Agregar opción para eliminar registros si el requisito lo contempla.

## 📎Pendientes generales

- [ ] Implementar el módulo de informes.
- [ ] Implementar `moneda_service.py`.
- [ ] Crear pruebas automatizadas con `pytest`.
- [ ] Mejorar el almacenamiento de contraseñas usando bcrypt o Argon2.
- [ ] Revisar transacciones y manejo de errores en los DAO.
- [ ] Actualizar la documentación de instalación y ejecución.

## Próximo orden recomendado

1. Resolver `tiempo_trabajado` y las sumas acumuladas.
2. Corregir la integración entre controlador y vista.
3. Completar los filtros por fecha y rango.
4. Probar el flujo completo de tiempos.
5. Implementar informes.
6. Agregar pruebas automatizadas.
7. Completar moneda y mejorar seguridad.