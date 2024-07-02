"""
This module contains the AppConfig class for configuring the 'app.architect_request'
Django application.
"""

from django.apps import AppConfig


class ArchitectRequestConfig(AppConfig):
    """
    AppConfig for the 'app.architect_request' Django application.

    This AppConfig defines configuration for the 'app.architect_request' app,
    including the default_auto_field setting and the app name.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.architect_request"
