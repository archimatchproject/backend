"""
Serializer module for the Decision model.
"""

from rest_framework import serializers

from app.moderation.models.Decision import Decision


class DecisionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Decision model.

    Attributes:
        name (CharField): The name or description of the decision.
        report_type (CharField): The type of report this decision applies to.
    """

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = Decision
        fields = ["id", "name", "report_type"]
