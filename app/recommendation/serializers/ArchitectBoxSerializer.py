from rest_framework import serializers
from app.users.models.Architect import Architect
from app.announcement.models.Announcement import Announcement
from app.recommendation.models.ArchitectBox import ArchitectBox
from app.users.serializers.ArchitectSerializer import ArchitectSerializer
from app.announcement.serializers.AnnouncementSerializer import AnnouncementSerializer


class ArchitectBoxPostSerializer(serializers.ModelSerializer):
    """
    Serializer for the ArchitectBox model.

    Attributes:
        architect (PrimaryKeyRelatedField): Associated architect.
        announcements (PrimaryKeyRelatedField): List of associated announcements.
    """

    architect = serializers.PrimaryKeyRelatedField(queryset=Architect.objects.all())
    announcements = serializers.PrimaryKeyRelatedField(
        queryset=Announcement.objects.all(), many=True, required=False
    )

    class Meta:
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
        model = ArchitectBox
        fields = ["id", "architect", "announcements", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]
