"""
Serializer module for the SelectionReport model.
"""

from rest_framework import serializers

from app.moderation.models.Reason import Reason
from app.moderation.models.SelectionReport import SelectionReport
from app.moderation.serializers.ReasonSerializer import ReasonSerializer
from app.selection.models.Selection import Selection
from app.selection.serializers.SelectionSerializer import SelectionSerializer
from app.users.serializers.ClientSerializer import ClientSerializer


class SelectionReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the SelectionReport model.

    Attributes:
        reported_selection_id (PrimaryKeyRelatedField): ID of the reported selection (write-only).
        reported_selection (SelectionSerializer): Details of the reported selection (read-only).
        reasons (PrimaryKeyRelatedField): List of reasons for the report (write-only).
        report_reasons (ReasonSerializer): Detailed reasons for the report (read-only).
        status (ChoiceField): Status of the report (read/write).
        decision (SlugRelatedField): Decision related to the report (read-only).
    """

    selection_id = serializers.PrimaryKeyRelatedField(
        queryset=Selection.objects.all(), write_only=True
    )
    selection = SelectionSerializer(read_only=True)
    reporting_client = ClientSerializer(read_only=True)
    report_reasons = serializers.PrimaryKeyRelatedField(
        queryset=Reason.objects.all(), many=True, write_only=True
    )
    reasons = ReasonSerializer(read_only=True, many=True)
    decision = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = SelectionReport
        fields = [
            "id",
            "selection_id",
            "selection",
            "reporting_client",
            "reasons",
            "report_reasons",
            "status",
            "decision",
            "decision_date",
            "created_at",
        ]
        read_only_fields = ["created_at", "decision_date"]
