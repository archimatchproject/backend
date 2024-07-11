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
from rest_framework.response import Response

from app.cms.models.GuideArticle import GuideArticle
from app.cms.models.GuideSection import GuideSection
from app.cms.serializers.GuideArticleSerializer import GuideArticleSerializer
from app.cms.serializers.GuideSectionSerializer import GuideSectionSerializer


class GuideArticleService:
    """
    Service class providing methods for creating and updating GuideArticle instances
    along with their related GuideSection instances.
    """

    @classmethod
    def create_guide_article(cls, data):
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
        serializer = GuideArticleSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                # Create GuideArticle instance
                guide_article = GuideArticle.objects.create(
                    title=serializer.validated_data["title"],
                    description=serializer.validated_data["description"],
                    guide_thematic=serializer.validated_data["guide_thematic"],
                    date=serializer.validated_data["date"],
                    rating=serializer.validated_data["rating"],
                )

                # Create related sections if provided
                sections_data = data.get("sections", [])
                for section_data in sections_data:
                    GuideSection.objects.create(guide_article=guide_article, **section_data)

                return Response(
                    GuideArticleSerializer(guide_article).data, status=status.HTTP_201_CREATED
                )
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating guide article: {str(e)}")

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

        try:
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

                return Response(GuideArticleSerializer(instance).data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating guide article: {str(e)}")
