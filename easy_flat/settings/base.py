"""
Django settings for easy_flat project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import typing
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
env_file = os.path.join(os.path.dirname(BASE_DIR), ".env")
env = environ.Env()
environ.Env.read_env(env_file=env_file)


def get_env_value(name: str, default: any = None) -> typing.Union[typing.Any, str]:
    return env(name, default=None) or os.environ.get(name) or default


# Build paths inside the project like this: BASE_DIR / 'subdir'.
AUTH_USER_MODEL = "user.CustomUser"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_value("SECRET_KEY", default="key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env_value("DEBUG", default=True)

ALLOWED_HOSTS: typing.List[str] = get_env_value("ALLOWED_HOSTS", default=True)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_jwt",
   # "silk",
    "drf_yasg",
    "django_filters",
    "community",
    "user",
    "api",
    "flat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
#    "silk.middleware.SilkyMiddleware",
]

ROOT_URLCONF = "easy_flat.urls"

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

WSGI_APPLICATION = "easy_flat.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_FILES_DIR = os.environ.get('STATIC_FILES_DIR', default=None)
STATIC_ROOT = os.environ.get('STATIC_FILES_DIR', default='staticfiles')
STATIC_URL = "/static/"
FRONTEND_URL = "http://127.0.0.1:8000/"
