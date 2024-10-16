"""
Module defining the CookiesPolicySerializer.

This module contains the serializer for the CookiesPolicy model,
which handles the serialization and deserialization of cookies policy data.
"""

from rest_framework import serializers

from app.cms.models.CookiesPolicy import CookiesPolicy


class CookiesPolicySerializer(serializers.ModelSerializer):
    """
    Serializer for the CookiesPolicy model.

    This serializer handles the conversion of CookiesPolicy model instances
    to and from JSON format, making it suitable for API interactions.
    """

    admin = serializers.EmailField(source="admin.user.email", read_only=True)

    class Meta:
        """
        Meta class for CookiesPolicySerializer.

        Specifies the model and fields to be included in the serialization.
        """

        model = CookiesPolicy
        fields = ["id", "content", "admin", "updated_at"]
        read_only_fields = ["admin"]
