"""
This module contains serializers for the QuoteService model.
The serializers defined in this module are used to convert QuoteService model instances
to JSON format and to validate input data for creating or updating QuoteService instances.
Classes:
- QuoteServiceSerializer: Serializer for the QuoteService model, including nested
    representations of related Unit and Category models.
- QuoteServiceCreateSerializer: Serializer for creating a new QuoteService instance,
    using primary key references for related Unit and Category models.
"""

from rest_framework import serializers

from app.quote.models.Category import Category
from app.quote.models.QuoteService import QuoteService
from app.quote.models.Unit import Unit
from app.quote.serializers.CategorySerializer import CategorySerializer
from app.quote.serializers.UnitSerializer import UnitSerializer


class QuoteServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the QuoteService model.

    This serializer is used to represent the QuoteService model in the response and
    to validate input data for creating or updating a QuoteService instance.
    """

    unit = UnitSerializer()
    category = CategorySerializer()

    class Meta:
        """
        Meta class for QuoteServiceSerializer.
        Attributes:
            model (type): The model class that is being serialized.
            fields (list): A list of field names to be included in the serialization.
        """

        model = QuoteService
        fields = ["id", "title", "description", "unit", "category", "unit_price"]


class QuoteServiceInputSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new QuoteService.

    This serializer validates and serializes data for creating a new QuoteService instance.
    """

    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        """
        Meta class for QuoteServiceSerializer.
        Attributes:
            model (QuoteService): The model that is being serialized.
            fields (list): List of fields to be included in the serialization.
        """

        model = QuoteService
        fields = ["title", "description", "unit", "category", "unit_price"]
