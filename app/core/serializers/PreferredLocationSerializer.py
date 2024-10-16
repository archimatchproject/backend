"""
Module containing the PreferredLocation serializer.

This module defines the serializer for the PreferredLocation model, which converts
the model instances to and from JSON format for API communication.

Serializers:
    PreferredLocationSerializer: Serializer for the PreferredLocation model.
"""

from rest_framework import serializers

from app.core.models.PreferredLocation import PreferredLocation


class PreferredLocationSerializer(serializers.ModelSerializer):
    """
    Serializer for the PreferredLocation model.

    Serializes PreferredLocation model instances to and from JSON format.
    """

    class Meta:
        """
        Meta class for PreferredLocationSerializer.

        Defines the model and fields to be included in the serialization.

        Attributes:
            model (PreferredLocation): The model class associated with this serializer.
            fields (list): List of fields to be included in the serialized representation.
        """

        model = PreferredLocation
        fields = ["id", "name"]
