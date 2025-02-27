"""
Module defining the FAQQuestionSerializer.

This module contains the FAQQuestionSerializer class, which provides
serialization for the FAQQuestion model.
"""

from rest_framework import serializers

from app.cms.models.FAQQuestion import FAQQuestion
from app.cms.models.FAQThematic import FAQThematic
from app.cms.models.GuideArticle import GuideArticle
from app.cms.models.GuideThematic import GuideThematic
from app.cms.serializers.GuideArticleSerializer import GuideArticleSerializer
from app.cms.serializers.GuideThematicSerializer import GuideThematicSerializer


class FAQQuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for the FAQQuestion model.

    This class provides serialization and deserialization logic for the FAQQuestion model.
    """

    guide_thematic = GuideThematicSerializer(read_only=True)
    guide_thematic_id = serializers.PrimaryKeyRelatedField(
        source="guide_thematic",
        queryset=GuideThematic.objects.all(),
        write_only=True,
        required=False,
    )
    guide_article = GuideArticleSerializer(read_only=True)
    guide_article_id = serializers.PrimaryKeyRelatedField(
        source="guide_article", queryset=GuideArticle.objects.all(), write_only=True, required=False
    )
    faq_thematic = serializers.SlugRelatedField(read_only=True, slug_field="title")
    faq_thematic_id = serializers.PrimaryKeyRelatedField(
        source="faq_thematic", queryset=FAQThematic.objects.all(), write_only=True
    )
    admin = serializers.EmailField(source="admin.user.email", read_only=True)

    class Meta:
        """
        Meta class for FAQQuestionSerializer.

        Defines the model and fields to be included in the serialized representation.
        """

        model = FAQQuestion
        fields = [
            "id",
            "question",
            "response",
            "admin",
            "faq_thematic",
            "faq_thematic_id",
            "guide_thematic",
            "guide_thematic_id",
            "guide_article",
            "guide_article_id",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]
