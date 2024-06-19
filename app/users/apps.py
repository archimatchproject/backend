"""
Module: app.apps

This module contains the AppConfig class for configuring the 'app.users' Django application.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    AppConfig for the 'app.users' Django application.

    This AppConfig defines configuration for the 'app.users' app,
    including the default_auto_field setting and the app name.

    Attributes:
        default_auto_field (str): The type of auto-generated primary key field for models.
        name (str): The full name of the Django application ('app.users').
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.users"
