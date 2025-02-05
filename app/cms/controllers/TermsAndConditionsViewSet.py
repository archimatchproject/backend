"""
Module defining the TermsAndConditionsViewSet.

This module contains the TermsAndConditionsViewSet class, which provides
view-level logic for the TermsAndConditions model, including creation operations.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.cms.controllers.ManageLegalAndPolicyPermission import ManageLegalAndPolicyPermission
from app.cms.models.TermsAndConditions import TermsAndConditions
from app.cms.serializers.TermsAndConditionsSerializer import TermsAndConditionsSerializer
from app.cms.services.TermsAndConditionsService import TermsAndConditionsService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

class TermsAndConditionsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the TermsAndConditions model.

    This class provides view-level logic for the TermsAndConditions model,
    including creation operations, delegating the business logic
    to the TermsAndConditionsService.
    """

    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer

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
        Handle the creation of a new TermsAndConditions instance.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the created instance data.
        """
        success,data = TermsAndConditionsService.create_terms_and_conditions(request)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)
