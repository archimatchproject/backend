"""
Serializers for handling Section model instances.
"""

from rest_framework import serializers

from app.cms.models.Section import Section
from app.cms.serializers.SliderImageSerializer import SliderImageSerializer


class SectionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Section model.

    This serializer handles the serialization and deserialization of Section instances,
    including fields such as id, section_type, content, image, and slider_images.

    """

    slider_images = SliderImageSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = Section
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
            instance (Section): Instance of the Section model.

        Returns:
            dict: Serialized representation of the Section instance.
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
