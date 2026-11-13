## Progreso estimado

Estimación basada en revisión del código y ejecución de modelos y DAOs sobre una
base temporal (revisión del 13-11-2026). Mide **funcionamiento comprobado**, no solo
código escrito.

| Módulo | Avance | Cambio |
|---|---:|---|
| Estructura general | 🟢 80% | ▲ +2: `.env.example` documenta `ADMIN_*`; código muerto eliminado |
| Base de datos | 🟢 85% | = |
| Autenticación y usuarios | 🟡 58% | ▼ −2: guarda `rut_empleado`, pero `registrar_usuario` falla en todos los roles |
| Empleados | 🔴 38% | ▲ +3: nuevas vistas y métodos; DAO de insertar/leer sigue desalineado |
| Departamentos | 🟡 50% | ▲ +12: modelo y DAO corregidos; falta `formulario_departamento`, editar y buscar |
| Tiempos | 🟡 46% | ▲ +1: menú con validador correcto |
| Proyectos | 🔴 35% | = |
| Informes | 🔴 15% | = |
| Servicios externos | 🔴 30% | = |
| Integración y pruebas | 🔴 8% | = |

**Avance global ponderado: 49%** (anterior 47%).

## Próximas tareas recomendadas

### Prioridad 1: que la aplicación arranque
- Corregir `CHECK (salario > 0)` por `sueldo` en `config/database.py` y detener `main.py` si `init_db()` falla.
- Quitar `@staticmethod` o `self` en `TiempoDAO.agregar_tiempo`.
- Reemplazar `Tiempo.tiempo_trabajado` e `id_empleado` por `duracion_trabajada` y `rut_empleado` (modelo, vistas y controller).

### Prioridad 2: alinear DAOs con el esquema
- `EmpleadoDAO`: eliminar `user`, `password` y `rol_admin`; separar insertar de convertir fila a objeto.
- `Departamento`: `empleados` con valor por defecto `[]` y orden de argumentos coherente en el DAO.
- `Proyecto`: agregar `id_proyecto`, guardar `estado` en INSERT y UPDATE, y decidir si el DAO devuelve objetos o `Row`.

### Prioridad 3: seguridad y usuarios
- Restringir la gestión de usuarios (opción 6) al rol Administrador.
- Guardar y leer `rut_empleado` en `UsuarioDAO`; distinguir `CHECK` de `UNIQUE` en los mensajes de error.
- Reemplazar SHA-256 sin sal por PBKDF2, bcrypt o argon2.
- Quitar la contraseña por defecto del banner y definir el flujo del administrador inicial.

### Prioridad 4: completar controllers y vistas
- Implementar los métodos faltantes (buscar, eliminar y mostrar empleados y departamentos, listar por rango de fechas).
- Alinear los validadores de menú con las opciones mostradas.
- Corregir las vistas sin `self` y las variables no definidas.

### Prioridad 5: informes, servicios y pruebas
- Implementar los informes y corregir las consultas de `InformeDAO`.
- Integrar o retirar `ClimaService` y `moneda_service.py`, y actualizar `.env.example`.
- Agregar tests con pytest sobre una base temporal y registrar los resultados aquí.
