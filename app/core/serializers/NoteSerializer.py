"""
This module contains the serializers for the Note model.

It provides functionality to convert Note instances to JSON format
for use in API responses.
"""

from rest_framework import serializers

from app.core.models.Note import Note


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Note model.

    Converts Note instances to JSON, including the fields id, message, and created_at.
    """

    class Meta:
        """
        Meta class for NoteSerializer.

        Specifies the model and the fields to be included in the serialization.

        Attributes:
            model (Note): The model to be serialized.
            fields (list): The fields to be included in the serialization.
        """

        model = Note
        fields = ["id", "message", "created_at"]
