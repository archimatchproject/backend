"""
Serializers for handling Block model instances.
"""

from rest_framework import serializers

from app.cms.models import Block

from .SliderImageSerializer import SliderImageSerializer


class BlockSerializer(serializers.ModelSerializer):
    """
    Serializer for the Block model.

    This serializer handles the serialization and deserialization of Block instances,
    including fields such as id, block_type, content, image, and slider_images.

    """

    slider_images = SliderImageSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = Block
        fields = [
            "id",
            "block_type",
            "content",
            "image",
            "slider_images",
        ]

    def to_representation(self, instance):
        """
        Customizes the serialized representation based on the block_type.

        Args:
            instance (Block): Instance of the Block model.

        Returns:
            dict: Serialized representation of the Block instance.
        """
        representation = super().to_representation(instance)

        # Conditionally exclude fields based on block_type
        if instance.block_type != "slider":
            representation.pop("slider_images", None)
        if instance.block_type != "image":
            representation.pop("image", None)
        if instance.block_type not in [
            "title",
            "paragraph",
        ]:
            representation.pop("content", None)

        return representation
