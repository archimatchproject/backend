"""
This module contains the configuration class for the 'quote' app.
    Classes:
        QuoteConfig: Configuration class for the 'quote' app, setting the default
"""

from django.apps import AppConfig


class QuoteConfig(AppConfig):
    """
    Configuration class for the 'quote' app.
    This class inherits from Django's AppConfig and sets the default
    auto field type to BigAutoField and the name of the app to 'app.quote'.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.quote"
