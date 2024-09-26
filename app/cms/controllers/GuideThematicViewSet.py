"""
REST API ViewSet for managing GuideThematic instances.

This module defines a ViewSet for handling CRUD operations
and additional actions
related to GuideThematic instances via REST API endpoints.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from app.cms.controllers.ManageGuidePermission import ManageGuidePermission
from app.cms.models.GuideThematic import GuideThematic
from app.cms.serializers.GuideThematicSerializer import GuideThematicSerializer
from app.cms.services.GuideThematicService import GuideThematicService


class GuideThematicViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling GuideThematic instances.

    This ViewSet provides endpoints for CRUD operations related to
    GuideThematic instances.
    """

    queryset = GuideThematic.objects.all()
    serializer_class = GuideThematicSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        """
        Get the queryset for the view.

        Raises:
            ValidationError: If the `target_user_type` query parameter is not provided.

        Returns:
            QuerySet: The filtered queryset based on the `target_user_type` parameter.
        """
        if self.action == "list":
            target_user_type = self.request.query_params.get("target_user_type")
            if not target_user_type:
                raise ValidationError("The 'target_user_type' query parameter is required.")
            return GuideThematic.objects.filter(target_user_type=target_user_type)
        else:
            return self.queryset

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        For `list` and `retrieve` actions (`GET` requests), no specific permissions are required.
        For `create`, `update`, `partial_update`, and `destroy` actions
        (`POST`, `PUT`, `PATCH`, `DELETE` requests),
        the view requires `IsAuthenticated` and `ManageBlogPermission` permissions.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["list", "retrieve"]:
            return []
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), ManageGuidePermission()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Create a new GuideThematic instance.

        Args:
            request (Request): The HTTP request object containing data to create
              GuideThematic instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the created GuideThematic instance.
        """
        return GuideThematicService.create_guide_thematic(request)

    def update(self, request, *args, **kwargs):
        """
        Update an existing GuideThematic instance.

        Args:
            request (Request): The HTTP request object containing data to
            update GuideThematic instance.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Serialized data of the updated GuideThematic instance.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        return GuideThematicService.update_guide_thematic(instance, request.data, partial=partial)

    @action(detail=True, methods=["PUT"])
    def change_visibility(self, request, pk=None):
        """
        Change the visibility of a Blog instance.

        Args:
            request (Request): The HTTP request object containing data to change visibility.
            pk (int): The primary key of the Blog instance to be updated.

        Returns:
            Response: Serialized data of the updated Blog instance.
        """

        return GuideThematicService.change_visibility(pk, request)

    def list(self, request, *args, **kwargs):
        return GuideThematicService.get_thematic_guides_paginated(request)