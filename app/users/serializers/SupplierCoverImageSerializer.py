"""
Module for serializing SupplierCoverImage instances using Django REST Framework serializers.
"""

from rest_framework import serializers

from app.users.models.SupplierCoverImage import SupplierCoverImage


class SupplierCoverImageSerializer(serializers.ModelSerializer):
    """
    Serializer for SupplierCoverImage instances.
    """

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = SupplierCoverImage
        fields = ["id", "image"]
