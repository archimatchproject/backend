"""
Module containing the service for handling BlogThematic logic.

This module defines the service for handling the business logic and exceptions
related to BlogThematic creation and management.

Classes:
    BlogThematicService: Service class for BlogThematic operations.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.cms.models.BlogThematic import BlogThematic
from app.cms.serializers.BlogThematicSerializer import BlogThematicSerializer


class BlogThematicService:
    """
    Service class for handling BlogThematic operations.

    Handles business logic and exception handling for BlogThematic creation and management.

    Methods:
        create_blog_thematic(data, user): Handles validation and creation of a new BlogThematic.
        update_blog_thematic(blog_thematic_instance, data, partial=False): Handles updating an
        existing BlogThematic.
    """

    @classmethod
    def create_blog_thematic(cls, data, user):
        """
        Handles validation and creation of a new BlogThematic.

        Args:
            data (dict): The validated data for creating a BlogThematic instance.
            user (User): The user creating the blog thematic, used to set the admin.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = BlogThematicSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            with transaction.atomic():
                # Create BlogThematic instance
                blog_thematic = BlogThematic.objects.create(
                    title=validated_data.get("title"),
                    admin=user.admin,
                    visible=validated_data.get("visible", False),
                )

                return Response(
                    BlogThematicSerializer(blog_thematic).data, status=status.HTTP_201_CREATED
                )

        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating blog thematic: {str(e)}")

    @classmethod
    def update_blog_thematic(cls, instance, data, partial=False):
        """
        Handle the update of an existing BlogThematic instance.

        Args:
            instance (BlogThematic): The existing BlogThematic instance.
            data (dict): The validated data for updating a BlogThematic.
            partial (bool): Whether to perform partial update (default: False).

        Returns:
            Response: The response object containing the updated instance data.
        """
        serializer = BlogThematicSerializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                instance.title = serializer.validated_data.get("title", instance.title)
                instance.visible = serializer.validated_data.get("visible", instance.visible)
                instance.save()

                return Response(BlogThematicSerializer(instance).data, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating blog thematic: {str(e)}")

    @classmethod
    def change_visibility(cls, blog_thematic_id, request):
        """
        Handle the change of visibility for a Blog instance.

        Args:
            blog_thematic_id (int): The primary key of the Blog instance.
            visibility (bool): The new visibility status for the Blog instance.

        Returns:
            Response: The response object containing the updated instance data.
        """
        try:
            visibility = request.data.get("visible")
            if visibility is None:
                raise serializers.ValidationError(detail="Visible field is required.")
            blog_thematic = BlogThematic.objects.get(pk=blog_thematic_id)
            blog_thematic.visible = visibility
            blog_thematic.save()
            return Response(BlogThematicSerializer(blog_thematic).data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            raise e
        except BlogThematic.DoesNotExist:
            raise NotFound(detail="Blog not found.")
        except Exception as e:
            raise APIException(detail=f"Error changing visibility: {str(e)}")
