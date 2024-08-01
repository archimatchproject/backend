"""
Serializer for the Collection model.
"""

from rest_framework import serializers

from app.catalogue.models.Collection import Collection
from app.catalogue.serializers.ProductSerializer import ProductSerializer


class CollectionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Collection model.

    This serializer provides a JSON representation of the Collection model,
    including fields for title, category, and related products.
    """

    products = ProductSerializer(many=True, read_only=True, source="product_set")
    category_label = serializers.SerializerMethodField(read_only=True)
    supplier = serializers.EmailField(source="supplier.user.email", read_only=True)

    class Meta:
        """
        Meta class for Collection Serializer.
        """

        model = Collection
        fields = ["id", "title", "category", "category_label", "products", "supplier"]
        extra_kwargs = {
            "category": {"write_only": True},
        }

    def get_category_label(self, obj):
        """
        Get the label of the category to which the collection belongs.

        Args:
            obj (Collection): The collection instance.

        Returns:
            str: The label of the category.
        """
        return obj.category.label if obj.category else None
