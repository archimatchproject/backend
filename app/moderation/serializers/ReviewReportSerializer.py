"""
Serializer module for the ReviewReport model.
"""

from rest_framework import serializers

from app.moderation.models.ClientReview import ClientReview
from app.moderation.models.Reason import Reason
from app.moderation.models.ReviewReport import ReviewReport
from app.moderation.serializers.ClientReviewSerializer import ClientReviewSerializer
from app.moderation.serializers.ReasonSerializer import ReasonSerializer
from app.users.serializers.ArchitectSerializer import ArchitectSerializer


class ReviewReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the ReviewReport model.

    Attributes:
        reported_review_id (PrimaryKeyRelatedField): ID of the reported review (write-only).
        reported_review (ClientReviewSerializer): Details of the reported review (read-only).
        reporting_architect (ArchitectSerializer): Details of the architect reporting the review
          (read-only).
        reasons (PrimaryKeyRelatedField): List of reasons for the report (write-only).
        report_reasons (ReasonSerializer): Detailed reasons for the report (read-only).
        status (ChoiceField): Status of the report (read/write).
        decision (SlugRelatedField): Decision related to the report (read-only).
    """

    reported_review_id = serializers.PrimaryKeyRelatedField(
        queryset=ClientReview.objects.all(), write_only=True
    )
    reported_review = ClientReviewSerializer(read_only=True)
    reporting_architect = ArchitectSerializer(read_only=True)
    reasons = serializers.PrimaryKeyRelatedField(
        queryset=Reason.objects.all(), many=True, write_only=True
    )
    report_reasons = ReasonSerializer(read_only=True, many=True)
    decision = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = ReviewReport
        fields = [
            "id",
            "reported_review_id",
            "reported_review",
            "reporting_architect",
            "reasons",
            "report_reasons",
            "status",
            "decision",
        ]
