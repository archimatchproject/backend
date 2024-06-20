"""
Configuration for the 'core' Django application.

This AppConfig defines the configuration for the Django application named 'core'.

"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configuration class for the 'core' Django application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.core"
