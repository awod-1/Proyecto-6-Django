# Proyecto Módulo 6: gestión de proyectos y tareas

Aplicación Django 5.2 con SQLite, registro, autenticación, proyectos y tareas por usuario, formularios, administración y pruebas. Requiere Python 3.10 o superior. Preparada para ejecución local en Visual Studio Code.

## Instalación en Windows

Descomprime el ZIP y abre la carpeta `proyecto6` en Visual Studio Code. Abre Terminal > Nueva terminal. Ejecuta desde la carpeta que contiene `manage.py`:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py runserver
```

No es necesario activar el entorno ni cambiar la política de PowerShell. En VS Code usa Python: Select Interpreter y selecciona `.venv\Scripts\python.exe`.

Abre http://127.0.0.1:8000/ en el navegador. Para detener el servidor presiona Ctrl+C. Para volver a iniciarlo usa el último comando.

## Instalación en macOS o Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py test
.venv/bin/python manage.py runserver
```

## Uso

1. Registra una cuenta en `/cuentas/registro/`.
2. Inicia sesión y crea un proyecto.
3. Abre el proyecto y agrega tareas con descripción, estado y fecha opcional.
4. Edita proyectos y tareas desde sus enlaces.
5. Elimina mediante una pantalla de confirmación. Eliminar un proyecto elimina sus tareas.
6. Usa Salir para cerrar la sesión mediante POST.
7. Entra a `/admin/` con el superusuario creado para administrar usuarios, grupos, permisos, proyectos y tareas.

Los usuarios normales solo acceden a sus propios datos. El administrador tiene acceso global a través del sitio administrativo y puede asignar permisos a personal autorizado. No se incluyen contraseñas predefinidas.

## Estructura

- `config/`: settings, URLs generales, WSGI y ASGI.
- `gestion/models.py`: Proyecto y Tarea; relación usuario -> proyectos -> tareas.
- `gestion/forms.py`: registro y ModelForms; propietario y proyecto se asignan en el servidor.
- `gestion/views.py`: vistas basadas en clases con LoginRequiredMixin y consultas por propietario.
- `gestion/urls.py`: rutas de proyectos y tareas.
- `gestion/admin.py`: administración, búsquedas, filtros y usuarios con permisos.
- `gestion/migrations/`: esquema inicial de base de datos.
- `gestion/tests.py`: pruebas automatizadas.
- `templates/base.html`: estructura compartida mediante herencia.
- `templates/registration/`: inicio de sesión.
- `templates/gestion/`: lista, detalle, formularios y confirmaciones.
- `static/estilos.css`: diseño adaptable sin dependencias externas.
- `pruebas_resultado.txt`: resultado de la ejecución realizada durante la preparación.

## Pruebas

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test --verbosity 2
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Se incluyen 13 pruebas: relaciones y representación de modelos, validación de modelos, validación de formularios, restricciones para visitantes, datos visibles por usuario, CRUD de proyectos, CRUD de tareas, bloqueo de accesos ajenos, eliminación en cascada, registro/login/logout, registro inválido, CSRF y administración.

Las pruebas crean una base temporal y no eliminan tus datos locales. Las contraseñas que aparecen en tests son únicamente datos de prueba.

## Correspondencia con la consigna

| Requisito | Implementación |
|---|---|
| Registro y autenticación | UserCreationForm, LoginView, LogoutView |
| Redirecciones | LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL |
| Acceso autenticado | LoginRequiredMixin |
| Modelos relacionados | Proyecto.usuario y Tarea.proyecto |
| Crear, modificar y eliminar | Vistas CreateView, UpdateView y DeleteView |
| Templates dinámicos | Herencia de base.html, contextos, bucles y estados |
| Validaciones | ModelForms, validadores de contraseñas y clean() |
| CSRF | Middleware y csrf_token en todos los formularios |
| Administración | ModelAdmin y UserAdmin con filtros y búsquedas |
| Pruebas | gestion/tests.py |

## Capturas y demostración para la entrega

El código y las pruebas están incluidos. Debes obtener capturas de tu ejecución y realizar la demostración solicitada por la evaluación.

Captura estas pantallas: registro, inicio de sesión, lista con proyectos creados, detalle con tareas en distintos estados, edición de una tarea y administración de usuarios/proyectos.

Guion sugerido de demostración: registrar una cuenta, iniciar sesión, crear un proyecto y dos tareas, completar una tarea, editar el proyecto, mostrar que otra cuenta no ve ese proyecto, eliminar una tarea, mostrar el administrador y ejecutar las pruebas en la terminal.

## Configuración

La configuración predeterminada es para desarrollo local. SQLite guarda los datos en `db.sqlite3`, creado al ejecutar migrate.

`DJANGO_SECRET_KEY` permite fijar la clave secreta mediante una variable de entorno. Si no se define, se genera una clave en cada proceso; en desarrollo reiniciar el servidor puede invalidar sesiones existentes.

Para despliegue real fija una clave persistente, `DJANGO_DEBUG=0` y `DJANGO_ALLOWED_HOSTS` con los dominios separados por comas. El modo sin DEBUG exige HTTPS y cookies seguras. Configura además un servidor WSGI/ASGI y el servicio de archivos estáticos; runserver se usa exclusivamente para desarrollo. No se incluyen un despliegue productivo ni un video grabado.

## Fuentes

Consigna: Proyecto Módulo #6 ABP proporcionado en PDF.
Documentación: https://docs.djangoproject.com/en/5.2/ y https://docs.djangoproject.com/en/5.2/topics/auth/default/
