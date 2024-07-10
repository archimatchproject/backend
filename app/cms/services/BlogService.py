"""
Module containing the service for handling Blog logic.

This module defines the service for handling the business logic and exceptions
related to Blog creation and management.

Classes:
    BlogService: Service class for Blog operations.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app.cms.models.Block import Block
from app.cms.models.Blog import Blog
from app.cms.serializers.BlogSerializer import BlogSerializer


class BlogService:
    """
    Service class for handling Blog operations.

    Handles business logic and exception handling for Blog creation and management.

    Methods:
        create_blog(data): Handles validation and creation of a new Blog.
        update_blog(blog_instance, data, partial=False): Handles updating an existing Blog.
    """

    @classmethod
    def create_blog(cls, data):
        """
        Handles validation and creation of a new Blog.

        Args:
            data (dict): The validated data for creating a Blog instance.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = BlogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        try:
            with transaction.atomic():
                # Create Blog instance
                blog = Blog.objects.create(
                    title=validated_data.get("title"), cover_photo=validated_data.get("cover_photo")
                )

                # Create related blocks if provided
                blocks_data = validated_data.get("blocks", [])
                for block_data in blocks_data:
                    Block.objects.create(blog=blog, **block_data)

                return Response(BlogSerializer(blog).data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating blog {str(e)}")

    @classmethod
    def update_blog(cls, blog_instance, data, partial=False):
        """
        Handles updating an existing Blog.

        Args:
            blog_instance (Blog): The existing Blog instance to update.
            data (dict): The validated data for updating the Blog instance.
            partial (bool): If True, allow partial updating of the Blog instance.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = BlogSerializer(blog_instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                # Update Blog instance
                blog = serializer.save()

                # Clear existing blocks and create new ones if provided
                blog.blog_blocks.all().delete()
                blocks_data = data.get("blocks", [])
                for block_data in blocks_data:
                    Block.objects.create(blog=blog, **block_data)

                return Response(BlogSerializer(blog).data, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating blog {str(e)}")
