from rest_framework import serializers

from app.announcement.models import Announcement
from app.announcement.models.utils.AnnouncementWorkType import AnnouncementWorkType
from app.announcement.models.utils.ArchitectSpeciality import ArchitectSpeciality
from app.announcement.models.utils.Need import Need
from app.announcement.models.utils.PieceRenovate import PieceRenovate
from app.announcement.models.utils.ProjectCategory import ProjectCategory
from app.announcement.models.utils.ProjectExtension import ProjectExtension
from app.announcement.models.utils.ProjectImage import ProjectImage
from app.announcement.models.utils.PropertyType import PropertyType
from app.announcement.serializers.utils.AnnouncementWorkTypeSerializer import (
    AnnouncementWorkTypeSerializer,
)
from app.announcement.serializers.utils.ArchitectSpecialitySerializer import (
    ArchitectSpecialitySerializer,
)
from app.announcement.serializers.utils.NeedSerializer import NeedSerializer
from app.announcement.serializers.utils.PieceRenovateSerializer import (
    PieceRenovateSerializer,
)
from app.announcement.serializers.utils.ProjectCategorySerializer import (
    ProjectCategorySerializer,
)
from app.announcement.serializers.utils.ProjectExtensionSerializer import (
    ProjectExtensionSerializer,
)
from app.announcement.serializers.utils.ProjectImageSerializer import (
    ProjectImageSerializer,
)
from app.announcement.serializers.utils.PropertyTypeSerializer import (
    PropertyTypeSerializer,
)
from app.users.models import Client
from app.users.serializers import ClientSerializer


class AnnouncementInputSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    architect_speciality = serializers.PrimaryKeyRelatedField(
        queryset=ArchitectSpeciality.objects.all()
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
    pieces_renovate = serializers.PrimaryKeyRelatedField(
        queryset=PieceRenovate.objects.all(), many=True
    )
    project_extensions = serializers.PrimaryKeyRelatedField(
        queryset=ProjectExtension.objects.all(), many=True
    )
    project_images = serializers.PrimaryKeyRelatedField(
        queryset=ProjectImage.objects.all(), many=True, required=False
    )

    class Meta:
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
        needs_data = validated_data.pop("needs")
        pieces_renovate_data = validated_data.pop("pieces_renovate")
        project_extensions_data = validated_data.pop("project_extensions")
        project_images_data = validated_data.pop("project_images", [])

        announcement = Announcement.objects.create(**validated_data)

        announcement.needs.set(needs_data)
        announcement.pieces_renovate.set(pieces_renovate_data)
        announcement.project_extensions.set(project_extensions_data)
        if project_images_data:
            announcement.project_images.set(project_images_data)

        return announcement

    def update(self, instance, validated_data):
        needs_data = validated_data.pop("needs")
        pieces_renovate_data = validated_data.pop("pieces_renovate")
        project_extensions_data = validated_data.pop("project_extensions")
        project_images_data = validated_data.pop("project_images", [])

        instance.needs.set(needs_data)
        instance.pieces_renovate.set(pieces_renovate_data)
        instance.project_extensions.set(project_extensions_data)
        if project_images_data:
            instance.project_images.set(project_images_data)
        else:
            instance.project_images.clear()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class AnnouncementOutputSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    architect_speciality = ArchitectSpecialitySerializer()
    needs = NeedSerializer(many=True)
    project_category = ProjectCategorySerializer()
    property_type = PropertyTypeSerializer()
    work_type = AnnouncementWorkTypeSerializer()
    pieces_renovate = PieceRenovateSerializer(many=True)
    project_extensions = ProjectExtensionSerializer(many=True)
    project_images = ProjectImageSerializer(many=True, required=False)

    class Meta:
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

    """def to_representation(self, instance):
        data = super().to_representation(instance)
        client_user = instance.client.user
        data["client_user_has_password"] = (client_user.password == "")
        return data"""


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
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
        serializer = AnnouncementOutputSerializer(instance)
        return serializer.data

    def to_internal_value(self, data):
        serializer = AnnouncementInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def create(self, validated_data):
        input_serializer = AnnouncementInputSerializer()
        return input_serializer.create(validated_data)

    def update(self, instance, validated_data):
        input_serializer = AnnouncementInputSerializer()
        return input_serializer.update(instance, validated_data)
