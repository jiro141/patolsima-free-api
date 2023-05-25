"""
Django settings for patolsima_api project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
import dj_database_url
from datetime import timedelta
import pdfkit
from patolsima_api.utils.pyBCV import Currency as BCV_handler

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-98o2t0se_#p1l#j*)&@x%dt3nt2u)xj1@e!2*9%8zs=d(rfzn3"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True


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
        "DIRS": [],
        # "APP_DIRS": True, Set casually to false, but I have to review this change later
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": (
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ),
        },
    },
]

WSGI_APPLICATION = "patolsima_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(conn_max_age=600, conn_health_checks=True)
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "patolsima_api.utils.pagination.PatolsimaPaginationDefault",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
}


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


ENV = os.environ.get("env")

# S3 HANDLING
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
S3_LOCALE_PATH = os.environ.get("S3_LOCALE_PATH", f"{os.getcwd()}/var/s3")
S3_DEFAULT_BUCKET = os.environ.get("S3_DEFAULT_BUCKET", "default")
S3_BUCKETS = [
    S3_DEFAULT_BUCKET,
    *[bucket for bucket in os.environ.get("S3_BUCKETS", "").split(",") if bucket],
]

# Binary streams chunk size (e.g. for downloading/uploading files without collapsing the system due to lack of memory
# resources)

DEFAULT_BINARY_STREAMS_CHUNK_SIZE = int(
    os.environ.get("DEFAULT_BINARY_STREAMS_CHUNK_SIZE", 4096)
)

# Cambios de Dolares a Bolivares
CAMBIO_USD_BS_PROPERTY_NAME = "bs_e"
BCV_HANDLER = BCV_handler(lazy_load=True)

# PDFKIT
PDFKIT_CONFIGURATION = pdfkit.configuration(
    wkhtmltopdf=os.environ.get(
        "WKHTMLTOPDF_EXECUTABLE_PATH", "/usr/local/bin/wkhtmltopdf"
    )
)
PDFKIT_RENDER_PATH = os.environ.get("PDFKIT_RENDER_PATH", f"{os.getcwd()}/var/pdfkit")
PDFKIT_VERBOSE_OUTPUT = bool(int(os.environ.get("PDFKIT_VERBOSE_OUTPUT", 0)))
