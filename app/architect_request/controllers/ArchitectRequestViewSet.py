"""
Module containing the viewset for the ArchitectRequest model.

This module defines the viewset for the ArchitectRequest model to provide
CRUD operations and additional functionality through the API.

Classes:
    ArchitectRequestViewSet: Viewset for the ArchitectRequest model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.architect_request.controllers.ManageArchitectRequestPermission import (
    ManageArchitectRequestPermission,
)
from app.architect_request.models.ArchitectRequest import ArchitectRequest
from app.architect_request.serializers.ArchitectRequestSerializer import (
    ArchitectRequestInputSerializer,
    ArchitectRequestSerializer,
)
from app.architect_request.services.ArchitectRequestService import (
    ArchitectRequestService,
)


class ArchitectRequestViewSet(viewsets.ModelViewSet):
    """
    Viewset for the ArchitectRequest model.

    Provides CRUD operations and additional functionality for ArchitectRequest instances.

    Attributes:
        queryset (QuerySet): The queryset of ArchitectRequest instances.
        serializer_class (ArchitectRequestSerializer): The serializer class for ArchitectRequest instances.
    """

    queryset = ArchitectRequest.objects.all()
    serializer_class = ArchitectRequestSerializer
    permission_classes = [IsAuthenticated, ManageArchitectRequestPermission]

    def get_serializer_class(self):
        """
        Return the serializer class based on the request method.

        Uses ArchitectRequestInputSerializer for POST and PUT requests,
        and ArchitectRequestSerializer for other operations.

        Returns:
            Serializer Class: The appropriate serializer class based on the request method.
        """
        if self.request.method in ["POST", "PUT"]:
            return ArchitectRequestInputSerializer
        return ArchitectRequestSerializer

    @action(
        detail=False,
        methods=["POST"],
        url_path="create-architect-request",
        permission_classes=[],
    )
    def create_architect_request(self, request):
        """
        Custom action to create an ArchitectRequest.

        Uses an input serializer to validate data and calls the service to handle the creation logic.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            Response: The response object containing the result of the operation.
        """
        return ArchitectRequestService.add_architect_request(request.data)
