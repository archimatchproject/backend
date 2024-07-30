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
            "popular",
            "updated_at",
        ]
        read_only_fields = ["blog_sections", "updated_at"]

    def to_internal_value(self, data):
        """
        Method mapping tags and adding those who don't exist
        """
        tags = data.get("tags", [])
        for i, tag in enumerate(tags):
            if isinstance(tag, str):
                tag_obj, created = BlogTag.objects.get_or_create(name=tag)
                tags[i] = tag_obj.name
        data["tags"] = tags
        return super().to_internal_value(data)
