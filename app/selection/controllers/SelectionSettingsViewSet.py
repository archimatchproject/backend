"""
Module: SelectionSettings ViewSet

This module defines the `SelectionSettingsViewSet`, which provides the API endpoints
to manage `SelectionSettings` resources, including retrieving and updating settings.

Classes:
    SelectionSettingsViewSet: A viewset that provides actions for managing selection settings.
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.selection.models.SelectionSettings import SelectionSettings
from app.selection.serializers import SelectionSettingsSerializer
from app.selection.services.SelectionSettingsService import SelectionSettingsService


class SelectionSettingsViewSet(viewsets.ViewSet):
    """
    ViewSet for handling selection settings-related actions.

    This ViewSet provides the following actions:
    - get_settings: Retrieve the current selection settings.
    - update_settings: Update the selection settings.

    Attributes:
        - queryset : returns all the selectionSettings
        - serializer_class : returns an instance of the serializer of the selectionSettings model

    Methods:
        - get_settings: Handles retrieving the current selection settings.
        - update_settings: Handles updating the selection settings with provided data.
    """

    queryset = SelectionSettings.objects.all()
    serializer_class = SelectionSettingsSerializer

    @action(detail=False, methods=["GET"], url_path="get-settings")
    @handle_service_exceptions
    def get_settings(self, request, pk):
        """
        Retrieve the current selection settings.

        Args:
            request (Request): The request object.

        Returns:
            Response: A response containing the serialized selection settings data.

        Raises:
            APIException: If no selection settings instance is found.
        """
        success, data = SelectionSettingsService.get_selection_settings(request, pk)
        return build_response(data=data, status=status.HTTP_200_OK, success=success)

    @action(detail=False, methods=["PUT"], url_path="update-settings")
    @handle_service_exceptions
    def update_settings(self, request, pk):
        """
        Update the selection settings with provided data.

        Args:
            request (Request): The request object containing the updated data.

        Returns:
            Response: A response containing the updated serialized selection settings data.

        Raises:
            ValidationError: If the provided data fails validation.
            APIException: If no selection settings instance exists.
        """

        success, data = SelectionSettingsService.update_selection_settings(request.data, pk)
        return build_response(data=data, status=status.HTTP_200_OK, success=success)

    @action(detail=False, methods=["GET"], url_path="get-settings-choises")
    @handle_service_exceptions
    def get_settings_choices(self, request):
        """
        Retrieve the current selection settings.

        Args:
            request (Request): The request object.

        Returns:
            Response: A response containing the serialized selection settings choices data.

        Raises:
            APIException: If no selection settings instance is found.
        """
        success, data = SelectionSettingsService.get_selection_settings_choices(request)
        return build_response(data=data, status=status.HTTP_200_OK, success=success)
