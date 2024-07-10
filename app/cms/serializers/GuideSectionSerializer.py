"""
Serializer for GuideSection model.

This module defines the serializer for the GuideSection model,
providing serialization and deserialization functionality.
"""

from rest_framework import serializers

from app.cms.models.GuideSection import GuideSection


class GuideSectionSerializer(serializers.ModelSerializer):
    """
    Serializer for GuideSection model.

    Provides fields for serialization and deserialization of GuideSection instances.
    """

    class Meta:
        """
        Meta class for GuideSectionSerializer.

        Specifies the model and fields to be included in the serialization.
        """

        model = GuideSection
        fields = ["id", "guide_article", "section_type", "content", "image", "video"]
        read_only_fields = ["guide_article"]
