"""
Module for Announcement ViewSet.

This module defines the AnnouncementViewSet class, which is a viewset
for viewing and editing Announcement instances using Django REST Framework.
"""

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from app.announcement.models.Announcement import Announcement
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.recommendation.models.ArchitectBox import ArchitectBox
from app.recommendation.serializers.ArchitectBoxSerializer import ArchitectBoxSerializer
from app.recommendation.services.ArchitectBoxService import ArchitectBoxService


class ArchitectBoxViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Announcement model.

    Provides endpoints for viewing and editing Announcement instances.
    """

    queryset = ArchitectBox.objects.all()
    serializer_class = ArchitectBoxSerializer

    def get_permissions(self):
        """
        Return the list of permissions that this view requires.

        Applies different permissions based on the action being executed.

        Returns:
            list: The list of permission classes.
        """
        if self.action in [
            "list",
        ]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []
        return super().get_permissions()

    def get_queryset(self):
        """
        Filter the collections by the supplier related to the currently authenticated user.
        """
        user = self.request.user
        return Announcement.objects.filter(client__user=user)

    @handle_service_exceptions
    def get_architect_score(self, request, pk):
        """
        Handle GET request and return paginated Announcement objects.

        This method retrieves all Announcement objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination is not applied correctly, it returns a 400 Bad Request response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing Announcement objects or an error message.
        """

        success, data = ArchitectBoxService.compute_score(request, id=pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @handle_service_exceptions
    def get_box_announcements(self, request):
        """
        Retrieve box announcements for the authenticated user.
        Args:
            request (Request): The HTTP request object containing user information.
        Returns:
            Response: A response object containing the success status, data, and HTTP
            status code 200.
        """

        user = request.user
        success, data = ArchitectBoxService.get_box_announcements(user)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
