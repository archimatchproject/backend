"""
Module containing the serializer for the OfficeRequest model.

This module defines the serializer for the OfficeRequest model to facilitate
conversion between model instances and JSON representations.

Classes:
    OfficeRequestSerializer: Serializer for the OfficeRequest model.
"""

from rest_framework import serializers

from app.architect_request.models.OfficeRequest import OfficeRequest

from app.core.serializers.NoteSerializer import NoteSerializer


class OfficeRequestInputSerializer(serializers.ModelSerializer):
    """
    Serializer for the OfficeRequest model.

    Converts OfficeRequest instances to JSON.

    Meta:
        model (OfficeRequest): The model to be serialized.
        fields (list): The fields to be included in the serialization.
    """

    date = serializers.DateField()
    time_slot = serializers.CharField(source="get_time_slot_display")

    class Meta:
        """
        Meta class for OfficeRequestInputSerializer.

        Meta Attributes:
            model (OfficeRequest): The model to be serialized.
            fields (list): The fields to be included in the serialization.
        """

        model = OfficeRequest
        fields = [
            "id",
            "office_name",
            "phone_number",
            "office_address",
            "email",
            "date",
            "time_slot",
            "city",
        ]


class OfficeRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the OfficeRequest model.

    Converts OfficeRequest instances to JSON.

    Meta:
        model (OfficeRequest): The model to be serialized.
        fields (list): The fields to be included in the serialization.
    """

    meeting_responsable = serializers.EmailField(
        source="meeting_responsable.user.email", read_only=True
    )
    notes = NoteSerializer(many=True)

    class Meta:
        """
        Meta class for OfficeRequestSerializer.

        Meta Attributes:
            model (OfficeRequest): The model to be serialized.
            fields (list): The fields to be included in the serialization.
        """

        model = OfficeRequest
        fields = [
            "id",
            "office_name",
            "phone_number",
            "office_address",
            "office_identifier",
            "email",
            "date",
            "time_slot",
            "meeting_responsable",
            "status",
            "notes",
            "city",
        ]
