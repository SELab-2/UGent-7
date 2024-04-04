"""
Django settings for ypovoli project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from datetime import timedelta
from os import environ
from pathlib import Path

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# TODO: Change
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, "data/production"))


TESTING_BASE_LINK = "http://testserver"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get("DJANGO_SECRET_KEY", "lnZZ2xHc6HjU5D85GDE3Nnu4CJsBnm")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environ.get("DJANGO_DEBUG", "False").lower() in ["true", "1", "t"]
DOMAIN_NAME = environ.get("DJANGO_DOMAIN_NAME", "localhost")
ALLOWED_HOSTS = [DOMAIN_NAME]
CSRF_TRUSTED_ORIGINS = ["https://" + DOMAIN_NAME]


# Application definition
INSTALLED_APPS = [
    # Built-ins
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework_swagger",  # Swagger
    "rest_framework",  # Django rest framework
    "drf_yasg",  # Yet Another Swagger generator
    "sslserver",  # Used for local SSL support (needed by CAS)
    "authentication",  # Ypovoli authentication
    "api",  # Ypovoli logic of the base application
    "notifications",  # Ypovoli notifications
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "UPDATE_LAST_LOGIN": True,
    "TOKEN_OBTAIN_SERIALIZER": "authentication.serializers.CASTokenObtainSerializer",
}

ROOT_URLCONF = "ypovoli.urls"
WSGI_APPLICATION = "ypovoli.wsgi.application"

# Authentication
AUTH_USER_MODEL = "authentication.User"

# Application endpoints
PORT = environ.get("DJANGO_CAS_PORT", "8080")
CAS_ENDPOINT = "https://login.ugent.be"
# TODO: Change back (remove api)
CAS_RESPONSE = f"https://{DOMAIN_NAME}:{PORT}/api/auth/verify"
CAS_DEBUG_RESPONSE = f"https://{DOMAIN_NAME}:{PORT}/api/auth/cas/echo"
API_ENDPOINT = f"https://{DOMAIN_NAME}/api"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": environ.get("DJANGO_DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": environ.get("DJANGO_DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": environ.get("DJANGO_DB_USER", ""),
        "PASSWORD": environ.get("DJANGO_DB_PASSWORD", ""),
        "HOST": environ.get("DJANGO_DB_HOST", ""),
        "PORT": environ.get("DJANGO_DB_PORT", ""),
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
LANGUAGES = [("en", _("languages.en")), ("nl", _("languages.nl"))]
USE_L10N = False
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = "api/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

EMAIL_HOST = "smtprelay.UGent.be"
EMAIL_PORT = 25

EMAIL_CUSTOM = {
    "from": "ypovoli@ugent.be",
    "subject": "[Ypovoli] New Notification",
    "timeout": 2,
    "max_errors": 3,
}

REDIS_CUSTOM = {
    "host": environ.get("DJANGO_REDIS_HOST", "localhost"),
    "port": environ.get("DJANGO_REDIS_PORT", 6379),
    "db_django": 0,
    "db_celery": 1,
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://@{REDIS_CUSTOM['host']}:{REDIS_CUSTOM['port']}/{REDIS_CUSTOM['db_django']}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

CELERY_BROKER_URL = f"redis://@{REDIS_CUSTOM['host']}:{REDIS_CUSTOM['port']}/{REDIS_CUSTOM['db_celery']}"
CELERY_RESULT_BACKEND = f"redis://@{REDIS_CUSTOM['host']}:{REDIS_CUSTOM['port']}/{REDIS_CUSTOM['db_celery']}"

FILE_PATHS = {
    "docker_images": "../data/docker_images/",
    "extra_checks": "../data/extra_checks/",
    "log_file": "../data/log_files/"
}
