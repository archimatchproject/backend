"""
Module defining the TermsAndConditionsSerializer.

This module contains the serializer for the TermsAndConditions model,
which handles the serialization and deserialization of terms & conditions data.
"""

from rest_framework import serializers

from app.cms.models.TermsAndConditions import TermsAndConditions


class TermsAndConditionsSerializer(serializers.ModelSerializer):
    """
    Serializer for the TermsAndConditions model.

    This serializer handles the conversion of TermsAndConditions model instances
    to and from JSON format, making it suitable for API interactions.
    """

    admin = serializers.EmailField(source="admin.user.email", read_only=True)

    class Meta:
        """
        Meta class for TermsAndConditionsSerializer.

        Specifies the model and fields to be included in the serialization.
        """

        model = TermsAndConditions
        fields = ["id", "content", "admin", "updated_at"]
        read_only_fields = ["admin"]
