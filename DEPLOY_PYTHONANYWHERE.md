# Guia de Despliegue - PythonAnywhere

## Prerequisitos

1. Cuenta en [PythonAnywhere](https://www.pythonanywhere.com/) (free tier funciona)
2. Git instalado
3. Tu repositorio en GitHub/GitLab

---

## Paso 1: Preparar el Repositorio

### 1.1 Asegurate de tener el script de datos de prueba

El management command `seed_all_data.py` ya esta creado en:
```
patolsima_api/apps/core/management/commands/seed_all_data.py
```

### 1.2 Crear archivo de configuracion para produccion

Crea `patolsima_api/settings_production.py` (ya creado en el repo).

### 1.3 Actualizar .gitignore

Asegurate de que `.env` NO se suba a git:

```gitignore
# En .gitignore debe estar:
.env
db.sqlite3
*.pyc
__pycache__/
staticfiles/
logs/
var/
```

### 1.4 Subir cambios a GitHub

```bash
git add .
git commit -m "feat: add production settings and seed data script"
git push origin main
```

---

## Paso 2: Configurar PythonAnywhere

### 2.1 Clonar el repositorio

En la consola de PythonAnywhere (Bash console):

```bash
cd ~
git clone https://github.com/TU_USUARIO/patolsima-free-api.git
cd patolsima-free-api
```

### 2.2 Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2.3 Configurar variables de entorno

Ve a **Web** > **Environment variables** y agrega:

```
SECRET_KEY=tu-clave-secreta-aqui-cambiala
DB_NAME=tu_usuario_pythonanywhere
DB_USER=tu_usuario_pythonanywhere
DB_PASSWORD=tu_password_de_mysql
DB_HOST=tu_usuario.mysql.pythonanywhere-services.com
DB_PORT=3306
ENV=production
API_HOST=https://ernestomolina.pythonanywhere.com
```

### 2.4 Configurar la base de datos

PythonAnywhere ofrece MySQL gratis. Ve a **Databases** y crea una base de datos:

1. Ve a la pestaña **Databases**
2. Crea una nueva base de datos (ej: `patolsima`)
3. Anota el nombre de usuario y host

### 2.5 Configurar el Web App

Ve a **Web** y configura:

1. **Python version**: 3.10
2. **Working directory**: `/home/ernestomolina/patolsima-free-api`
3. **Virtualenv**: `/home/ernestomolina/patolsima-free-api/venv`

En **WSGI configuration file**, edita y reemplaza todo con:

```python
import os
import sys

# Agrega tu proyecto al path
project_home = '/home/ernestomolina/patolsima-free-api'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Settings de produccion
os.environ['DJANGO_SETTINGS_MODULE'] = 'patolsima_api.settings_production'

# Activar virtualenv
activate_this = '/home/ernestomolina/patolsima-free-api/venv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## Paso 3: Migraciones y Datos de Prueba

### 3.1 Ejecutar migraciones

En la consola de PythonAnywhere:

```bash
cd ~/patolsima-free-api
source venv/bin/activate

# Configurar modulo de MySQL si usas MySQL
pip install mysqlclient

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
# Sigue las instrucciones (usuario, email, password)
```

### 3.2 Poblar datos de prueba

```bash
python manage.py seed_all_data
```

Esto creara:
- 5 pacientes
- 4 medicos
- 2 patologos
- 5 estudios
- 6 muestras
- 3 informes
- 4 clientes
- 4 ordenes
- 5 items de orden
- 3 pagos
- 2 facturas
- 2 recibos
- 1 nota de credito
- 1 nota de debito
- 3 transacciones

### 3.3 Recopilar archivos estaticos

```bash
python manage.py collectstatic
```

---

## Paso 4: Configurar Static Files

En la configuracion de **Web** de PythonAnywhere, agrega un **Static files**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/ernestomolina/patolsima-free-api/staticfiles` |

---

## Paso 5: Reiniciar y Probar

1. Haz clic en el boton **Reload** en la pestaña Web
2. Visita `https://ernestomolina.pythonanywhere.com/admin/`
3. Prueba el login:

```bash
curl -X POST https://ernestomolina.pythonanywhere.com/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "tu_password"}'
```

---

## Comandos Utiles

### Actualizar el servidor

```bash
cd ~/patolsima-free-api
git pull origin main
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

### Ver logs de errores

```bash
cat ~/patolsima-free-api/logs/django.log
```

### Acceder a la consola Django

```bash
cd ~/patolsima-free-api
source venv/bin/activate
python manage.py shell
```

### Resetear datos de prueba

```bash
python manage.py seed_all_data --flush
```

---

## Estructura de Usuarios Creados

| Usuario | Contraseña | Grupo |
|---------|------------|-------|
| `admin` | `admin123` | admin |
| `dr_martinez` | `patologo123` | patologo |
| `recepcion1` | `recepcion123` | recepcion |
| `facturacion1` | `facturacion123` | facturacion |

---

## Endpoints Disponibles

| Endpoint | Descripcion |
|----------|-------------|
| `POST /login/` | Login (JWT) |
| `POST /token/refresh/` | Refrescar token |
| `GET /v1/core/pacientes/` | Lista pacientes |
| `GET /v1/core/medicos/` | Lista medicos |
| `GET /v1/core/estudios/` | Lista estudios |
| `GET /v1/core/informes/` | Lista informes |
| `GET /v1/facturacion/ordenes/` | Lista ordenes |
| `GET /v1/facturacion/clientes/` | Lista clientes |
| `GET /admin/` | Panel de administracion |

---

## Troubleshooting

### Error 500 Internal Server Error

1. Revisa los logs: `cat ~/patolsima-free-api/logs/django.log`
2. Verifica las variables de entorno
3. Asegurate de que las migraciones estan ejecutadas

### Error de base de datos

1. Verifica que MySQL esta corriendo en PythonAnywhere
2. Revisa las credenciales en las variables de entorno
3. Ejecuta `python manage.py migrate` de nuevo

### Error de permisos

1. Verifica que el usuario de PythonAnywhere tiene permisos
2. Revisa que `ALLOWED_HOSTS` incluye tu dominio

### Los archivos estaticos no cargan

1. Ejecuta `python manage.py collectstatic`
2. Verifica la configuracion de Static files en Web
