"""
Serializer module for RealizationImage model.

This module defines a serializer class for the RealizationImage model.

"""

from rest_framework import serializers

from app.architect_realization.models.RealizationImage import RealizationImage


class RealizationImageSerializer(serializers.ModelSerializer):
    """
    Serializer class for RealizationImage model.
    """

    class Meta:
        """
        Meta class for RealizationImageSerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """

        model = RealizationImage
        fields = ["id", "image"]
