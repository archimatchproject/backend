"""
Module defining serializers for the Announcement model.

This module contains the AnnouncementInputSerializer, AnnouncementOutputSerializer,
and AnnouncementSerializer classes, which handle the serialization and deserialization
of Announcement instances for API views.
"""

from django.core.exceptions import ValidationError
from django.db import transaction

from rest_framework import serializers

from app.announcement.models import Announcement
from app.announcement.models.AnnouncementPieceRenovate import AnnouncementPieceRenovate
from app.announcement.models.Need import Need
from app.announcement.models.PieceRenovate import PieceRenovate
from app.announcement.models.ProjectExtension import ProjectExtension
from app.announcement.models.ProjectImage import ProjectImage
from app.announcement.serializers.AnnouncementPieceRenovateSerializer import (
    AnnouncementPieceRenovateSerializer,
)
from app.announcement.serializers.ArchitectSpecialitySerializer import (
    ArchitectSpecialitySerializer,
)
from app.announcement.serializers.ArchitecturalStyleSerializer import (
    ArchitecturalStyleSerializer,
)
from app.announcement.serializers.NeedSerializer import NeedSerializer
from app.announcement.serializers.PieceRenovateSerializer import PieceRenovateSerializer
from app.announcement.serializers.ProjectCategorySerializer import (
    ProjectCategorySerializer,
)
from app.announcement.serializers.ProjectExtensionSerializer import (
    ProjectExtensionSerializer,
)
from app.announcement.serializers.ProjectImageSerializer import ProjectImageSerializer
from app.announcement.serializers.PropertyTypeSerializer import PropertyTypeSerializer
from app.announcement.serializers.WorkTypeSerializer import WorkTypeSerializer
from app.core.models.ArchitectSpeciality import ArchitectSpeciality
from app.core.models.ArchitecturalStyle import ArchitecturalStyle
from app.core.models.ProjectCategory import ProjectCategory
from app.core.models.PropertyType import PropertyType
from app.core.models.WorkType import WorkType
from app.users.models import Client
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.serializers import ClientSerializer


class AnnouncementPOSTSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Announcement instances.

    This serializer handles the POST validation and creation/updating
    logic for Announcement instances.

    """

    client = ClientSerializer()
    architect_speciality = serializers.PrimaryKeyRelatedField(
        queryset=ArchitectSpeciality.objects.all()
    )
    architectural_style = serializers.PrimaryKeyRelatedField(
        queryset=ArchitecturalStyle.objects.all()
    )
    needs = serializers.PrimaryKeyRelatedField(queryset=Need.objects.all(), many=True)
    project_category = serializers.PrimaryKeyRelatedField(
        queryset=ProjectCategory.objects.all()
    )
    property_type = serializers.PrimaryKeyRelatedField(
        queryset=PropertyType.objects.all()
    )
    work_type = serializers.PrimaryKeyRelatedField(queryset=WorkType.objects.all())
    pieces_renovate = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(required=True), allow_empty=False
        )
    )
    project_extensions = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExtension.objects.all(), many=True
    )
    project_images = serializers.ListField(
        child=serializers.ImageField(required=False), required=False
    )

    class Meta:
        """
        Meta class for Announcement Serializer.

        Defines display fields.
        """

        model = Announcement
        fields = [
            "client",
            "architect_speciality",
            "needs",
            "project_category",
            "property_type",
            "work_type",
            "pieces_renovate",
            "address",
            "city",
            "terrain_surface",
            "work_surface",
            "budget",
            "description",
            "architectural_style",
            "project_extensions",
            "project_images",
        ]


class AnnouncementPUTSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Announcement instances.

    This serializer handles the PUT validation and creation/updating
    logic for Announcement instances.

    """

    architect_speciality = serializers.PrimaryKeyRelatedField(
        queryset=ArchitectSpeciality.objects.all()
    )
    architectural_style = serializers.PrimaryKeyRelatedField(
        queryset=ArchitecturalStyle.objects.all()
    )
    needs = serializers.PrimaryKeyRelatedField(queryset=Need.objects.all(), many=True)
    project_category = serializers.PrimaryKeyRelatedField(
        queryset=ProjectCategory.objects.all()
    )
    property_type = serializers.PrimaryKeyRelatedField(
        queryset=PropertyType.objects.all()
    )
    work_type = serializers.PrimaryKeyRelatedField(queryset=WorkType.objects.all())
    pieces_renovate = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(required=True), allow_empty=False
        )
    )
    project_extensions = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExtension.objects.all(), many=True
    )
    project_images = serializers.ListField(
        child=serializers.ImageField(required=False), required=False
    )

    class Meta:
        """
        Meta class for Announcement Serializer.

        Defines display fields.
        """

        model = Announcement
        fields = [
            "architect_speciality",
            "needs",
            "project_category",
            "property_type",
            "work_type",
            "pieces_renovate",
            "address",
            "city",
            "terrain_surface",
            "work_surface",
            "budget",
            "description",
            "architectural_style",
            "project_extensions",
            "project_images",
        ]


class AnnouncementOutputSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving Announcement instances.

    This serializer handles the output representation of Announcement instances,
    including related fields serialized with their respective serializers.
    """

    client = ClientSerializer()
    architect_speciality = ArchitectSpecialitySerializer()
    architectural_style = ArchitecturalStyleSerializer()
    needs = NeedSerializer(many=True)
    project_category = ProjectCategorySerializer()
    property_type = PropertyTypeSerializer()
    work_type = WorkTypeSerializer()
    pieces_renovate = AnnouncementPieceRenovateSerializer(many=True)
    project_extensions = ProjectExtensionSerializer(many=True)
    project_images = ProjectImageSerializer(many=True, required=False)

    class Meta:
        """
        Meta class for Announcement Serializer.

        Defines display fields.
        """

        model = Announcement
        fields = [
            "id",
            "client",
            "architect_speciality",
            "needs",
            "project_category",
            "property_type",
            "work_type",
            "pieces_renovate",
            "address",
            "city",
            "terrain_surface",
            "work_surface",
            "budget",
            "description",
            "architectural_style",
            "project_extensions",
            "project_images",
        ]


class AnnouncementSerializer(serializers.ModelSerializer):
    """
    Combined serializer for Announcement instances.

    This serializer combines both input and output serializers for Announcement instances,
    providing methods for converting between internal and external representations.

    """

    class Meta:
        """
        Meta class for Announcement Serializer.

        Defines display fields.
        """

        model = Announcement
        fields = [
            "id",
            "client",
            "architect_speciality",
            "needs",
            "project_category",
            "property_type",
            "work_type",
            "pieces_renovate",
            "address",
            "city",
            "terrain_surface",
            "work_surface",
            "budget",
            "description",
            "architectural_style",
            "project_extensions",
            "project_images",
        ]

    def to_representation(self, instance):
        """
        Convert the Announcement instance to an external representation.

        Args:
            instance (Announcement): The Announcement instance to represent.

        Returns:
            dict: The external representation of the announcement.
        """
        serializer = AnnouncementOutputSerializer(instance)
        return serializer.data
