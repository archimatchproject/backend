"""
This module contains the AppConfig class for configuring the 'app.moderation' Django application.
"""

from django.apps import AppConfig


class ModerationConfig(AppConfig):
    """
    AppConfig for the 'app.moderation' Django application.

    This AppConfig defines configuration for the 'app.moderation' app,
    including the default_auto_field setting and the app name.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.moderation"
