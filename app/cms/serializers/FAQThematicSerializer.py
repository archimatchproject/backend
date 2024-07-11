"""
Module defining the FAQThematicSerializer.

This module contains the FAQThematicSerializer class, which provides
serialization for the FAQThematic model, including its related questions.
"""

from rest_framework import serializers

from app.cms.models.FAQThematic import FAQThematic
from app.cms.serializers.FAQQuestionSerializer import FAQQuestionSerializer


class FAQThematicSerializer(serializers.ModelSerializer):
    """
    Serializer for the FAQThematic model.

    This class provides serialization and deserialization logic for the FAQThematic model,
    including its related FAQQuestion instances.
    """

    faq_thematic_questions = FAQQuestionSerializer(many=True, read_only=True)
    questions = FAQQuestionSerializer(many=True, write_only=True)

    class Meta:
        """
        Meta class for FAQThematicSerializer.

        Defines the model and fields to be included in the serialized representation.
        """

        model = FAQThematic
        fields = ("id", "title", "faq_thematic_questions", "questions")