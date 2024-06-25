"""
Serializer module for AnnouncementPieceRenovate model.

This module defines a serializer class for the AnnouncementPieceRenovate model.

"""

from rest_framework import serializers

from app.announcement.models.AnnouncementPieceRenovate import AnnouncementPieceRenovate
from app.announcement.serializers.PieceRenovateSerializer import PieceRenovateSerializer


class AnnouncementPieceRenovateSerializer(serializers.ModelSerializer):
    """
    Serializer class for AnnouncementPieceRenovate model.
    """

    piece_renovate = PieceRenovateSerializer()

    class Meta:
        """
        Meta class for AnnouncementPieceRenovateSerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """

        model = AnnouncementPieceRenovate
        fields = ["piece_renovate", "number"]
