"""
Settings de produccion para PythonAnywhere.
Copia este archivo como settings_production.py en patolsima_api/
"""
import os
from pathlib import Path
import dj_database_url
from datetime import timedelta
import pdfkit
from patolsima_api.utils.pyBCV import Currency as BCV_handler

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-98o2t0se_#p1l#j*)&@x%dt3nt2u)xj1@e!2*9%8zs=d(rfzn3"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "patolsima.pythonanywhere.com",
    "localhost",
    "127.0.0.1",
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = [
    "https://patolsima.pythonanywhere.com",
    "https://patolsimaprueba.netlify.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "https://patolsima.pythonanywhere.com",
    "https://patolsimaprueba.netlify.app",
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-Party Apps
    "corsheaders",
    "softdelete",
    "simple_history",
    "rest_framework",
    "rest_framework_simplejwt",
    # Local Apps (Your project's apps)
    "patolsima_api.apps.core",
    "patolsima_api.apps.facturacion",
    "patolsima_api.apps.uploaded_file_management",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # simple_history
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "patolsima_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

WSGI_APPLICATION = "patolsima_api.wsgi.application"

# Database - SQLite para PythonAnywhere free tier
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "patolsima_api.utils.pagination.PatolsimaPaginationDefault",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "EXCEPTION_HANDLER": "patolsima_api.utils.error_handling.general_error_handler",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissions",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Environment-specific settings
ENV = os.environ.get("env", "production")

# S3 HANDLING
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
S3_LOCALE_PATH = os.environ.get("S3_LOCALE_PATH", f"{os.getcwd()}/var/s3")
S3_DEFAULT_BUCKET = os.environ.get("S3_DEFAULT_BUCKET", "default")
S3_BUCKETS = [
    S3_DEFAULT_BUCKET,
    *[bucket for bucket in os.environ.get("S3_BUCKETS", "").split(",") if bucket],
]
S3_DEFAULT_REGION = os.environ.get("S3_DEFAULT_REGION", "us-east-2")

DEFAULT_BINARY_STREAMS_CHUNK_SIZE = int(
    os.environ.get("DEFAULT_BINARY_STREAMS_CHUNK_SIZE", 4096)
)

# Cambios de Dolares a Bolivares
CAMBIO_USD_BS_PROPERTY_NAME = "bs_e"
BCV_HANDLER = BCV_handler(lazy_load=True)

# PDFKIT configuration - wkhtmltopdf no disponible en PythonAnywhere
# Se usa solo para generacion de PDFs en local
try:
    PDFKIT_CONFIGURATION = pdfkit.configuration(
        wkhtmltopdf=os.environ.get(
            "WKHTMLTOPDF_EXECUTABLE_PATH", "/usr/local/bin/wkhtmltopdf"
        )
    )
    PDFKIT_RENDER_PATH = os.environ.get("PDFKIT_RENDER_PATH", f"{os.getcwd()}/var/pdfkit")
    PDFKIT_VERBOSE_OUTPUT = bool(int(os.environ.get("PDFKIT_VERBOSE_OUTPUT", 0)))
except IOError:
    # wkhtmltopdf no instalado (ej: PythonAnywhere free tier)
    PDFKIT_CONFIGURATION = None
    PDFKIT_RENDER_PATH = os.environ.get("PDFKIT_RENDER_PATH", f"{os.getcwd()}/var/pdfkit")
    PDFKIT_VERBOSE_OUTPUT = False

# API Host
API_HOST = os.environ.get("API_HOST", "https://patolsima.pythonanywhere.com")

# Uploaded file expiration time
UPLOADED_FILE_EXPIRATION_TIME_SECONDS = int(
    os.environ.get("UPLOADED_FILE_EXPIRATION_TIME_SECONDS", "3600")
)

# Logging - usar console en lugar de archivo para PythonAnywhere
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}
