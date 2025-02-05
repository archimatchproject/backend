"""
Module containing SupplierSocialMediaSerializer class.

This module provides a serializer for the SupplierSocialMedia model.

Classes:
    SupplierSocialMediaSerializer: Serializer for the SupplierSocialMedia model.
"""

from rest_framework import serializers

from app.users.models.SupplierSocialMedia import SupplierSocialMedia


class SupplierSocialMediaSerializer(serializers.ModelSerializer):
    """
    Serializer for the SupplierSocialMedia model.

    Fields:
        All fields of the SupplierSocialMedia model.
    """

    class Meta:
        """
        Meta class for SupplierSocialMediaSerializer.

        Meta Attributes:
            model: The model that this serializer is associated with.
            fields: The fields to include in the serialized representation.
        """

        model = SupplierSocialMedia
        fields = "__all__"
