"""
This module contains the AppConfig class for configuring the 'app.users' Django application.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    AppConfig for the 'app.users' Django application.

    This AppConfig defines configuration for the 'app.users' app,
    including the default_auto_field setting and the app name.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.users"

    def ready(self):
        """
        importing app signals
        """
        import app.users.signals  # noqa
