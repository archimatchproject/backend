"""
Module defining the PrivacyPolicySerializer.

This module contains the serializer for the PrivacyPolicy model,
which handles the serialization and deserialization of privacy policy data.
"""

from rest_framework import serializers

from app.cms.models.PrivacyPolicy import PrivacyPolicy


class PrivacyPolicySerializer(serializers.ModelSerializer):
    """
    Serializer for the PrivacyPolicy model.

    This serializer handles the conversion of PrivacyPolicy model instances
    to and from JSON format, making it suitable for API interactions.
    """

    admin = serializers.EmailField(source="admin.user.email", read_only=True)

    class Meta:
        """
        Meta class for PrivacyPolicySerializer.

        Specifies the model and fields to be included in the serialization.
        """

        model = PrivacyPolicy
        fields = ["id", "content", "admin", "updated_at"]
        read_only_fields = ["admin"]
