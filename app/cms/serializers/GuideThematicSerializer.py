"""
Serializer for GuideThematic model.

This module defines the serializer for the GuideThematic model,
providing serialization and deserialization functionality,
including related GuideArticle instances.
"""

from rest_framework import serializers

from app.cms.models.GuideThematic import GuideThematic
from app.cms.serializers.GuideArticleSerializer import GuideArticleSerializer


class GuideThematicSerializer(serializers.ModelSerializer):
    """
    Serializer for GuideThematic model.

    Provides fields for serialization and deserialization of GuideThematic instances,
    including related GuideArticle instances.
    """

    guide_thematic_articles = GuideArticleSerializer(many=True, read_only=True)
    admin = serializers.StringRelatedField()

    class Meta:
        """
        Meta class for GuideThematicSerializer.

        Specifies the model and fields to be included in the serialization.
        """

        model = GuideThematic
        fields = [
            "id",
            "title",
            "sub_title",
            "target_user_type",
            "icon",
            "admin",
            "visible",
            "updated_at",
            "guide_thematic_articles",
        ]
        read_only_fields = ["updated_at", "target_user_type"]
