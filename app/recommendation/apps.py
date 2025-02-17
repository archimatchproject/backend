"""
This module defines the configuration for the recommendation app.
Classes:
    RecommendationConfig: Configures the recommendation app with the default
    auto field and the app name.
Attributes:
    default_auto_field (str): Specifies the type of auto field to use for
    primary keys by default.
    name (str): The full Python path to the application.
Methods:
    ready: (commented out) Method to import signals when the app is ready.

"""

from django.apps import AppConfig


class RecommendationConfig(AppConfig):
    """
    Configuration class for the recommendation app.
    Attributes:
        default_auto_field (str): Specifies the type of auto-incrementing primary key to use for models in this app.
        name (str): The full Python path to the application.
    Methods:
        ready(): Uncomment to import signals when the application is ready.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.recommendation"

    # def ready(self):
    #     import app.recommendation.signals
