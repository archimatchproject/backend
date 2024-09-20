"""
Module defining the PrivacyPolicyViewSet.

This module contains the PrivacyPolicyViewSet class, which provides
view-level logic for the PrivacyPolicy model, including creation operations.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.cms.controllers.ManageLegalAndPolicyPermission import ManageLegalAndPolicyPermission
from app.cms.models.PrivacyPolicy import PrivacyPolicy
from app.cms.serializers.PrivacyPolicySerializer import PrivacyPolicySerializer
from app.cms.services.PrivacyPolicyService import PrivacyPolicyService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status
from rest_framework.decorators import action

class PrivacyPolicyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the PrivacyPolicy model.

    This class provides view-level logic for the PrivacyPolicy model,
    including creation operations, delegating the business logic
    to the PrivacyPolicyService.
    """

    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer

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

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new PrivacyPolicy instance.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the created instance data.
        """
        return PrivacyPolicyService.create_privacy_policy(request)

    @action(detail=True, methods=["PUT"])
    def get_policy_by_admin(self, request, pk=None):
        """
        Retrieve the PrivacyPolicy instance associated with the given admin.

        Args:
            admin (Admin): The admin instance.

        Returns:
            dict: The serialized data of the PrivacyPolicy instance.

        Raises:
            NotFound: If no policy is found for the admin.
        """

        success, data = PrivacyPolicyService.get_policy_by_admin(request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)