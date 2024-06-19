from rest_framework import serializers

from app.cms.models import Block

from .SliderImageSerializer import SliderImageSerializer


class BlockSerializer(serializers.ModelSerializer):
    slider_images = SliderImageSerializer(many=True, read_only=True)

    class Meta:
        model = Block
        fields = ["id", "block_type", "content", "image", "slider_images"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.block_type != "slider":
            representation.pop("slider_images", None)
        if instance.block_type != "image":
            representation.pop("image", None)
        if instance.block_type not in ["title", "paragraph"]:
            representation.pop("content", None)
        return representation
