"""
Serializer for GuideArticle model.

This module defines the serializer for the GuideArticle model,
providing serialization and deserialization functionality,
including related GuideSection instances.
"""

from rest_framework import serializers

from app.cms.models.GuideArticle import GuideArticle
from app.cms.serializers.GuideSectionSerializer import GuideSectionSerializer


class GuideArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for GuideArticle model.

    Provides fields for serialization and deserialization of GuideArticle instances,
    including related GuideSection instances.
    """

    guide_article_sections = GuideSectionSerializer(many=True, read_only=True)
    sections = GuideSectionSerializer(many=True, write_only=True)

    class Meta:
        """
        Meta class for GuideArticleSerializer.

        Specifies the model and fields to be included in the serialization.
        """

        model = GuideArticle
        fields = [
            "id",
            "title",
            "description",
            "guide_thematic",
            "date",
            "rating",
            "guide_article_sections",
            "sections",
        ]
