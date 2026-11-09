# NuevoRepositorio

Sistema de gestión para control de recursos, tiempos y reportes de personal.

---

## 📊 Estado del Proyecto
# Sistema de gestión de personal

Aplicación de consola en Python para administrar empleados, departamentos, proyectos, registros de tiempo, usuarios e informes. Utiliza SQLite como base de datos.

> **Estado actual:** proyecto en desarrollo. La estructura y varias operaciones están implementadas, pero quedan tareas de integración y pruebas antes de considerar estable el sistema.

## Progreso estimado

Estimación basada en una revisión estática del código. No equivale a una ejecución o aprobación de pruebas.

| Módulo | Avance estimado | Estado |
|---|---:|---|
| Estructura general | ✅ 85% | Capas y archivos principales creados |
| Base de datos | ✅ 70% | Esquema SQLite definido; falta alinearlo con todos los DAO |
| Autenticación y usuarios | ✅ 55% | Login implementado; falta integrar roles y relación con empleado |
| Empleados | ✅65% | Modelo y operaciones principales; requiere verificación con el esquema actual |
| Departamentos | ✅65% | Implementación parcial; falta probar el CRUD completo |
| Tiempos | ✅ 45% | DAO y menú parcialmente implementados; quedan métodos por corregir |
| Proyectos | ✅55% | CRUD parcial; revisar integración con tiempos |
| Informes | ✅ 30% | Consultas y flujo todavía incompletos |
| Integración y pruebas | ✅40% | Falta comprobar los flujos completos |

**Avance global estimado: 60–65%.**  
**Funcionamiento integrado comprobado: pendiente de verificar.**

## Arquitectura

- `config/`: configuración, base de datos y ajustes.
- `controllers/`: coordinación de los flujos de la aplicación.
- `models/`: entidades y acceso a datos (DAO).
- `views/`: menús, formularios y salida por consola.
- `services/`: servicios auxiliares.
- `main.py`: punto de entrada.

## Diseño de datos

La intención actual es usar `empleado.rut` como clave primaria del empleado. La tabla `tiempo` lo referencia mediante `rut_empleado`; la tabla `usuario` también contempla una relación con el RUT del empleado.

Es importante mantener esos nombres y relaciones consistentes en el esquema, los modelos y las consultas DAO. En particular, revisar cualquier consulta que aún use `id_empleado` como columna numérica.

## Requisitos y ejecución

Se recomienda Python 3.10 o superior.

Crear y activar un entorno virtual:

```bash
# Windows PowerShell
py -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Configurar las variables de entorno usando `.env.example` como referencia, si corresponde. No subir contraseñas ni secretos al repositorio.

Ejecutar:

```bash
py main.py
```

En macOS/Linux también puede usarse:

```bash
python3 main.py
```

La base SQLite se inicializa desde la configuración de la aplicación. **El esquema creado con `CREATE TABLE IF NOT EXISTS` no se actualiza automáticamente** si ya existía una base de datos anterior. Antes de recrearla o migrarla, hacer una copia de seguridad de `sistema_gestion.db`.

## Próximas tareas recomendadas

### Prioridad 1: que la aplicación arranque

- Ejecutar `py main.py` y resolver cualquier error de sintaxis o importación.
- Quitar `@staticmethod` de los métodos de `TiempoController` que usan `self`.
- Completar los métodos pendientes de listar por fecha e intervalo.

### Prioridad 2: alinear autenticación y datos

- Hacer que los roles ofrecidos por la vista coincidan con los permitidos por el modelo `Usuario`.
- Alinear `usuario.rut_empleado` entre el esquema, `Usuario`, `UsuarioDAO` y el registro de usuarios.
- Decidir cómo se crea el administrador inicial si la tabla exige un RUT de empleado.
- No asumir que cambiar el esquema actualiza una base SQLite ya existente.

### Prioridad 3: unificar la clave del empleado

- Confirmar que `empleado.rut` sea la clave primaria en la base de datos.
- Cambiar las consultas y operaciones de tiempo para guardar y buscar `rut_empleado`.
- Revisar informes y cualquier otro DAO que todavía use `id_empleado`.

### Prioridad 4: probar flujos completos

- Crear empleado y departamento.
- Iniciar sesión con un usuario válido.
- Crear proyecto.
- Registrar tiempo asociado al RUT y al proyecto.
- Consultar tiempos por empleado, proyecto, fecha e intervalo.
- Revisar informes y operaciones de eliminación/actualización.
- Anotar qué pruebas se ejecutaron y sus resultados.

## Nota sobre el estado

Este README es una guía de avance, no una confirmación de que todas las funciones estén operativas. Actualizar los porcentajes después de ejecutar y probar los flujos principales.
