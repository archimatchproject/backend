"""
Serializer module for the ClientReview model.
"""

from rest_framework import serializers

from app.moderation.models.ClientReview import ClientReview
from app.users.models.Architect import Architect
from app.users.serializers.ArchitectSerializer import ArchitectSerializer
from app.users.serializers.ClientSerializer import ClientSerializer


class ClientReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the ClientReview model.

    Attributes:
        architect (ArchitectSerializer): Details of the architect being reviewed (read-only).
        client (ClientSerializer): Details of the client who wrote the review (read-only).
        rating (FloatField): Rating given by the client (read/write).
        comment (TextField): Review comment provided by the client (read/write).
    """

    architect_id = serializers.PrimaryKeyRelatedField(
        queryset=Architect.objects.all(), write_only=True
    )
    architect = ArchitectSerializer(read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = ClientReview
        fields = ["id", "architect_id", "architect", "client", "rating", "comment"]
