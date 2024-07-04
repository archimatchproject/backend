"""
Serializer module for PieceRenovate model.

This module defines a serializer class for the PieceRenovate model.

"""

from rest_framework import serializers

from app.announcement.models.PieceRenovate import PieceRenovate


class PieceRenovateSerializer(serializers.ModelSerializer):
    """
    Serializer class for PieceRenovate model.
    """

    class Meta:
        """
        Meta class for PieceRenovateSerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """

        model = PieceRenovate
        fields = ["id", "label", "icon", "property_type"]
