"""
Serializer module for the ArchitectReport model.
"""

from rest_framework import serializers

from app.moderation.models.ArchitectReport import ArchitectReport
from app.moderation.models.Reason import Reason
from app.moderation.serializers.ReasonSerializer import ReasonSerializer
from app.users.models.Architect import Architect
from app.users.serializers.ArchitectSerializer import ArchitectSerializer
from app.users.serializers.ClientSerializer import ClientSerializer


class ArchitectReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the ArchitectReport model.

    Attributes:
        reported_architect_id (PrimaryKeyRelatedField): ID of the reported architect (write-only).
        reported_architect (ArchitectSerializer): Details of the reported architect (read-only).
        reasons (PrimaryKeyRelatedField): List of reasons for the report (write-only).
        report_reasons (ReasonSerializer): Detailed reasons for the report (read-only).
        status (ChoiceField): Status of the report (read/write).
        decision (SlugRelatedField): Decision related to the report (read-only).
    """

    reported_architect_id = serializers.PrimaryKeyRelatedField(
        queryset=Architect.objects.all(), write_only=True
    )
    reported_architect = ArchitectSerializer(read_only=True)
    reporting_client = ClientSerializer(read_only=True)
    reasons = serializers.PrimaryKeyRelatedField(
        queryset=Reason.objects.all(), many=True, write_only=True
    )
    report_reasons = ReasonSerializer(read_only=True, many=True)
    decision = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = ArchitectReport
        fields = [
            "id",
            "reported_architect_id",
            "reported_architect",
            "reporting_client",
            "reasons",
            "report_reasons",
            "status",
            "decision",
            "created_at",
        ]
        read_only_fields = ["created_at"]
