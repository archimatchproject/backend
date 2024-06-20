"""
This module contains the AppConfig class for configuring the 'app.cms' Django application.
"""
from django.apps import AppConfig


class CmsConfig(AppConfig):
    """
    AppConfig for the 'app.cms' Django application.

    This AppConfig defines configuration for the 'app.cms' app,
    including the default_auto_field setting and the app name.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.cms"
