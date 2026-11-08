# NuevoRepositorio

Sistema de gestión para control de recursos, tiempos y reportes de personal.

---

## 📊 Estado del Proyecto

El proyecto se encuentra en una etapa avanzada de desarrollo, con la estructura base, la conexión a la base de datos y los módulos principales ya implementados. Aún faltan algunos ajustes de integración y la finalización de ciertos módulos clave para dejarlo completamente funcional y estable.

| Módulo | Estado | Avance |
|---|---|---|
| Estructura general | ✅ Completa | 85% |
| Autenticación / usuarios | ✅ Avanzado | 80% |
| Base de datos | ✅ Estable | 75% |
| Empleados | ✅ Avanzado | 75% |
| Departamentos | ✅ Avanzado | 70% |
| Tiempos | ✅ Avanzado | 80% |
| Proyectos | ⚠️ En desarrollo | 45% |
| Informes | ⚠️ Inicial | 30% |
| Integración final y pruebas | ⚠️ Pendiente | 40% |

> Progreso global estimado: 65%

---

## ✅ Funcionalidades actuales

- Gestión de usuarios y autenticación.
- Registro y administración de empleados.
- Organización por departamentos.
- Registro de tiempos de trabajo.
- Conexión con SQLite.
- Estructura modular con modelos, DAO, controladores y vistas.

---

## ⚠️ Pendientes principales

- Completar la gestión de proyectos.
- Finalizar la lógica de informes y reportes.
- Corregir detalles de integración entre DAO, controladores y vistas.
- Validar flujo completo de alta, edición, eliminación y consultas.
- Realizar pruebas de funcionamiento integradas.

---

## 🧩 Arquitectura

El proyecto está organizado en capas:

- `models/`: entidades y acceso a datos.
- `controllers/`: lógica de control del flujo.
- `views/`: interfaz de usuario / mensajes / menús.
- `config/`: configuración de la aplicación y base de datos.
- `services/`: lógica auxiliar y procesos específicos.
- `main.py`: punto de entrada del sistema.

---

## 🚀 Ejecución

1. Clonar el repositorio.
2. Crear un entorno virtual.
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt