"""
Module containing the viewset for the OfficeRequest model.

This module defines the viewset for the OfficeRequest model to provide
CRUD operations and additional functionality through the API.

Classes:
    OfficeRequestViewSet: Viewset for the OfficeRequest model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action


from app.architect_request.models.OfficeRequest import OfficeRequest


from app.architect_request.serializers.OfficeRequestSerializer import (
    OfficeRequestSerializer,
)
from app.architect_request.services.OfficeRequestService import (
    OfficeRequestService,
)
from app.core.pagination import CustomPagination

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status


class OfficeRequestViewSet(viewsets.ModelViewSet):
    """
    Viewset for the OfficeRequest model.

    Provides CRUD operations and additional functionality for OfficeRequest
    instances.

    Attributes:
        queryset (QuerySet): The queryset of OfficeRequest instances.
        serializer_class (OfficeRequestSerializer): The serializer class for
        OfficeRequest
        instances.
    """

    queryset = OfficeRequest.objects.all()

    serializer_class = OfficeRequestSerializer
    pagination_class = CustomPagination

    @action(detail=False, methods=["POST"], url_path="create-office-request")
    @handle_service_exceptions
    def create_office_request(self, request):
        """
        Custom action to create an OfficeRequest.

        Uses an input serializer to validate data and calls the service to handle the
        creation logic.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            Response: The response object containing the result of the operation.
        """
        success, data = OfficeRequestService.add_office_request(request.data)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)
