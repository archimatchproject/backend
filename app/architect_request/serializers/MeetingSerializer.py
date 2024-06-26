"""
Module containing the serializer for the Meeting model.

This module defines the serializer for the Meeting model to facilitate
conversion between model instances and JSON representations.

Classes:
    MeetingSerializer: Serializer for the Meeting model.
"""

from rest_framework import serializers

from app.architect_request.models.Meeting import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Meeting model.

    Converts Meeting instances to JSON.

    Meta:
        model (Meeting): The model to be serialized.
        fields (list): The fields to be included in the serialization.
    """

    class Meta:
        """
        Meta class for MeetingSerializer.

        Meta Attributes:
            model (Meeting): The model to be serialized.
            fields (list): The fields to be included in the serialization.
        """

        model = Meeting
        fields = ["id", "date", "time_slot"]
