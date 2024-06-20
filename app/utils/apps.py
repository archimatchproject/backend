"""
Configuration for the 'utils' Django application.

This AppConfig defines the configuration for the Django application named 'utils'.

"""

from django.apps import AppConfig


class UtilsConfig(AppConfig):
    """
    Configuration class for the 'utils' Django application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.utils"
