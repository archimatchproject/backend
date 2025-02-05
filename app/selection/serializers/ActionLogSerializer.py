"""
This module defines the serializer for the ActionLog model, allowing
the conversion of ActionLog instances to JSON format and vice versa.
"""

from rest_framework import serializers
from app.selection.models.ActionLog import ActionLog
from app.users.serializers.AdminSerializer import AdminSerializer


class ActionLogSerializer(serializers.ModelSerializer):
    """
    Serializer for the ActionLog model. Converts ActionLog instances
    to JSON for API responses and validates input data for creating or
    updating ActionLog entries.
    """
    admin = AdminSerializer()
    class Meta:
        """
        Metadata options for the ActionLogSerializer.
        Defines the model to serialize and the fields to include.
        """
        model = ActionLog
        fields = ['id', 'admin', 'action', 'timestamp', 'details']
        read_only_fields = ['id', 'timestamp']



    def validate_action(self, value):
        """
        Validate the action field to ensure it is one of the defined choices.

        :param value: The action value to validate.
        :return: The validated value if valid.
        :raises serializers.ValidationError: If the action is not a valid choice.
        """
        valid_actions = dict(ActionLog.ACTION_CHOICES).keys()
        if value not in valid_actions:
            raise serializers.ValidationError(f"Invalid action: {value}.")
        return value
