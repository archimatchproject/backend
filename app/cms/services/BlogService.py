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

from app.cms.models.Blog import Blog
from app.cms.models.Section import Section
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

                # Create related sections if provided
                sections_data = validated_data.get("sections", [])
                for section_data in sections_data:
                    Section.objects.create(blog=blog, **section_data)

                return Response(BlogSerializer(blog).data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating blog {str(e)}")

    @classmethod
    def update_blog(cls, instance, data, partial=False):
        """
        Handle the update of an existing Blog instance along with related Section instances.

        Args:
            instance (Blog): The existing Blog instance.
            data (dict): The validated data for updating a Blog.
            partial (bool): Whether to perform partial update (default: False).

        Returns:
            Response: The response object containing the updated instance data.
        """
        serializer = BlogSerializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                instance.title = serializer.validated_data.get("title", instance.title)
                instance.cover_photo = serializer.validated_data.get(
                    "cover_photo", instance.cover_photo
                )
                instance.save()

                # Handle sections update or create new sections
                sections_data = data.get("sections", [])

                updated_section_ids = []

                for section_data in sections_data:
                    section_id = section_data.get("id", None)

                    if section_id:
                        # Update existing section
                        section = Section.objects.get(id=section_id, blog=instance)
                        section.section_type = section_data.get(
                            "section_type", section.section_type
                        )
                        section.content = section_data.get("content", section.content)
                        section.image = section_data.get("image", section.image)
                        section.save()
                        updated_section_ids.append(section.id)
                    else:
                        # Create new section
                        Section.objects.create(blog=instance, **section_data)

                # Delete sections not in updated_section_ids
                Section.objects.filter(blog=instance).exclude(id__in=updated_section_ids).delete()

                return Response(BlogSerializer(instance).data, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating blog: {e}")
