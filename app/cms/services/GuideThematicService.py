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
from app.core.pagination import CustomPagination
from rest_framework.exceptions import ValidationError

class GuideThematicService:
    """
    Service class for handling GuideThematic operations.

    Handles business logic and exception handling for GuideThematic creation and management.

    Methods:
        create_guide_thematic(request): Handles validation and creation of a new GuideThematic.
        update_guide_thematic(guide_thematic_instance, data, partial=False): Handles updating an
        existing GuideThematic.
    """

    pagination_class = CustomPagination
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

        with transaction.atomic():
            # Create GuideThematic instance
            guide_thematic = GuideThematic.objects.create(
                **validated_data, admin=request.user.admin
            )

            return True,GuideThematicSerializer(guide_thematic).data

        

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

        with transaction.atomic():
            fields = ["title", "sub_title", "visible", "icon"]
            for field in fields:
                setattr(instance, field, validated_data.get(field, getattr(instance, field)))
            instance.save()

            return True,GuideThematicSerializer(instance).data

        

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

        visibility = request.data.get("visible")
        if visibility is None:
            raise serializers.ValidationError(detail="Visible field is required.")
        guide_thematic = GuideThematic.objects.get(pk=guide_thematic_id)
        guide_thematic.visible = visibility
        guide_thematic.save()
        return True,GuideThematicSerializer(guide_thematic).data
        

    def get_thematic_guides_paginated(cls, request):
        """
        Handle GET request and return paginated Supplier objects.
        This method retrieves all Supplier objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination parameters are not provided correctly or if an
        error occurs during serialization or database access, it returns a 400 Bad
        Request response with an appropriate error message.
        Args:
            request (HttpRequest): The incoming HTTP request object containing
                pagination parameters like page number, page size, etc.
        Returns:
            Response: A paginated response containing serialized Supplier objects
                or a 400 Bad Request response with an error message.
        """
        target_user_type = request.query_params.get("target_user_type")
        if not target_user_type:
            raise ValidationError("The 'target_user_type' query parameter is required.")
        queryset = GuideThematic.objects.filter(target_user_type=target_user_type)
        paginator = cls.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = GuideThematicSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = GuideThematicSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)