"""
Serializer module for ArchitecturalStyle model.

This module defines a serializer class for the ArchitecturalStyle model.
"""

from rest_framework import serializers

from app.announcement.models.ArchitecturalStyle import ArchitecturalStyle


class ArchitecturalStyleSerializer(serializers.ModelSerializer):
    """
    Serializer class for ArchitecturalStyle model.
    """

    class Meta:
        """
        Meta class for ArchitecturalStyleSerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """

        model = ArchitecturalStyle
        fields = ["id", "label", "icon"]
