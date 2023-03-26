# PATOLSIMA API

Este es el repo que contiene la API para el sistema web del Laboratorio Patologico Patolsima.

Este backend se encuentra escrito en Django (4.x) con Python 3.10.x, usando el paquete Django REST Framework.
Puede ser ejecutado usando Docker (recomendado) o como un servidor comun y silvestre.

## Instalacion (local/sin docker)

1. Cree un entorno virtual (puede usar `venv`, `virtualenvwrapper` o cualquier otro wrapper alrededor de `venv`).
2. Active el entorno virtual.
3. Ejecute `pip install -r requirements.txt`
4. Descargue y ejecute el servidor para PostgreSQL en su entorno local.
5. Copie el archivo `.env.template` dentro de un archivo nuevo llamado `.env`
6. Dentro del nuevo `.env` añada las credenciales para acceder a su servidor de Postgres dentro de la variable de entorno DB_URL.
7. Ejecute el comando `python manage.py migrate` para aplicar las migraciones en la DB.
7. Ahora puede iniciar el servidor usando el comando `python manage.py runserver 0.0.0.0:8000`
8. Verifique en su terminal si hay errores.

## Instalacion (Docker)

1. Instale en su compudatora `docker` y la extension `docker-compose`.
    * Recuerde habilitar a su usuario con los permisos para utilizar docker.
2. En el directorio del repositorio ejecute `docker compose build` para compilar la imagen de la API.
3. Ahora ejecute `docker compose up`
4. Si no hay errores en el paso anterior, abra otra terminal y ejecute `docker compose run api make migrate` para correr las migraciones sobre la base de datos.
5. Luego de aplicar las migraciones, ejecute `docker compose run api make tests` para correr los tests.
6. Ahora agregue la data de prueba utilizando `docker compose run api make addtestdata`.
