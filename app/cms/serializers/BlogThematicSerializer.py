"""
Module for serializing BlogThematic instances using Django REST Framework serializers.
"""

from rest_framework import serializers

from app.cms.models.BlogThematic import BlogThematic
from app.cms.serializers.BlogSerializer import BlogSerializer


class BlogThematicSerializer(serializers.ModelSerializer):
    """
    Serializer for defining request body structure of BlogThematic instances.
    """

    admin = serializers.StringRelatedField()
    blog_thematic_blogs = BlogSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = BlogThematic
        fields = [
            "id",
            "title",
            "admin",
            "visible",
            "target_user_type",
            "updated_at",
            "blog_thematic_blogs",
        ]
        read_only_fields = ["updated_at"]
        extra_kwargs = {
            "target_user_type": {"required": False},
        }
