"""
Django settings for my_health_diary project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import datetime
import os
from pathlib import Path

from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv("DEBUG").lower() == "true":
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = str(os.getenv("ALLOWED_HOSTS")).split(" ")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    "debug_toolbar",
    "post_office",
    "rest_framework",
    "apps.core",
    "apps.authentication",
]

AUTH_USER_MODEL = "core.User"

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "my_health_diary.urls"

CSRF_TRUSTED_ORIGINS = [
    "http://www.f-programs.ru",
    "http://f-programs.ru",
    "http://127.0.0.1",
    "http://localhost",
    "https://www.f-programs.ru",
    "https://f-programs.ru",
    "https://127.0.0.1",
    "https://localhost",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "my_health_diary.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": f"{BASE_DIR}/database/" + "db.sqlite3",
    },
}

# CELERY settings
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
# CELERY settings for localhost
# CELERY_BROKER_URL = "redis://localhost:6379/0"
# CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        # "LOCATION": "redis://127.0.0.1:6379/0",
        "TIMEOUT": 60 * 15,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

POST_OFFICE = {
    "DEFAULT_PRIORITY": "now",
    "CELERY_ENABLED": True,
    "MESSAGE_ID_ENABLED": True,
    "MAX_RETRIES": 5,
    "RETRY_INTERVAL": datetime.timedelta(
        minutes=15,
    ),  # Schedule to be retried 15 minutes later
    "LOG_LEVEL": 2,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(name)-12s %(levelname)-8s %(message)s",
        },
        "main": {
            "format": "%(levelname)-8s %(asctime)s %(name)s:%(lineno)d"
            "  >  %(message)s",
            "style": "%",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "file_django": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/service_django.log",
            "formatter": "main",
        },
        "file_site": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/service.log",
            "formatter": "main",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["console", "file_site"],
            "propagate": True,
        },
        "django.template": {
            "handlers": ["file_django"],
            "level": "INFO",
            "propagate": True,
        },
        "django": {
            "handlers": ["file_django"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console", "file_django", "mail_admins"],
            "level": "DEBUG",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console", "file_site", "mail_admins"],
            "level": "DEBUG",
        },
    },
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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

DATE_INPUT_FORMATS = ("%d.%m.%Y",)  # '10.12.1985'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

EMAIL_BACKEND = "post_office.EmailBackend"
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
