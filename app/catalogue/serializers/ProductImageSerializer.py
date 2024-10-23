"""
Serializer for the ProductImage model.
"""

from rest_framework import serializers

from app.catalogue.models.ProductImage import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductImage model.

    This serializer provides a JSON representation of the ProductImage model,
    including fields for product and image.
    """

    class Meta:
        """
        Meta class for ProductImage Serializer.
        """

        model = ProductImage
        fields = ["id", "image"]
