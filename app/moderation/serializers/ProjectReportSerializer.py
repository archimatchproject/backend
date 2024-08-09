"""
Serializer module for the ProjectReport model.
"""

from rest_framework import serializers

from app.announcement.models.Announcement import Announcement
from app.announcement.serializers.AnnouncementSerializer import AnnouncementSerializer
from app.moderation.models.ProjectReport import ProjectReport
from app.moderation.models.Reason import Reason
from app.moderation.serializers.ReasonSerializer import ReasonSerializer
from app.users.serializers.ArchitectSerializer import ArchitectSerializer


class ProjectReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProjectReport model.

    Attributes:
        reported_project_id (PrimaryKeyRelatedField): ID of the reported project (write-only).
        reported_project (AnnouncementSerializer): Details of the reported project (read-only).
        reporting_architect (ArchitectSerializer): Details of the architect reporting the project
          (read-only).
        reasons (PrimaryKeyRelatedField): List of reasons for the report (write-only).
        report_reasons (ReasonSerializer): Detailed reasons for the report (read-only).
        status (ChoiceField): Status of the report (read/write).
        decision (SlugRelatedField): Decision related to the report (read-only).
    """

    reported_project_id = serializers.PrimaryKeyRelatedField(
        queryset=Announcement.objects.all(), write_only=True
    )
    reported_project = AnnouncementSerializer(read_only=True)
    reporting_architect = ArchitectSerializer(read_only=True)
    report_reasons = serializers.PrimaryKeyRelatedField(
        queryset=Reason.objects.all(), many=True, write_only=True
    )
    reasons = ReasonSerializer(read_only=True, many=True)
    decision = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = ProjectReport
        fields = [
            "id",
            "reported_project_id",
            "reported_project",
            "reporting_architect",
            "reasons",
            "report_reasons",
            "status",
            "decision",
        ]
