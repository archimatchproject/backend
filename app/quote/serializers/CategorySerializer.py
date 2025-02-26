"""
CategorySerializer
This module defines the CategorySerializer class, which is a serializer for the Category model.
It is used to represent the Category model in API responses and to validate input data
for creating or updating a Category instance.
Classes:
    CategorySerializer: A serializer for the Category model.

"""

from rest_framework import serializers

from app.quote.models.Category import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    This serializer is used to represent the Category model in the response and to
    validate input data for creating or updating a Category instance.
    """

    class Meta:
        """
        Meta class for CategorySerializer.
        Attributes:
            model (Model): The model that is being serialized.
            fields (list): The list of fields to be included in the serialization.
        """

        model = Category
        fields = ["id", "title"]
