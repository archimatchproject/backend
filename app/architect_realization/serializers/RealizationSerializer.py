"""
Module defining serializers for the Announcement model.

This module contains the AnnouncementInputSerializer, AnnouncementOutputSerializer,
and AnnouncementSerializer classes, which handle the serialization and deserialization
of Announcement instances for API views.
"""

from rest_framework import serializers

from app.announcement.serializers.ArchitecturalStyleSerializer import ArchitecturalStyleSerializer
from app.announcement.serializers.ProjectCategorySerializer import ProjectCategorySerializer
from app.announcement.serializers.ProjectImageSerializer import ProjectImageSerializer
from app.announcement.serializers.WorkTypeSerializer import WorkTypeSerializer
from app.architect_realization.models.Realization import Realization
from app.core.models.ArchitecturalStyle import ArchitecturalStyle
from app.core.models.ProjectCategory import ProjectCategory
from app.core.models.WorkType import WorkType
from app.users.serializers.ArchitectSerializer import ArchitectSerializer


class RealizationPOSTSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Realization instances.

    This serializer handles the POST validation and creation/updating
    logic for Realization instances.

    """

    architectural_style = serializers.PrimaryKeyRelatedField(
        queryset=ArchitecturalStyle.objects.all()
    )
    project_category = serializers.PrimaryKeyRelatedField(queryset=ProjectCategory.objects.all())
    work_type = serializers.PrimaryKeyRelatedField(queryset=WorkType.objects.all())

    realization_images = serializers.ListField(
        child=serializers.ImageField(required=False),
        required=False,
    )

    class Meta:
        """
        Meta class for Realization Serializer.

        Defines display fields.
        """

        model = Realization
        fields = [
            "project_category",
            "work_type",
            "address",
            "city",
            "terrain_surface",
            "work_surface",
            "description",
            "architectural_style",
            "realization_images",
        ]


class RealizationPUTSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Realization instances.

    This serializer handles the PUT validation and creation/updating
    logic for Realization instances.

    """

    architectural_style = serializers.PrimaryKeyRelatedField(
        queryset=ArchitecturalStyle.objects.all()
    )
    project_category = serializers.PrimaryKeyRelatedField(queryset=ProjectCategory.objects.all())
    work_type = serializers.PrimaryKeyRelatedField(queryset=WorkType.objects.all())

    realization_images = serializers.ListField(
        child=serializers.ImageField(required=False),
        required=False,
    )

    class Meta:
        """
        Meta class for Realization Serializer.

        Defines display fields.
        """

        model = Realization
        fields = [
            "project_category",
            "work_type",
            "address",
            "city",
            "terrain_surface",
            "work_surface",
            "description",
            "architectural_style",
            "realization_images",
        ]


class RealizationOutputSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving Realization instances.

    This serializer handles the output representation of Realization instances,
    including related fields serialized with their respective serializers.
    """

    architect = ArchitectSerializer()
    architectural_style = ArchitecturalStyleSerializer()
    project_category = ProjectCategorySerializer()
    work_type = WorkTypeSerializer()
    realization_images = ProjectImageSerializer(many=True, required=False)

    class Meta:
        """
        Meta class for Realization Serializer.

        Defines display fields.
        """

        model = Realization
        fields = [
            "id",
            "architect",
            "project_category",
            "work_type",
            "address",
            "city",
            "terrain_surface",
            "work_surface",
            "description",
            "architectural_style",
            "realization_images",
        ]


class RealizationSerializer(serializers.ModelSerializer):
    """
    Combined serializer for Realization instances.

    This serializer combines both input and output serializers for Realization instances,
    providing methods for converting between internal and external representations.

    """

    class Meta:
        """
        Meta class for Realization Serializer.

        Defines display fields.
        """

        model = Realization
        fields = [
            "id",
            "architect",
            "project_category",
            "work_type",
            "address",
            "city",
            "terrain_surface",
            "work_surface",
            "description",
            "architectural_style",
            "realization_images",
        ]

    def to_representation(self, instance):
        """
        Convert the Realization instance to an external representation.

        Args:
            instance (Realization): The Realization instance to represent.

        Returns:
            dict: The external representation of the Realization.
        """
        serializer = RealizationOutputSerializer(instance)
        return serializer.data
