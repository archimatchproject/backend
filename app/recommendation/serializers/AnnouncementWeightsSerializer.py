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
        model = AnnouncementWeights
        fields = [
            "architectural_style",
            "work_type",
            "project_category",
            "property_type",
            "needs_per_match",
        ]
