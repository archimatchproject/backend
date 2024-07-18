"""
Serializers for handling BlogSection model instances.
"""

from rest_framework import serializers

from app.cms.models.BlogSection import BlogSection
from app.cms.serializers.SliderImageSerializer import SliderImageSerializer


class BlogSectionSerializer(serializers.ModelSerializer):
    """
    Serializer for the BlogSection model.

    This serializer handles the serialization and deserialization of BlogSection instances,
    including fields such as id, section_type, content, image, and slider_images.

    """

    slider_images = SliderImageSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = BlogSection
        fields = [
            "id",
            "section_type",
            "content",
            "image",
            "slider_images",
        ]

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
            representation.pop("slider_images", None)
        if instance.section_type != "image":
            representation.pop("image", None)
        if instance.section_type not in [
            "title",
            "paragraph",
        ]:
            representation.pop("content", None)

        return representation
