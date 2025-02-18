"""
This module contains the AppConfig class for configuring the 'app.officeOffer' Django application.
"""

from django.apps import AppConfig


class OfficeOfferConfig(AppConfig):
    """
    AppConfig for the 'app.officeOffer' Django application.

    This AppConfig defines configuration for the 'app.officeOffer' app,
    including the default_auto_field setting and the app name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.officeOffer"
