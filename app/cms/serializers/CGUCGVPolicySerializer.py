"""
Module defining the CGUCGVPolicySerializer.

This module contains the serializer for the CGUCGVPolicy model,
which handles the serialization and deserialization of CGU/CGV policy data.
"""

from rest_framework import serializers
from app.cms.models.CGUCGVPolicy import CGUCGVPolicy


class CGUCGVPolicySerializer(serializers.ModelSerializer):
    """
    Serializer for the CGUCGVPolicy model.

    This serializer handles the conversion of CGUCGVPolicy model instances
    to and from JSON format, making it suitable for API interactions.
    """

    admin = serializers.EmailField(source="admin.user.email", read_only=True)

    class Meta:
        """
        Meta class for CGUCGVPolicySerializer.

        Specifies the model and fields to be included in the serialization.
        """

        model = CGUCGVPolicy
        fields = ["id", "content", "admin", "updated_at"]
        read_only_fields = ["admin"]
