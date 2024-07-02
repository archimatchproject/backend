"""
This module contains the AppConfig class for configuring the 'app.announcement' Django application.
"""

from django.apps import AppConfig


class AnnouncementConfig(AppConfig):
    """
    AppConfig for the 'app.announcement' Django application.

    This AppConfig defines configuration for the 'app.announcement' app,
    including the default_auto_field setting and the app name.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.announcement"
