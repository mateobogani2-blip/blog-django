# Blog Django

Blog web hecho con Django como trabajo final del curso de Python. Es la evolución del
**blog por consola** del curso, que usaba clases `Autor`, `Post` y `Blog` y guardaba los
datos en JSON. Ahora los posts y los autores son modelos de Django guardados en una base
SQLite, con una interfaz web, usuarios y carga de imágenes.

## Tecnologías

- Python 3.12 o superior (probado con 3.13 y 3.15)
- Django 6.1
- SQLite (base de datos que trae Django)
- Pillow (para las imágenes)

## Funcionalidades

- **Posts:** listar, ver detalle, crear, editar y eliminar desde la interfaz web.
- **Imágenes:** cada post puede tener una imagen. Si no tiene, se muestra una imagen
  genérica y la página no se rompe.
- **Estados:** borrador, publicado y archivado. La portada muestra solo los publicados;
  los borradores y archivados los ve únicamente su autor.
- **Tags:** se cargan separados por coma y, al hacer clic en uno, se filtran los posts
  que lo tienen.
- **Búsqueda:** por título o contenido, con un aviso cuando no hay coincidencias.
- **Usuarios:** registro, login y logout.
- **Perfil:** página pública con bio, especialidad, redes y foto, más la lista de posts
  del usuario. Cada uno puede editar su propio perfil y su foto.
- **Rutas protegidas:** para crear, editar o eliminar posts y para editar el perfil hay
  que iniciar sesión. La protección está en las views (`LoginRequiredMixin` y
  `@login_required`): si un visitante anónimo entra a esas URLs, lo manda al login.
  Además, solo el autor de un post puede editarlo o eliminarlo.
- **Panel de administración** de Django para posts y perfiles.

## Del blog por consola al blog web

El proyecto reúne lo que se trabajó en cada etapa del curso:

| Blog por consola | Blog Django |
|---|---|
| Clase `Post` (título, contenido, tags, estado, autor) | Modelo `Post` en `posts/models.py`, con los mismos campos más la imagen y las fechas |
| Clase `Autor` (nombre, bio, especialidad, redes) | Usuario de Django + modelo `Perfil` en `usuarios/models.py` |
| Clase `Blog` (listar, buscar por título, filtrar por tag) | Views de `posts/views.py`: lista, búsqueda (`?q=`) y filtro por tag (`?tag=`) |
| Estados `borrador`, `publicado`, `archivado` | `Post.Estado`, con las mismas tres opciones |
| `posts.json` con `json.load()` | Base SQLite con migraciones. Los posts del JSON se cargan con `cargar_posts_ejemplo` |
| Menú por consola | Interfaz web con templates y Bootstrap |

## Instalación

> Los comandos son para Windows (PowerShell o CMD). En macOS/Linux se indica la
> alternativa.

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/mateobogani2-blip/blog-django.git
   cd blog-django
   ```

2. **Crear y activar el entorno virtual**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   En macOS/Linux: `python3 -m venv .venv` y `source .venv/bin/activate`.

3. **Instalar las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno (opcional)**

   Copiá `.env.example` como `.env` y poné tu propia `SECRET_KEY`:

   ```bash
   copy .env.example .env
   ```

   En macOS/Linux: `cp .env.example .env`.

   Si no creás el `.env`, el proyecto igual arranca con valores de desarrollo.

5. **Aplicar las migraciones** (crea la base `db.sqlite3`)

   ```bash
   python manage.py migrate
   ```

6. **(Opcional) Cargar posts de ejemplo**

   Carga los 3 posts del blog por consola con su autor:

   ```bash
   python manage.py cargar_posts_ejemplo
   ```

7. **(Opcional) Crear un superusuario** para entrar al panel `/admin/`

   ```bash
   python manage.py createsuperuser
   ```

8. **Iniciar el servidor**

   ```bash
   python manage.py runserver
   ```

   Abrí <http://127.0.0.1:8000/> en el navegador.

## Probar el proyecto desde cero

El repositorio no incluye `db.sqlite3` ni la carpeta `media/`, así que cada persona
empieza con una base vacía. Para probarlo:

1. Seguí los pasos de instalación (con `migrate`).
2. Registrate en **Registrarse** (arriba a la derecha).
3. Creá un post con **+ Nuevo post**, con imagen y sin imagen.
4. Probá editar, eliminar, buscar y hacer clic en un tag.
5. Cerrá sesión y entrá a `/posts/nuevo/`: te tiene que mandar al login.

También hay tests automáticos que cubren todo lo anterior:

```bash
python manage.py test
```

## Estructura

```
blog-django/
├── config/            # Configuración del proyecto (settings, urls)
├── posts/             # App de publicaciones: modelo Post, views, forms, tests
│   ├── datos/         # posts_ejemplo.json (del blog por consola)
│   ├── management/    # Comando cargar_posts_ejemplo
│   └── migrations/
├── usuarios/          # App de usuarios: registro, login, perfil (modelo Perfil)
│   └── migrations/
├── templates/         # Templates HTML (base, posts, usuarios, login)
├── static/            # CSS, imágenes del sitio y Bootstrap
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Rutas principales

| URL | Qué hace | ¿Requiere login? |
|---|---|---|
| `/` | Lista de posts, búsqueda (`?q=`) y filtro por tag (`?tag=`) | No |
| `/posts/<id>/` | Detalle de un post | No |
| `/posts/nuevo/` | Crear post | Sí |
| `/posts/<id>/editar/` | Editar post (solo el autor) | Sí |
| `/posts/<id>/eliminar/` | Eliminar post (solo el autor) | Sí |
| `/usuarios/registro/` | Crear cuenta | No |
| `/usuarios/login/` y `/usuarios/logout/` | Iniciar y cerrar sesión | — |
| `/usuarios/perfil/<usuario>/` | Perfil público | No |
| `/usuarios/perfil/editar/` | Editar mi perfil | Sí |
| `/admin/` | Panel de administración | Superusuario |

## Autor

**Mateo Bogani**. Trabajo final del curso de Python.
