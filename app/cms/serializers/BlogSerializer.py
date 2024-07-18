"""
Module for serializing Blog instances with Sections using Django REST Framework serializers.
"""

from rest_framework import serializers

from app.cms.models.Blog import Blog
from app.cms.models.BlogTag import BlogTag
from app.cms.models.BlogThematic import BlogThematic
from app.cms.serializers.BlogSectionSerializer import BlogSectionSerializer


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for defining request body structure of Blog instances with Sections.
    """

    blog_sections = BlogSectionSerializer(many=True, read_only=True)
    sections = BlogSectionSerializer(many=True, write_only=True)
    blog_thematic = serializers.SlugRelatedField(read_only=True, slug_field="title")
    blog_thematic_id = serializers.PrimaryKeyRelatedField(
        source="blog_thematic", queryset=BlogThematic.objects.all(), write_only=True
    )
    tags = serializers.SlugRelatedField(
        many=True, queryset=BlogTag.objects.all(), slug_field="name"
    )
    admin = serializers.EmailField(source="admin.user.email", read_only=True)

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = Blog
        fields = [
            "id",
            "title",
            "sub_title",
            "cover_photo",
            "blog_sections",
            "sections",
            "blog_thematic",
            "blog_thematic_id",
            "tags",
            "admin",
            "visible",
            "last_update",
        ]
        read_only_fields = ["blog_sections", "last_update"]
