"""
Module containing the TerrainSurface serializer.

This module defines the serializer for the TerrainSurface model, which converts
the model instances to and from JSON format for API communication.

Serializers:
    TerrainSurfaceSerializer: Serializer for the TerrainSurface model.
"""

from rest_framework import serializers

from app.core.models.TerrainSurface import TerrainSurface


class TerrainSurfaceSerializer(serializers.ModelSerializer):
    """
    Serializer for the TerrainSurface model.

    Serializes TerrainSurface model instances to and from JSON format.
    """

    class Meta:
        """
        Meta class for TerrainSurfaceSerializer.

        Defines the model and fields to be included in the serialization.

        Attributes:
            model (TerrainSurface): The model class associated with this serializer.
            fields (list): List of fields to be included in the serialized representation.
        """

        model = TerrainSurface
        fields = ["id", "name"]
