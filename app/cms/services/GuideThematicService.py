"""
Module containing the service for handling GuideThematic logic.

This module defines the service for handling the business logic and exceptions
related to GuideThematic creation and management.

Classes:
    GuideThematicService: Service class for GuideThematic operations.
"""

from django.db import transaction

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.cms.models.GuideThematic import GuideThematic
from app.cms.serializers.GuideThematicSerializer import GuideThematicSerializer


class GuideThematicService:
    """
    Service class for handling GuideThematic operations.

    Handles business logic and exception handling for GuideThematic creation and management.

    Methods:
        create_guide_thematic(request): Handles validation and creation of a new GuideThematic.
        update_guide_thematic(guide_thematic_instance, data, partial=False): Handles updating an
        existing GuideThematic.
    """

    @classmethod
    def create_guide_thematic(cls, request):
        """
        Handles validation and creation of a new GuideThematic.

        Args:
            data (dict): The validated data for creating a GuideThematic instance.
            user (User): The user creating the guide thematic, used to set the admin.

        Returns:
            Response: The response object containing the result of the operation.
        """
        serializer = GuideThematicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        try:
            with transaction.atomic():
                # Create GuideThematic instance
                guide_thematic = GuideThematic.objects.create(
                    **validated_data, admin=request.user.admin
                )

                return Response(
                    GuideThematicSerializer(guide_thematic).data, status=status.HTTP_201_CREATED
                )

        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error creating guide thematic: {str(e)}")

    @classmethod
    def update_guide_thematic(cls, instance, data, partial=False):
        """
        Handle the update of an existing GuideThematic instance.

        Args:
            instance (GuideThematic): The existing GuideThematic instance.
            data (dict): The validated data for updating a GuideThematic.
            partial (bool): Whether to perform partial update (default: False).

        Returns:
            Response: The response object containing the updated instance data.
        """
        serializer = GuideThematicSerializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        try:
            with transaction.atomic():
                fields = ["title", "sub_title", "visible", "icon"]
                for field in fields:
                    setattr(instance, field, validated_data.get(field, getattr(instance, field)))
                instance.save()

                return Response(GuideThematicSerializer(instance).data, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise APIException(detail=f"Error updating guide thematic: {str(e)}")

    @classmethod
    def change_visibility(cls, guide_thematic_id, request):
        """
        Handle the change of visibility for a Guide instance.

        Args:
            guide_thematic_id (int): The primary key of the Guide instance.
            visibility (bool): The new visibility status for the Guide instance.

        Returns:
            Response: The response object containing the updated instance data.
        """
        try:
            visibility = request.data.get("visible")
            if visibility is None:
                raise serializers.ValidationError(detail="Visible field is required.")
            guide_thematic = GuideThematic.objects.get(pk=guide_thematic_id)
            guide_thematic.visible = visibility
            guide_thematic.save()
            return Response(GuideThematicSerializer(guide_thematic).data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            raise e
        except GuideThematic.DoesNotExist:
            raise NotFound(detail="Guide not found.")
        except Exception as e:
            raise APIException(detail=f"Error changing visibility: {str(e)}")
