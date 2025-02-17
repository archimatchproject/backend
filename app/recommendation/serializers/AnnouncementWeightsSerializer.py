"""
This module contains serializers for the AnnouncementWeights model.
It includes both input and output serializers to handle the serialization
and deserialization of AnnouncementWeights data.
"""

from rest_framework import serializers

from app.recommendation.models import AnnouncementWeights


# Input Serializer for AnnouncementWeights
class AnnouncementWeightsSerializer(serializers.ModelSerializer):
    """Input serializer for AnnouncementWeights model."""

    class Meta:
        """
        Meta class for AnnouncementWeightsSerializer.
        Attributes:
            model (AnnouncementWeights): The model that is being serialized.
            fields (list): A list of fields to be included in the serialization.
                - "architectural_style": The architectural style of the announcement.
                - "work_type": The type of work related to the announcement.
                - "project_category": The category of the project.
                - "property_type": The type of property involved in the announcement.
                - "needs_per_match": The needs per match for the announcement.
        """

        model = AnnouncementWeights
        fields = [
            "architectural_style",
            "work_type",
            "project_category",
            "property_type",
            "needs_per_match",
        ]
