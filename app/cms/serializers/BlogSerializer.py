"""
Module for serializing Blog instances with Blocks using Django REST Framework serializers.
"""

from rest_framework import serializers

from app.cms.models import Block
from app.cms.models import Blog
from app.cms.serializers.BlockSerializer import BlockSerializer


class BlogInputSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Blog instances along with Blocks.
    """

    blog_blocks = BlockSerializer(many=True)

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = Blog
        fields = ["id", "title", "cover_photo", "blog_blocks"]

    def create(self, validated_data):
        """
        Create and return a new Blog instance with associated Blocks.

        Args:
            validated_data (dict): Validated data for creating Blog instance.

        Returns:
            Blog: Created Blog instance.
        """
        blocks_data = validated_data.pop("blocks", [])
        blog = Blog.objects.create(**validated_data)

        for block_data in blocks_data:
            Block.objects.create(blog=blog, **block_data)

        return blog

    def update(self, instance, validated_data):
        """
        Update and return an existing Blog instance with associated Blocks.

        Args:
            instance (Blog): Existing Blog instance to update.
            validated_data (dict): Validated data for updating Blog instance.

        Returns:
            Blog: Updated Blog instance.
        """
        blocks_data = validated_data.pop("blocks", [])

        instance.title = validated_data.get("title", instance.title)
        instance.cover_photo = validated_data.get("cover_photo", instance.cover_photo)
        instance.save()

        instance.blocks.all().delete()
        for block_data in blocks_data:
            Block.objects.create(blog=instance, **block_data)

        return instance


class BlogOutputSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving Blog instances with read-only Blocks data.
    """

    blog_blocks = BlockSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = Blog
        fields = ["id", "title", "cover_photo", "blog_blocks"]


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer combining BlogInputSerializer and BlogOutputSerializer
    for handling input and output of Blog instances.
    """

    class Meta:
        """
        Meta class specifying the model and fields for the serializer.
        """

        model = Blog
        fields = ["id", "title", "cover_photo", "blog_blocks"]

    def to_representation(self, instance):
        """
        Transform Blog instance into a representation using BlogOutputSerializer.

        Args:
            instance (Blog): Blog instance to represent.

        Returns:
            dict: Represented data of Blog instance.
        """
        serializer = BlogOutputSerializer(instance)
        return serializer.data

    def to_internal_value(self, data):
        """
        Validate input data and return validated data using BlogInputSerializer.

        Args:
            data (dict): Data to validate for creating/updating Blog instance.

        Returns:
            dict: Validated data for creating/updating Blog instance.
        """
        serializer = BlogInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def create(self, validated_data):
        """
        Create and return a new Blog instance using BlogInputSerializer.

        Args:
            validated_data (dict): Validated data for creating Blog instance.

        Returns:
            Blog: Created Blog instance.
        """
        input_serializer = BlogInputSerializer()
        return input_serializer.create(validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Blog instance using BlogInputSerializer.

        Args:
            instance (Blog): Existing Blog instance to update.
            validated_data (dict): Validated data for updating Blog instance.

        Returns:
            Blog: Updated Blog instance.
        """
        input_serializer = BlogInputSerializer()
        return input_serializer.update(instance, validated_data)
