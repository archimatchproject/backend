"""
This module contains the AppConfig class for configuring the 'app.catalogue' Django application.
"""

from django.apps import AppConfig


class CatalogueConfig(AppConfig):
    """
    AppConfig for the 'app.catalogue' Django application.

    This AppConfig defines configuration for the 'app.catalogue' app,
    including the default_auto_field setting and the app name.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.catalogue"
