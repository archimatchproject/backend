"""
Module defining the CGUCGVPolicyViewSet.

This module contains the CGUCGVPolicyViewSet class, which provides
view-level logic for the CGU/CGV policy model, including creation operations.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.cms.controllers.ManageLegalAndPolicyPermission import ManageLegalAndPolicyPermission
from app.cms.models.CGUCGVPolicy import CGUCGVPolicy
from app.cms.serializers.CGUCGVPolicySerializer import CGUCGVPolicySerializer
from app.cms.services.CGUCGVPolicyService import CGUCGVPolicyService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

class CGUCGVPolicyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the CGUCGVPolicy model.

    This class provides view-level logic for the CGU/CGV policy model,
    including creation operations, delegating the business logic
    to the CGUCGVPolicyService.
    """

    queryset = CGUCGVPolicy.objects.all()
    serializer_class = CGUCGVPolicySerializer

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        For `create`, `update`, `partial_update`, and `destroy` actions, the view
        requires `IsAuthenticated` and `ManageLegalAndPolicyPermission` permissions.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["list", "retrieve"]:
            return []
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), ManageLegalAndPolicyPermission()]
        return super().get_permissions()

    @handle_service_exceptions
    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new CGUCGVPolicy instance.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the created instance data.
        """
        success, data = CGUCGVPolicyService.create_cgucgv_policy(request)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)
