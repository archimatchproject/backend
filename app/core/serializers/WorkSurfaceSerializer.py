"""
Module containing the WorkSurface serializer.

This module defines the serializer for the WorkSurface model, which converts
the model instances to and from JSON format for API communication.

Serializers:
    WorkSurfaceSerializer: Serializer for the WorkSurface model.
"""

from rest_framework import serializers

from app.core.models.WorkSurface import WorkSurface


class WorkSurfaceSerializer(serializers.ModelSerializer):
    """
    Serializer for the WorkSurface model.

    Serializes WorkSurface model instances to and from JSON format.
    """

    class Meta:
        """
        Meta class for WorkSurfaceSerializer.

        Defines the model and fields to be included in the serialization.

        Attributes:
            model (WorkSurface): The model class associated with this serializer.
            fields (list): List of fields to be included in the serialized representation.
        """

        model = WorkSurface
        fields = ["id", "name"]
