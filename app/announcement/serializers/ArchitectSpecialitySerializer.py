"""
Serializer module for ArchitectSpeciality model.

This module defines a serializer class for the ArchitectSpeciality model.
"""

from rest_framework import serializers

from app.announcement.models.ArchitectSpeciality import ArchitectSpeciality


class ArchitectSpecialitySerializer(serializers.ModelSerializer):
    """
    Serializer class for ArchitectSpeciality model.
    """

    class Meta:
        """
        Meta class for ArchitectSpecialitySerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """

        model = ArchitectSpeciality
        fields = ["id", "label", "icon"]
