"""
Module defining the FAQQuestionSerializer.

This module contains the FAQQuestionSerializer class, which provides
serialization for the FAQQuestion model.
"""

from rest_framework import serializers

from app.cms.models.FAQQuestion import FAQQuestion


class FAQQuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for the FAQQuestion model.

    This class provides serialization and deserialization logic for the FAQQuestion model.
    """

    class Meta:
        """
        Meta class for FAQQuestionSerializer.

        Defines the model and fields to be included in the serialized representation.
        """

        model = FAQQuestion
        fields = ("id", "question", "response")
