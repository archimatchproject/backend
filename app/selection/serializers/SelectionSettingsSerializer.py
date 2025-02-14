"""
This module provides the SelectionSettingsSerializer for transforming the
SelectionSettings model into a structured format suitable for API responses.
"""

from rest_framework import serializers
from app.selection import (
    DAYS_AFTER_CALL_EMAIL_CHOICES,
    DAYS_BEFORE_CALL_EMAIL_CHOICES,
    DAYS_FOR_ADMIN_DISPLAY_CHOICES,
    DAYS_FOR_ADMIN_MANAGEMENT_CHOICES,
    DAYS_TO_LOCK_PROJECT_CHOICES,
    DAYS_TO_PHONE_CALL_CHOICES,
    DAYS_TO_REDIFFUSE_CHOICES,
    PHASE_DAYS_CHOICES,
    TIMES_TO_UNLOCK_PROJECT_CHOICES,
)
from app.selection.models.SelectionSettings import SelectionSettings


class SelectionSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for the SelectionSettings model.

    Transforms the SelectionSettings instance into a structured dictionary
    with labels and values for API responses. Includes custom formatting for
    the email sending hour field.
    """

    settings = serializers.SerializerMethodField()

    class Meta:
        model = SelectionSettings
        fields = ["id", "settings"]

    def get_settings(self, obj):
        """
        Generate a structured representation of selection settings with camelCase names.

        Args:
            obj (SelectionSettings): The SelectionSettings instance to serialize.

        Returns:
            list[dict]: A list of dictionaries, each containing a camelCase name, label, and value.
        """

        return [
            {
                "name": "phase_days",
                "label": "Deadline de la selection",
                "value": obj.phase_days,
                "choices": PHASE_DAYS_CHOICES,
            },
            {
                "name": "days_before_call_email",
                "label": "Relance automatique avant appel telephonique",
                "value": obj.days_before_call_email,
                "choices": DAYS_BEFORE_CALL_EMAIL_CHOICES,
            },
            {
                "name": "days_to_phone_call",
                "label": "Appel telephonique",
                "value": obj.days_to_phone_call,
                "choices": DAYS_TO_PHONE_CALL_CHOICES,
            },
            {
                "name": "days_after_call_email",
                "label": "Relance automatique apres appel telephonique",
                "value": obj.days_after_call_email,
                "choices": DAYS_AFTER_CALL_EMAIL_CHOICES,
            },
            {
                "name": "days_to_rediffuse",
                "label": "Rediffusion du projet",
                "value": obj.days_to_rediffuse,
                "choices": DAYS_TO_REDIFFUSE_CHOICES,
            },
            {
                "name": "days_to_lock_project",
                "label": "Deadline de deblocage du projet",
                "value": obj.days_to_lock_project,
                "choices": DAYS_TO_LOCK_PROJECT_CHOICES,
            },
            {
                "name": "times_to_unlock_project",
                "label": "Nombre de fois de deblocage du projet",
                "value": obj.times_to_unlock_project,
                "choices": TIMES_TO_UNLOCK_PROJECT_CHOICES,
            },
            {
                "name": "days_for_admin_management",
                "label": "Intervention manuelle admin",
                "value": obj.days_for_admin_management,
                "choices": DAYS_FOR_ADMIN_MANAGEMENT_CHOICES,
            },
            {
                "name": "email_sending_hour",
                "label": "Heure de relance",
                "value": obj.email_sending_hour.strftime("%H:%M"),
                "choices": PHASE_DAYS_CHOICES,
            },
            {
                "name": "days_for_admin_display",
                "label": "Affichage en espace admin",
                "value": obj.days_for_admin_display,
                "choices": DAYS_FOR_ADMIN_DISPLAY_CHOICES,
            },
        ]
