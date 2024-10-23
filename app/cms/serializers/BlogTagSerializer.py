"""
Module for serializing BlogTag instances with Sections using Django REST Framework serializers.
"""

from rest_framework import serializers

from app.cms.models.BlogTag import BlogTag


class BlogTagSerializer(serializers.ModelSerializer):
    """
    Serializer for BlogTag instances.
    """

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = BlogTag
        fields = ["id", "name"]
