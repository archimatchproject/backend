"""
Serializer module for the OfficeReview model.
"""

from rest_framework import serializers

from app.moderation.models import OfficeReview
from app.users.models import Architect
from app.users.serializers.OfficeSerializer import OfficeSerializer


class OfficeReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the OfficeReview model.

    Attributes:
        architect_id (PrimaryKeyRelatedField): ID of the architect being reviewed (write-only).
        office (OfficeSerializer): Details of the office that wrote the review (read-only).
        rating (IntegerField): Rating given by the office (read/write).
        comment (TextField): Review comment provided by the office (read/write).
    """

    architect_id = serializers.PrimaryKeyRelatedField(queryset=Architect.objects.all(), write_only=True)
    office = OfficeSerializer(read_only=True)

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = OfficeReview
        fields = ["id", "architect_id", "office", "rating", "comment", "created_at"]
