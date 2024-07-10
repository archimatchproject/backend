"""
Module for serializing Blog instances with Blocks using Django REST Framework serializers.
"""

from rest_framework import serializers

from app.cms.models import Blog
from app.cms.serializers.BlockSerializer import BlockSerializer


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for defining request body structure of Blog instances with Blocks.
    """

    blog_blocks = BlockSerializer(many=True, read_only=True)
    blocks = BlockSerializer(many=True, write_only=True)

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = Blog
        fields = [
            "id",
            "title",
            "cover_photo",
            "blog_blocks",
            "blocks",
        ]
