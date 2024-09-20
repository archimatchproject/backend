"""
Module defining the CookiesPolicyViewSet.

This module contains the CookiesPolicyViewSet class, which provides
view-level logic for the CookiesPolicy model, including creation operations.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.cms.controllers.ManageLegalAndPolicyPermission import ManageLegalAndPolicyPermission
from app.cms.models.CookiesPolicy import CookiesPolicy
from app.cms.serializers.CookiesPolicySerializer import CookiesPolicySerializer
from app.cms.services.CookiesPolicyService import CookiesPolicyService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

class CookiesPolicyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the CookiesPolicy model.

    This class provides view-level logic for the CookiesPolicy model,
    including creation operations, delegating the business logic
    to the CookiesPolicyService.
    """

    queryset = CookiesPolicy.objects.all()
    serializer_class = CookiesPolicySerializer

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
        Handle the creation of a new CookiesPolicy instance.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the created instance data.
        """
        success, data = CookiesPolicyService.create_cookies_policy(request)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)
