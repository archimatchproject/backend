"""
Module defining the GuideArticleService class for handling business logic related to
GuideArticle operations.

This module provides methods for creating and updating GuideArticle instances along with
their related GuideSection instances.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.cms.models.GuideArticle import GuideArticle
from app.cms.models.GuideSection import GuideSection
from app.cms.models.GuideSliderImage import GuideSliderImage
from app.cms.serializers.GuideArticleSerializer import GuideArticleSerializer
from app.cms.serializers.GuideSectionSerializer import GuideSectionSerializer


class GuideArticleService:
    """
    Service class providing methods for creating and updating GuideArticle instances
    along with their related GuideSection instances.
    """

    @classmethod
    def create_guide_article(cls, request):
        """
        Create a new GuideArticle instance along with its related GuideSection
        instances.

        Args:
            data (dict): Validated data for creating a GuideArticle instance,
            including sections.

        Returns:
            Response: Response object containing the serialized data of the
            created GuideArticle
                      instance and HTTP status code 201 upon successful creation.

        Raises:
            serializers.ValidationError: If validation fails for GuideArticleSerializer.
            APIException: If an unexpected error occurs during creation.

        Note:
            Uses GuideArticleSerializer for GuideArticle serialization and deserialization.
        """
        serializer = GuideArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        with transaction.atomic():
            # Create GuideArticle instance
            sections_data = validated_data.pop("sections", [])
            guide_article = GuideArticle.objects.create(
                **validated_data, admin=request.user.admin
            )

            # Create related sections if provided

            for section_data in sections_data:
                GuideSection.objects.create(guide_article=guide_article, **section_data)

            return True,GuideArticleSerializer(guide_article).data
        

    @classmethod
    def update_guide_article(cls, instance, data):
        """
        Update an existing GuideArticle instance along with its related GuideSection instances.

        Args:
            instance (GuideArticle): Existing GuideArticle instance to update.
            data (dict): Validated data for updating the GuideArticle instance, including sections.

        Returns:
            Response: Response object containing the serialized data of the updated GuideArticle
                      instance and HTTP status code 200 upon successful update.

        Raises:
            serializers.ValidationError: If validation fails for GuideArticleSerializer
            or GuideSectionSerializer.
            APIException: If an unexpected error occurs during update.

        Note:
            Uses GuideArticleSerializer and GuideSectionSerializer for serialization
            and deserialization.
            Deletes GuideSection instances not mentioned in the request.
        """
        partial = data.get("partial", False)
        serializer = GuideArticleSerializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)


        with transaction.atomic():
            instance.title = serializer.validated_data.get("title", instance.title)
            instance.description = serializer.validated_data.get(
                "description", instance.description
            )
            instance.guide_thematic = serializer.validated_data.get(
                "guide_thematic", instance.guide_thematic
            )
            instance.date = serializer.validated_data.get("date", instance.date)
            instance.rating = serializer.validated_data.get("rating", instance.rating)
            instance.save()

            # Update or create related sections
            sections_data = data.get("sections", [])
            section_ids_to_keep = []

            for section_data in sections_data:
                section_id = section_data.get("id")
                section_instance = None
                if section_id:
                    try:
                        section_instance = instance.guide_article_sections.get(id=section_id)
                    except GuideSection.DoesNotExist:
                        raise serializers.ValidationError(
                            f"GuideSection with id {section_id} does not exist."
                        )

                section_serializer = GuideSectionSerializer(
                    section_instance,
                    data=section_data,
                    partial=partial,
                )
                section_serializer.is_valid(raise_exception=True)
                section_instance = section_serializer.save(guide_article=instance)
                section_ids_to_keep.append(section_instance.id)

            # Delete sections not mentioned in the request
            instance.guide_article_sections.exclude(id__in=section_ids_to_keep).delete()

            return True,GuideArticleSerializer(instance).data
    

    @classmethod
    def change_visibility(cls, guide_id, request):
        """
        Handle the change of visibility for a GuideArticle instance.

        Args:
            guide_id (int): The primary key of the GuideArticle instance.
            visibility (bool): The new visibility status for the GuideArticle instance.

        Returns:
            Response: The response object containing the updated instance data.
        """

        visibility = request.data.get("visible")
        if visibility is None:
            raise serializers.ValidationError(detail="Visible field is required.")
        guide = GuideArticle.objects.get(pk=guide_id)
        guide.visible = visibility
        guide.save()
        return True,GuideArticleSerializer(guide).data
    

    @classmethod
    def upload_media(cls, request):
        """
        Handle the upload of media for a Guide section.

        Args:
            request (Request): The HTTP request object containing data to update Guide section.

        Returns:
            Response: The response object containing the result of the operation.
        """

        section_id = request.data.get("section_id")
        image = request.FILES.get("image")
        video = request.FILES.get("video")
        slider_images = request.FILES.getlist("slider_images")
        section = GuideSection.objects.get(id=section_id)

        # Handle image section type
        if section.section_type == "image":
            if not image:
                raise serializers.ValidationError(
                    detail="Image file is required for image section type."
                )
            section.image = image
            section.save()
            guide_article = section.guide_article
            return True,GuideArticleSerializer(guide_article).data
        # Handle video section type
        if section.section_type == "video":
            if not video:
                raise serializers.ValidationError(
                    detail="Video file is required for video section type."
                )
            section.video = video
            section.save()
            guide_article = section.guide_article
            return True,GuideArticleSerializer(guide_article).data

        # Handle slider section type
        elif section.section_type == "slider":
            if not slider_images:
                raise serializers.ValidationError(
                    "At least one slider image file is required for slider section type."
                )

            # Create multiple SliderImage instances for the slider section
            GuideSliderImage.objects.filter(
                section=section
            ).delete()  # Clear existing slider images
            for img in slider_images:
                GuideSliderImage.objects.create(section=section, image=img)

            guide_article = section.guide_article
            return True,GuideArticleSerializer(guide_article).data

        else:
            raise serializers.ValidationError(
                detail="Invalid section type. Must be either image or slider."
            )
        
