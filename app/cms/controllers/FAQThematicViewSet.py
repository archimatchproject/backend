"""
Module defining the FAQThematicViewSet.

This module contains the FAQThematicViewSet class, which provides
view-level logic for the FAQThematic model, including creation and update operations.
"""

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from app.cms.controllers.ManageFAQPermission import ManageFAQPermission
from app.cms.models.FAQThematic import FAQThematic
from app.cms.serializers.FAQThematicSerializer import FAQThematicSerializer
from app.cms.services.FAQThematicService import FAQThematicService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status

class FAQThematicViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the FAQThematic model.

    This class provides view-level logic for the FAQThematic model,
    including creation and update operations, delegating the business logic
    to the FAQThematicService.
    """

    queryset = FAQThematic.objects.all()
    serializer_class = FAQThematicSerializer

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
            return FAQThematic.objects.filter(target_user_type=target_user_type)
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
            return [IsAuthenticated(), ManageFAQPermission()]
        return super().get_permissions()

    @handle_service_exceptions
    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new FAQThematic instance along with related FAQQuestion instances.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the created instance data.
        """
        success,data = FAQThematicService.create_faq_thematic(request)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)


    @handle_service_exceptions
    def update(self, request, *args, **kwargs):
        """
        Handle the update of an existing FAQThematic instance along with related
        FAQQuestion instances.

        Args:
            request (Request): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The response object containing the updated instance data.
        """
        success,data =  FAQThematicService.update_faq_thematic(self.get_object(), request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

