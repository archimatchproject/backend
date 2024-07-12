"""
REST API ViewSet for managing GuideThematic instances.

This module defines a ViewSet for handling CRUD operations
and additional actions
related to GuideThematic instances via REST API endpoints.
"""

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from app.cms.controllers.ManageGuidePermission import ManageGuidePermission
from app.cms.models.GuideThematic import GuideThematic
from app.cms.serializers.GuideThematicSerializer import GuideThematicSerializer


class GuideThematicViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling GuideThematic instances.

    This ViewSet provides endpoints for CRUD operations related to
    GuideThematic instances.
    """

    queryset = GuideThematic.objects.all()
    serializer_class = GuideThematicSerializer

    def get_queryset(self):
        """
        Get the queryset for the view.

        Raises:
            ValidationError: If the `target_user_type` query parameter is not provided.

        Returns:
            QuerySet: The filtered queryset based on the `target_user_type` parameter.
        """
        target_user_type = self.request.query_params.get("target_user_type")
        if not target_user_type:
            raise ValidationError("The 'target_user_type' query parameter is required.")
        return GuideThematic.objects.filter(target_user_type=target_user_type)

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
