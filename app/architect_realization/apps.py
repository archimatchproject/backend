"""
This module contains the AppConfig class for configuring the 'app.cms' Django application.
"""

from django.apps import AppConfig


class ArchitectRealizationConfig(AppConfig):
    """
    AppConfig for the 'app.architect_realization' Django application.

    This AppConfig defines configuration for the 'app.architect_realization' app,
    including the default_auto_field setting and the app name.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.architect_realization"
