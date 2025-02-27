"""Module: RecommendationSettings ViewSet

This module defines the `RecommendationSettingsViewSet`, which provides API endpoints
to manage `RecommendationSettings` resources, including retrieving, updating settings,
and handling attribute updates.
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.recommendation.models.RecommendationSettings import RecommendationSettings
from app.recommendation.serializers.RecommendationSettingsSerializer import RecommendationSettingsSerializer
from app.recommendation.services.RecommendationSettingsService import RecommendationSettingsService


class RecommendationSettingsViewSet(viewsets.ViewSet):
    """ViewSet for handling recommendation settings-related actions."""

    queryset = RecommendationSettings.objects.all()
    serializer_class = RecommendationSettingsSerializer

    @action(detail=False, methods=["GET"], url_path="get-settings")
    @handle_service_exceptions
    def get_settings(self, request, pk):
        """Retrieve the current recommendation settings.

        Args:
            request (Request): The request object.
            pk (int): The primary key of the recommendation settings instance.

        Returns:
            Response: Serialized recommendation settings data.
        """
        success, data = RecommendationSettingsService.get_recommendation_settings(pk)
        return build_response(data=data, status=status.HTTP_200_OK, success=success)

    @action(detail=False, methods=["PUT"], url_path="update-settings")
    @handle_service_exceptions
    def update_settings(self, request, pk):
        """Update the recommendation settings with provided data.

        Args:
            request (Request): The request object containing updated data.
            pk (int): The primary key of the recommendation settings instance.

        Returns:
            Response: Serialized updated recommendation settings data.
        """
        success, data = RecommendationSettingsService.update_recommendation_settings(request.data, pk)
        return build_response(data=data, status=status.HTTP_200_OK, success=success)

    @action(detail=False, methods=["PUT"], url_path="update-attributes")
    @handle_service_exceptions
    def update_attributes(self, request, pk):
        """Update the attributes of recommendation settings.

        Args:
            request (Request): The request object containing updated attribute data.
            pk (int): The primary key of the recommendation settings instance.

        Returns:
            Response: Serialized updated attributes data.
        """
        success, data = RecommendationSettingsService.update_recommendation_attributes(request.data, pk)
        return build_response(data=data, status=status.HTTP_200_OK, success=success)

    @action(detail=False, methods=["GET"], url_path="get-settings-choices")
    @handle_service_exceptions
    def get_settings_choices(self, request):
        """Retrieve the available choices for recommendation settings.

        Args:
            request (Request): The request object.

        Returns:
            Response: Serialized recommendation settings choices.
        """
        success, data = RecommendationSettingsService.get_recommendation_settings_choices()
        return build_response(data=data, status=status.HTTP_200_OK, success=success)
