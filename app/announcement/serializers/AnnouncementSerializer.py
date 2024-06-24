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
from app.announcement.models.AnnouncementWorkType import AnnouncementWorkType
from app.announcement.models.ArchitectSpeciality import ArchitectSpeciality
from app.announcement.models.ArchitecturalStyle import ArchitecturalStyle
from app.announcement.models.Need import Need
from app.announcement.models.PieceRenovate import PieceRenovate
from app.announcement.models.ProjectCategory import ProjectCategory
from app.announcement.models.ProjectExtension import ProjectExtension
from app.announcement.models.ProjectImage import ProjectImage
from app.announcement.models.PropertyType import PropertyType
from app.announcement.serializers.AnnouncementPieceRenovateSerializer import (
    AnnouncementPieceRenovateSerializer,
)
from app.announcement.serializers.AnnouncementWorkTypeSerializer import (
    AnnouncementWorkTypeSerializer,
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
from app.users.models import Client
from app.users.models.ArchimatchUser import ArchimatchUser
from app.users.serializers import ClientSerializer


class AnnouncementInputSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Announcement instances.

    This serializer handles the input validation and creation/updating
    logic for Announcement instances.

    """

    client = ClientSerializer(required=False)
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
    work_type = serializers.PrimaryKeyRelatedField(
        queryset=AnnouncementWorkType.objects.all()
    )
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

    def create(self, validated_data):
        """
        Create a new Announcement instance.

        Args:
            validated_data (dict): Validated data for the announcement.

        Returns:
            Announcement: The created Announcement instance.
        """
        needs_data = validated_data.pop("needs")
        pieces_renovate_data = validated_data.pop("pieces_renovate", [])
        project_extensions_data = validated_data.pop("project_extensions")
        project_images_data = validated_data.pop("project_images", [])

        client_data = validated_data.pop(
            "client", None
        )  # Client data is optional during update

        with transaction.atomic():
            # Create ArchimatchUser instance
            if client_data:
                user_data = client_data.pop("user")
                user_data["username"] = user_data["email"]
                user_data["user_type"] = "Client"
                user_instance = ArchimatchUser.objects.create_user(**user_data)

                # Create Client instance
                client_instance = Client.objects.create(
                    user=user_instance, **client_data
                )
            else:
                client_instance = None

            # Create Announcement instance
            announcement = Announcement.objects.create(
                client=client_instance, **validated_data
            )
            announcement.needs.set(needs_data)

            for piece_data in pieces_renovate_data:
                piece_renovate_id = piece_data["piece_renovate"]
                piece_renovate = PieceRenovate.objects.get(pk=piece_renovate_id)
                AnnouncementPieceRenovate.objects.create(
                    announcement=announcement,
                    piece_renovate=piece_renovate,
                    number=piece_data["number"],
                )

            announcement.project_extensions.set(project_extensions_data)

            for image in project_images_data:
                ProjectImage.objects.create(announcement=announcement, image=image)

        return announcement

    def update(self, instance, validated_data):
        """
        Update an existing Announcement instance.

        Args:
            instance (Announcement): The Announcement instance to update.
            validated_data (dict): Validated data for updating the announcement.

        Returns:
            Announcement: The updated Announcement instance.
        """
        needs_data = validated_data.pop("needs")
        pieces_renovate_data = validated_data.pop("pieces_renovate", [])
        project_extensions_data = validated_data.pop("project_extensions")
        project_images_data = validated_data.pop("project_images", [])

        client_data = validated_data.pop(
            "client", None
        )  # Client data is optional during update

        instance.needs.set(needs_data)

        AnnouncementPieceRenovate.objects.filter(announcement=instance).delete()
        for piece_data in pieces_renovate_data:
            piece_renovate_id = piece_data["piece_renovate"]
            piece_renovate = PieceRenovate.objects.get(pk=piece_renovate_id)
            AnnouncementPieceRenovate.objects.create(
                announcement=instance,
                piece_renovate=piece_renovate,
                number=piece_data["number"],
            )

        instance.project_extensions.set(project_extensions_data)

        ProjectImage.objects.filter(announcement=instance).delete()
        for image in project_images_data:
            ProjectImage.objects.create(announcement=instance, image=image)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


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
    work_type = AnnouncementWorkTypeSerializer()
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

    def to_internal_value(self, data):
        """
        Convert the external data to an internal representation.

        Args:
            data (dict): The external data to convert.

        Returns:
            dict: The internal representation of the data.
        """
        serializer = AnnouncementInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def create(self, validated_data):
        """
        Create a new Announcement instance.

        Args:
            validated_data (dict): The validated data for the announcement.

        Returns:
            Announcement: The created Announcement
            Returns:
            Announcement: The created Announcement instance.
        """
        input_serializer = AnnouncementInputSerializer()
        return input_serializer.create(validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing Announcement instance.

        Args:
            instance (Announcement): The Announcement instance to update.
            validated_data (dict): The validated data for updating the announcement.

        Returns:
            Announcement: The updated Announcement instance.
        """
        input_serializer = AnnouncementInputSerializer()
        return input_serializer.update(instance, validated_data)
