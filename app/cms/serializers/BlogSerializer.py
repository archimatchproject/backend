from rest_framework import serializers

from app.cms.models import Block, Blog
from app.cms.serializers.utils.BlockSerializer import BlockSerializer


class BlogInputSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True)

    class Meta:
        model = Blog
        fields = ["id", "title", "cover_photo", "blocks"]

    def create(self, validated_data):
        blocks_data = validated_data.pop("blocks", [])
        blog = Blog.objects.create(**validated_data)

        for block_data in blocks_data:
            Block.objects.create(blog=blog, **block_data)

        return blog

    def update(self, instance, validated_data):
        blocks_data = validated_data.pop("blocks", [])

        instance.title = validated_data.get("title", instance.title)
        instance.cover_photo = validated_data.get("cover_photo", instance.cover_photo)
        instance.save()

        instance.blocks.all().delete()
        for block_data in blocks_data:
            Block.objects.create(blog=instance, **block_data)

        return instance


class BlogOutputSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ["id", "title", "cover_photo", "blocks"]


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "cover_photo", "blocks"]

    def to_representation(self, instance):
        serializer = BlogOutputSerializer(instance)
        return serializer.data

    def to_internal_value(self, data):
        serializer = BlogInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def create(self, validated_data):
        input_serializer = BlogInputSerializer()
        return input_serializer.create(validated_data)

    def update(self, instance, validated_data):
        input_serializer = BlogInputSerializer()
        return input_serializer.update(instance, validated_data)
