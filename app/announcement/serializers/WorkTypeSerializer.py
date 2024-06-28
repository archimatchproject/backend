"""
Serializer module for ArchitectWorkType model.

This module defines a serializer class for the ArchitectWorkType model.
"""
from rest_framework import serializers

from app.core.models.WorkType import WorkType


class WorkTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the WorkType model.

    This serializer handles the representation of WorkType instances,
    including validation and conversion between Python objects and JSON.
    """

    class Meta:
        """
        Meta class for WorkTypeSerializer.

        Specifies the model to be serialized and the fields to be included in the serialization.
        """

        model = WorkType
        fields = ["id", "header", "description"]
