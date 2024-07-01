"""
Serializer module for PropertyType model.

This module defines a serializer class for the PropertyType model.
"""

from rest_framework import serializers

from app.announcement.models.PropertyType import PropertyType


class PropertyTypeSerializer(serializers.ModelSerializer):
    """
    Serializer class for PropertyType model.
    """

    class Meta:
        """
        Meta class for PropertyTypeSerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """

        model = PropertyType
        fields = [
            "id",
            "label",
            "icon",
            "project_category",
        ]
