"""
Serializer for the Product model.
"""

from rest_framework import serializers

from app.catalogue.models.Product import Product
from app.catalogue.serializers.ProductImageSerializer import ProductImageSerializer


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    This serializer provides a JSON representation of the Product model,
    including fields for name, price, collection, description, and images.
    """

    collection_category = serializers.SerializerMethodField(read_only=True)
    product_images = ProductImageSerializer(many=True, read_only=True)
    collection_title = serializers.CharField(source="collection.title", read_only=True)

    class Meta:
        """
        Meta class for Product Serializer.
        """

        model = Product
        fields = [
            "id",
            "name",
            "price",
            "description",
            "product_images",
            "collection",
            "collection_title",
            "collection_category",
            "order",
            "display",
            "visibility",
        ]
        extra_kwargs = {
            "collection": {"write_only": True},
        }

    def get_collection_category(self, obj):
        """
        Get the category label of the collection to which the product belongs.

        Args:
            obj (Product): The product instance.

        Returns:
            str: The category label of the collection.
        """
        return obj.collection.category.label if obj.collection and obj.collection.category else None
