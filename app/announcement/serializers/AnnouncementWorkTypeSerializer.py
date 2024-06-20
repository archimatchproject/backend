"""
Serializer module for ArchitectWorkType model.

This module defines a serializer class for the ArchitectWorkType model.
"""
from rest_framework import serializers

from app.announcement.models.AnnouncementWorkType import AnnouncementWorkType


class AnnouncementWorkTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the AnnouncementWorkType model.

    This serializer handles the representation of AnnouncementWorkType instances,
    including validation and conversion between Python objects and JSON.
    """

    class Meta:
        """
        Meta class for AnnouncementWorkTypeSerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """

        model = AnnouncementWorkType
        fields = ["id", "header", "description"]
