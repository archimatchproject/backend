"""
Serializer module for the Reason model.
"""

from rest_framework import serializers

from app.moderation.models.Reason import Reason


class ReasonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Reason model.

    Attributes:
        name (CharField): The name or description of the reason.
        report_type (CharField): The type of report this reason applies to.
    """

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = Reason
        fields = ["id", "name", "report_type"]
