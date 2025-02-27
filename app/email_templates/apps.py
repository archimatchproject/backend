"""
Configuration for the 'email_templates' Django application.

This AppConfig defines the configuration for the Django application named 'email_templates'.

"""

from django.apps import AppConfig


class EmailTemplatesConfig(AppConfig):
    """
    Configuration class for the 'email_templates' Django application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app.email_templates"

    def ready(self):
        """
        Performs initialization tasks when the Django application is fully loaded.
        """
        import app.email_templates.receivers  # noqa
