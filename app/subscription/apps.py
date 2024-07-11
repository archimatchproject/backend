"""
This module contains the AppConfig class for configuring the 'app.subscription' Django application.
"""

from django.apps import AppConfig


class SubscriptionConfig(AppConfig):
    """
    AppConfig for the 'app.subscription' Django application.

    This AppConfig defines configuration for the 'app.subscription' app,
    including the default_auto_field setting and the app name.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.subscription"
