"""
Serializer module for Need model.

This module defines a serializer class for the Need model.
"""

from rest_framework import serializers

from app.announcement.models.Need import Need


class NeedSerializer(serializers.ModelSerializer):
    """
    Serializer class for Need model.
    """

    class Meta:
        """
        Meta class for NeedSerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """

        model = Need
        fields = [
            "id",
            "label",
            "icon",
            "description",
            "architect_speciality",
        ]
