"""
This module provides the SelectionSettingsSerializer for transforming the 
SelectionSettings model into a structured format suitable for API responses.
"""

from rest_framework import serializers
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
        fields = ['settings']

    def get_settings(self, obj):
        """
        Generate a structured representation of selection settings.

        Args:
            obj (SelectionSettings): The SelectionSettings instance to serialize.

        Returns:
            list[dict]: A list of dictionaries, each containing a label and a value 
                        representing a specific setting.
        """
        return [
            {"label": "Deadline de la selection", "value": obj.phase_days},
            {"label": "Relance automatique avant appel telephonique", "value": obj.days_before_call_email},
            {"label": "Appel telephonique", "value": obj.days_to_phone_call},
            {"label": "Relance automatique apres appel telephonique", "value": obj.days_after_call_email},
            {"label": "Rediffusion du projet", "value": obj.days_to_rediffuse},
            {"label": "Deadline de deblocage du projet", "value": obj.days_to_lock_project},
            {"label": "Nombre de fois de deblocage du projet", "value": obj.times_to_unlock_project},
            {"label": "Intervention manuelle admin", "value": obj.days_for_admin_management},
            {"label": "Heure de relance", "value": obj.email_sending_hour.strftime("%H:%M")},
        ]
