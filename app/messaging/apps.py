"""
This module contains the AppConfig class for configuring the 'app.messaging' Django application.
"""

from django.apps import AppConfig


class MessagingConfig(AppConfig):
    """
    AppConfig for the 'app.messaging' Django application.

    This AppConfig defines configuration for the 'app.messaging' app,
    including the default_auto_field setting and the app name.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.messaging"
