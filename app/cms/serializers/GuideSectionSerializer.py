"""
Serializer for GuideSection model.

This module defines the serializer for the GuideSection model,
providing serialization and deserialization functionality.
"""

from rest_framework import serializers

from app.cms.models.GuideSection import GuideSection
from app.cms.serializers.GuideSliderImageSerializer import GuideSliderImageSerializer


class GuideSectionSerializer(serializers.ModelSerializer):
    """
    Serializer for GuideSection model.

    Provides fields for serialization and deserialization of GuideSection instances.
    """

    section_slider_images = GuideSliderImageSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class for GuideSectionSerializer.

        Specifies the model and fields to be included in the serialization.
        """

        model = GuideSection
        fields = [
            "id",
            "guide_article",
            "section_type",
            "content",
            "image",
            "section_slider_images",
            "video",
        ]
        read_only_fields = ["guide_article"]

    def to_representation(self, instance):
        """
        Customizes the serialized representation based on the section_type.

        Args:
            instance (BlogSection): Instance of the BlogSection model.

        Returns:
            dict: Serialized representation of the BlogSection instance.
        """
        representation = super().to_representation(instance)

        # Conditionally exclude fields based on section_type
        if instance.section_type != "slider":
            representation.pop("section_slider_images", None)
        if instance.section_type != "image":
            representation.pop("image", None)
        if instance.section_type != "video":
            representation.pop("video", None)
        if instance.section_type not in [
            "title",
            "paragraph",
        ]:
            representation.pop("content", None)

        return representation
