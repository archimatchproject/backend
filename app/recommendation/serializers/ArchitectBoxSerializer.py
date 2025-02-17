"""
This module contains serializers for the ArchitectBox model.
Classes:
    ArchitectBoxPostSerializer: Serializer for creating and updating ArchitectBox instances.
    ArchitectBoxSerializer: Serializer for retrieving ArchitectBox instances with nested relationships.
    ArchitectBoxPostSerializer.architect (PrimaryKeyRelatedField): Associated architect.
    ArchitectBoxPostSerializer.announcements (PrimaryKeyRelatedField): List of associated announcements.
    ArchitectBoxSerializer.architect (ArchitectSerializer): Nested serializer for the associated architect.
    ArchitectBoxSerializer.announcements (AnnouncementSerializer): Nested serializer for the associated announcements.
"""

from rest_framework import serializers

from app.announcement.models.Announcement import Announcement
from app.announcement.serializers.AnnouncementSerializer import AnnouncementSerializer
from app.recommendation.models.ArchitectBox import ArchitectBox
from app.users.models.Architect import Architect
from app.users.serializers.ArchitectSerializer import ArchitectSerializer


class ArchitectBoxPostSerializer(serializers.ModelSerializer):
    """
    Serializer for the ArchitectBox model.

    Attributes:
        architect (PrimaryKeyRelatedField): Associated architect.
        announcements (PrimaryKeyRelatedField): List of associated announcements.
    """

    architect = serializers.PrimaryKeyRelatedField(queryset=Architect.objects.all())
    announcements = serializers.PrimaryKeyRelatedField(queryset=Announcement.objects.all(), many=True, required=False)

    class Meta:
        """
        Meta class for ArchitectBoxSerializer.
        Attributes:
            model (type): The model associated with the serializer.
            fields (list): List of fields to be included in the serialized output.
            read_only_fields (list): List of fields that are read-only and cannot be modified.
        """

        model = ArchitectBox
        fields = ["id", "architect", "announcements", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class ArchitectBoxSerializer(serializers.ModelSerializer):
    """
    Serializer for the ArchitectBox model.

    Attributes:
        architect (PrimaryKeyRelatedField): Associated architect.
        announcements (PrimaryKeyRelatedField): List of associated announcements.
    """

    architect = ArchitectSerializer()
    announcements = AnnouncementSerializer(many=True)

    class Meta:
        """
        Meta class for ArchitectBoxSerializer.
        Attributes:
            model (type): The model associated with the serializer.
            fields (list): List of fields to be included in the serialized output.
            read_only_fields (list): List of fields that are read-only and cannot be modified.
        """

        model = ArchitectBox
        fields = ["id", "architect", "announcements", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]
