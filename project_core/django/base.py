"""
Module-level constants for base configuration.

This module defines the base configuration constants and settings for the Django project.
"""

import os

from project_core.env import BASE_DIR
from project_core.env import env
from project_core.settings.cors import *
from project_core.settings.email_sending import *
from project_core.settings.jwt import *
from project_core.settings.sms_sending import *
from project_core.settings.templates_icon import *


"""
Third-party applications used in the project.
"""
THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "drf_yasg",
    "rest_framework_simplejwt",
    "djangorestframework_camel_case",
    "drf_standardized_errors",
    "background_task",
]

"""
Local applications specific to this Django project.
"""
LOCAL_APPS = [
    "app.core",
    "app.users",
    "app.cms",
    "app.announcement",
    "app.architect_request",
    "app.email_templates",
    "app.architect_realization",
    "app.subscription",
    "app.catalogue",
    "app.moderation",
]


"""
Combined list of installed applications.
"""
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *LOCAL_APPS,
    *THIRD_PARTY_APPS,
]

"""
Configuration for Django Rest Framework.
"""
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
}

DRF_STANDARDIZED_ERRORS = {"ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True}

"""
Middleware stack for request/response processing.
"""
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

"""
URL configuration for the project.
"""
ROOT_URLCONF = "project_core.urls"

"""
Template engine configuration.
"""
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "app/email_templates/templates"),
        ],
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

"""
WSGI application configuration.
"""
WSGI_APPLICATION = "project_core.wsgi.application"

"""
Password validation configuration.
"""
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

"""
Database configuration.
"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

"""
Custom user model for authentication.
"""
AUTH_USER_MODEL = "users.ArchimatchUser"

"""
Internationalization and localization settings.
"""
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Tunis"
USE_TZ = True
USE_I18N = True

"""
Static files (CSS, JavaScript, Images) serving configuration.
"""
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

"""
Static files storage configuration for production.
"""
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

"""
Default primary key field type configuration.
"""
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

"""
Media files (uploads) configuration.
"""
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
