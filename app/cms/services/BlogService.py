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
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.cms.models.Blog import Blog
from app.cms.models.BlogSection import BlogSection
from app.cms.models.BlogTag import BlogTag
from app.cms.models.SliderImage import SliderImage
from app.cms.serializers.BlogSerializer import BlogSerializer
from app.cms.serializers.BlogTagSerializer import BlogTagSerializer


class BlogService:
    """
    Service class for handling Blog operations.

    Handles business logic and exception handling for Blog creation and management.

    Methods:
        create_blog(data): Handles validation and creation of a new Blog.
        update_blog(blog_instance, data, partial=False): Handles updating an existing Blog.
    """

    @classmethod
    def create_blog(cls, data, user):
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

        with transaction.atomic():
            # Create Blog instance
            blog = Blog.objects.create(
                title=validated_data.get("title"),
                cover_photo=validated_data.get("cover_photo"),
                sub_title=validated_data.get("sub_title"),
                blog_thematic=validated_data.get("blog_thematic"),
                admin=user.admin,
                visible=validated_data.get("visible", False),
            )

            # Create related sections if provided
            sections_data = validated_data.get("sections", [])
            for section_data in sections_data:
                BlogSection.objects.create(blog=blog, **section_data)

            # Add tags if provided
            tags = validated_data.get("tags", [])
            blog.tags.set(tags)

            return True,BlogSerializer(blog).data

        

    @classmethod
    def update_blog(cls, instance, data, partial=False):
        """
        Handle the update of an existing Blog instance along with related BlogSection instances.

        Args:
            instance (Blog): The existing Blog instance.
            data (dict): The validated data for updating a Blog.
            partial (bool): Whether to perform partial update (default: False).

        Returns:
            Response: The response object containing the updated instance data.
        """
        serializer = BlogSerializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)


        with transaction.atomic():
            instance.title = serializer.validated_data.get("title", instance.title)
            instance.cover_photo = serializer.validated_data.get(
                "cover_photo", instance.cover_photo
            )
            instance.sub_title = serializer.validated_data.get("sub_title", instance.sub_title)
            instance.blog_thematic = serializer.validated_data.get(
                "blog_thematic", instance.blog_thematic
            )
            instance.visible = serializer.validated_data.get("visible", instance.visible)
            instance.save()

            # Handle sections update or create new sections
            sections_data = data.get("sections", [])
            updated_section_ids = []

            for section_data in sections_data:
                section_id = section_data.get("id", None)

                if section_id:
                    # Update existing section
                    section = BlogSection.objects.get(id=section_id, blog=instance)
                    section.section_type = section_data.get(
                        "section_type", section.section_type
                    )
                    section.content = section_data.get("content", section.content)
                    section.image = section_data.get("image", section.image)
                    section.save()
                    updated_section_ids.append(section.id)
                else:
                    # Create new section

                    section_created = BlogSection.objects.create(blog=instance, **section_data)
                    updated_section_ids.append(section_created.id)

            # Delete sections not in updated_section_ids

            BlogSection.objects.filter(blog=instance).exclude(
                id__in=updated_section_ids
            ).delete()

            # Update tags
            tags = serializer.validated_data.get("tags", [])
            instance.tags.set(tags)

            return True,BlogSerializer(instance).data

        

    @classmethod
    def update_cover_photo(cls, pk, request):
        """
        Handle the update of a Blog cover photo.

        Args:
            blog_id (int): The primary key of the Blog instance.
            request (Request): The HTTP request object containing data to update Blog instance.

        Returns:
            Response: The response object containing the updated instance data.
        """

        blog = Blog.objects.get(pk=pk)
        cover_photo = request.data.get("cover_photo")
        if not cover_photo:
            raise serializers.ValidationError(detail="Cover photo is required.")

        blog.cover_photo = cover_photo
        blog.save()
        return True,BlogSerializer(blog).data

    

    @classmethod
    def change_visibility(cls, blog_id, request):
        """
        Handle the change of visibility for a Blog instance.

        Args:
            blog_id (int): The primary key of the Blog instance.
            visibility (bool): The new visibility status for the Blog instance.

        Returns:
            Response: The response object containing the updated instance data.
        """

        visibility = request.data.get("visible")
        if visibility is None:
            raise serializers.ValidationError(detail="Visible field is required.")
        blog = Blog.objects.get(pk=blog_id)
        blog.visible = visibility
        blog.save()
        return True,BlogSerializer(blog).data
        
    @classmethod
    def upload_media(cls, request):
        """
        Handle the upload of media for a Blog section.

        Args:
            request (Request): The HTTP request object containing data to update Blog section.

        Returns:
            Response: The response object containing the result of the operation.
        """

        section_id = request.data.get("section_id")
        image = request.FILES.get("image")
        slider_images = request.FILES.getlist("slider_images")
        section = BlogSection.objects.get(id=section_id)

        # Handle image section type
        if section.section_type == "image":
            if not image:
                raise serializers.ValidationError(
                    detail="Image file is required for image section type."
                )
            section.image = image
            section.save()
            blog = section.blog
            return True,BlogSerializer(blog).data

        # Handle slider section type
        elif section.section_type == "slider":
            if not slider_images:
                raise serializers.ValidationError(
                    "At least one slider image file is required for slider section type."
                )

            # Create multiple SliderImage instances for the slider section
            SliderImage.objects.filter(section=section).delete()  # Clear existing slider images
            for img in slider_images:
                SliderImage.objects.create(section=section, image=img)

            blog = section.blog
            return True,BlogSerializer(blog).data

        else:
            raise serializers.ValidationError(
                detail="Invalid section type. Must be either image or slider."
            )
        

    @classmethod
    def list_tags(cls):
        """
        Retrieve all tags.
        """
        tags = BlogTag.objects.all()
        serializer = BlogTagSerializer(tags, many=True)
        return True,serializer.data
