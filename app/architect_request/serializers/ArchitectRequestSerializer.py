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
from app.core.models.ArchitecturalStyle import ArchitecturalStyle
from app.core.models.ProjectCategory import ProjectCategory
from app.core.models.PropertyType import PropertyType
from app.core.models.WorkType import WorkType
from app.users.models.Admin import Admin


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
    meeting_responsable = serializers.PrimaryKeyRelatedField(queryset=Admin.objects.all())
    date = serializers.DateField()
    time_slot = serializers.CharField(source="get_time_slot_display")

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
            "meeting_responsable",
            "status",
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
    meeting_responsable = serializers.EmailField(
        source="meeting_responsable.user.email", read_only=True
    )

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
            "meeting_responsable",
            "status",
        ]


class ArchitectAcceptSerializer(serializers.Serializer):
    """
    Serializer for accepting an ArchitectRequest and creating an Architect.

    Meta:
        fields (list): The fields to be included in the serialization.
    """

    project_categories = serializers.PrimaryKeyRelatedField(
        queryset=ProjectCategory.objects.all(), many=True, required=True
    )
    property_types = serializers.PrimaryKeyRelatedField(
        queryset=PropertyType.objects.all(), many=True, required=True
    )
    work_types = serializers.PrimaryKeyRelatedField(
        queryset=WorkType.objects.all(), many=True, required=True
    )
    architectural_styles = serializers.PrimaryKeyRelatedField(
        queryset=ArchitecturalStyle.objects.all(), many=True, required=True
    )

    def validate_project_categories(self, value):
        """
        Validation Methid to verify array not empty
        """
        if not value:
            raise serializers.ValidationError("Project categories cannot be empty.")
        return value

    def validate_property_types(self, value):
        """
        Validation Methid to verify array not empty
        """
        if not value:
            raise serializers.ValidationError("Property types cannot be empty.")
        return value

    def validate_work_types(self, value):
        """
        Validation Methid to verify array not empty
        """
        if not value:
            raise serializers.ValidationError("Work types cannot be empty.")
        return value

    def validate_architectural_styles(self, value):
        """
        Validation Methid to verify array not empty
        """
        if not value:
            raise serializers.ValidationError("Architectural styles cannot be empty.")
        return value

    class Meta:
        """
        Meta class for ArchitectAcceptSerializer.

        Meta Attributes:
            fields (list): The fields to be included in the serialization.
        """

        fields = [
            "project_categories",
            "property_types",
            "work_types",
            "architectural_styles",
        ]
