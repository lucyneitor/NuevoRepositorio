## Progreso estimado

Estimación basada en revisión del código y ejecución de modelos y DAOs sobre una
base temporal (revisión del 11-11-2026). Mide **funcionamiento comprobado**, no solo
código escrito.

| Módulo | Avance | Estado |
|---|---:|---|
| Estructura general | 🟢 75% | Capas definidas; `main.py` ignora fallos de `init_db()`; archivos vacíos y restos de otro proyecto |
| Base de datos | 🟡 60% | Esquema sólido, pero `init_db()` falla (`CHECK (salario > 0)`, la columna es `sueldo`) |
| Autenticación y usuarios | 🟡 60% | Login y hash verificados; no se pueden crear usuarios "Empleado" (`rut_empleado` no se guarda); opción 6 sin control de rol; SHA-256 sin sal |
| Empleados | 🔴 25% | DAO usa columnas inexistentes (`user`, `password`, `rol_admin`); controller llama métodos que no existen |
| Departamentos | 🔴 35% | DAO correcto; el modelo exige lista de empleados y el controller tiene métodos inexistentes |
| Tiempos | 🟡 45% | Modelo y consultas de lectura verificados; `agregar_tiempo`, controller y vistas rotos |
| Proyectos | 🔴 35% | Lecturas funcionan; modelo sin `id_proyecto`, `estado` no se guarda, controller y vistas con errores |
| Informes | 🔴 15% | Solo menú; 1 de 3 consultas funciona |
| Servicios externos | 🔴 30% | `ClimaService` listo pero sin usar; `moneda_service.py` vacío; `.env.example` desalineado |
| Integración y pruebas | 🔴 5% | Sin tests; solo el login funciona de punta a punta |

**Avance global ponderado: 41%.**
**Funcionamiento integrado comprobado: no. La aplicación no inicializa la base de datos.**

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
