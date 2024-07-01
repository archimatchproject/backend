"""
Module containing the serializer for the ArchitectRequest model.

This module defines the serializer for the ArchitectRequest model to facilitate
conversion between model instances and JSON representations.

Classes:
    ArchitectRequestSerializer: Serializer for the ArchitectRequest model.
"""

from rest_framework import serializers

from app.announcement.serializers.ArchitectSpecialitySerializer import ArchitectSpecialitySerializer
from app.architect_request.models.ArchitectRequest import ArchitectRequest
from app.core.models.ArchitectSpeciality import ArchitectSpeciality


class ArchitectRequestInputSerializer(serializers.ModelSerializer):
    """
    Serializer for the ArchitectRequest model.

    Converts ArchitectRequest instances to JSON.

    Meta:
        model (ArchitectRequest): The model to be serialized.
        fields (list): The fields to be included in the serialization.
    """

    architect_speciality = serializers.PrimaryKeyRelatedField(
        queryset=ArchitectSpeciality.objects.all()
    )

    class Meta:
        """
        Meta class for ArchitectRequestInputSerializer.

        Meta Attributes:
            model (ArchitectRequest): The model to be serialized.
            fields (list): The fields to be included in the serialization.
        """

        model = ArchitectRequest
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "architect_identifier",
            "email",
            "architect_speciality",
            "date",
            "time_slot",
        ]


class ArchitectRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the ArchitectRequest model.

    Converts ArchitectRequest instances to JSON.

    Meta:
        model (ArchitectRequest): The model to be serialized.
        fields (list): The fields to be included in the serialization.
    """

    architect_speciality = ArchitectSpecialitySerializer(read_only=True)

    class Meta:
        """
        Meta class for ArchitectRequestSerializer.

        Meta Attributes:
            model (ArchitectRequest): The model to be serialized.
            fields (list): The fields to be included in the serialization.
        """

        model = ArchitectRequest
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "architect_identifier",
            "email",
            "architect_speciality",
            "date",
            "time_slot",
        ]
