"""
This module contains serializers for the QuoteArticle model.
The serializers defined in this module are used to convert QuoteArticle model instances
to JSON format and to validate input data for creating or updating QuoteArticle instances.
Classes:
- QuoteArticleSerializer: Serializer for the QuoteArticle model, including nested
    representations of related Unit and Category models.
- QuoteArticleCreateSerializer: Serializer for creating a new QuoteArticle instance,
    using primary key references for related Unit and Category models.
"""

from rest_framework import serializers

from app.quote.models.QuoteArticle import QuoteArticle
from app.users.serializers.ArchitectSerializer import ArchitectSerializer


class QuoteArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the QuoteArticle model.

    This serializer is used to represent the QuoteArticle model in the response and
    to validate input data for creating or updating a QuoteArticle instance.
    """

    architect = ArchitectSerializer()

    class Meta:
        """
        Meta class for QuoteArticleSerializer.
        Attributes:
            model (type): The model class that is being serialized.
            fields (list): A list of field names to be included in the serialization.
        """

        model = QuoteArticle
        fields = ["id", "title", "description", "byDefault", "architect"]


class QuoteArticleInputSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new QuoteArticle.

    This serializer validates and serializes data for creating a new QuoteArticle instance.
    """

    class Meta:
        """
        Meta class for QuoteArticleSerializer.
        Attributes:
            model (QuoteArticle): The model that is being serialized.
            fields (list): List of fields to be included in the serialization.
        """

        model = QuoteArticle
        fields = ["title", "description", "byDefault"]
