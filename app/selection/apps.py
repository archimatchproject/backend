"""
This module contains the AppConfig class for configuring the 'app.announcement' Django application.
"""

from django.apps import AppConfig


class SelectionConfig(AppConfig):
    """
    AppConfig for the 'app.selection' Django application.

    This AppConfig defines configuration for the 'app.selection' app,
    including the default_auto_field setting and the app name.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.selection"
