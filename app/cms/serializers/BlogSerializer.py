"""
Module for serializing Blog instances with Sections using Django REST Framework serializers.
"""

from rest_framework import serializers

from app.cms.models import Blog
from app.cms.serializers.SectionSerializer import SectionSerializer


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for defining request body structure of Blog instances with Sections.
    """

    blog_sections = SectionSerializer(many=True, read_only=True)
    sections = SectionSerializer(many=True, write_only=True)

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = Blog
        fields = [
            "id",
            "title",
            "cover_photo",
            "blog_sections",
            "sections",
        ]
