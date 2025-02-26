"""
Serializer module for the OfficeReportArchitect model.
"""

from rest_framework import serializers

from app.moderation.models import OfficeReportArchitect
from app.moderation.models import Reason
from app.moderation.serializers.ReasonSerializer import ReasonSerializer
from app.users.models import Architect
from app.users.serializers import ArchitectSerializer
from app.users.serializers import OfficeSerializer


class OfficeReportArchitectSerializer(serializers.ModelSerializer):
    """
    Serializer for the OfficeReportArchitect model.

    Attributes:
        reported_architect_id (PrimaryKeyRelatedField): ID of the reported architect (write-only).
        reported_architect (ArchitectSerializer): Details of the reported architect (read-only).
        reporting_office (OfficeSerializer): Details of the reporting office (read-only).
        reasons (PrimaryKeyRelatedField): List of reasons for the report (write-only).
        report_reasons (ReasonSerializer): Detailed reasons for the report (read-only).
        status (ChoiceField): Status of the report (read/write).
        decision (SlugRelatedField): Decision related to the report (read-only).
    """

    reported_architect_id = serializers.PrimaryKeyRelatedField(queryset=Architect.objects.all(), write_only=True)
    reported_architect = ArchitectSerializer(read_only=True)
    reporting_office = OfficeSerializer(read_only=True)
    report_reasons = serializers.PrimaryKeyRelatedField(queryset=Reason.objects.all(), many=True, write_only=True)
    reasons = ReasonSerializer(read_only=True, many=True)
    decision = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = OfficeReportArchitect
        fields = [
            "id",
            "reported_architect_id",
            "reported_architect",
            "reporting_office",
            "reasons",
            "comments",
            "report_reasons",
            "status",
            "decision",
            "decision_date",
            "created_at",
        ]
        read_only_fields = ["created_at", "decision_date"]
