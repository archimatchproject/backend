"""
Attributes:
    queryset (QuerySet): The queryset of UnlockRequest objects.
    serializer_class (Serializer): The serializer class for UnlockRequest objects.
Methods:
    list(request):
    create(request):
    accept(request, pk=None):
    refuse(request, pk=None):

Returns:_summary_
    _type_: _description_
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.selection.models.UnlockRequest import UnlockRequest
from app.selection.serializers.UnlockRequestSerializer import UnlockRequestPostSerializer
from app.selection.serializers.UnlockRequestSerializer import UnlockRequestSerializer
from app.selection.services.UnlockRequestService import UnlockRequestService


class UnlockRequestViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling UnlockRequest operations.

    This viewset provides actions to get paginated unlock requests, create an unlock request,
    accept an unlock request, and refuse an unlock request.
    """

    queryset = UnlockRequest.objects.all()
    serializer_class = UnlockRequestSerializer

    @action(detail=False, methods=["get"])
    @handle_service_exceptions
    def list(self, request):
        """
        Handle GET request to list paginated unlock requests.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing the unlock requests,
                      or an error message if the data retrieval fails.
        """
        return UnlockRequestService.get_paginated_unlock_requests(request)

    @action(detail=False, methods=["post"])
    @handle_service_exceptions
    def create(self, request):
        """
        Handle POST request to create a new unlock request.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: The created unlock request instance,
                      or an error message if the creation fails.
        """
        serializer = UnlockRequestPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selection_id = serializer.validated_data.get("selection")
        message = serializer.validated_data.get("message")

        success, message = UnlockRequestService.create_unlock_request(selection_id, message)

        return build_response(success=success, message=message, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    @handle_service_exceptions
    def accept(self, request, pk=None):
        """
        Handle POST request to accept an unlock request.

        Args:
            request (HttpRequest): The incoming HTTP request.
            pk (int): The primary key of the unlock request to be accepted.

        Returns:
            Response: The updated unlock request instance,
                      or an error message if the update fails.
        """
        success, message = UnlockRequestService.accept_unlock_request(pk)
        return build_response(
            success=success,
            message=message,
            status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["post"])
    @handle_service_exceptions
    def refuse(self, request, pk=None):
        """
        Handle POST request to refuse an unlock request.

        Args:
            request (HttpRequest): The incoming HTTP request.
            pk (int): The primary key of the unlock request to be refused.

        Returns:
            Response: The updated unlock request instance,
                      or an error message if the update fails.
        """
        success, message = UnlockRequestService.refuse_unlock_request(pk)
        return build_response(
            success=success,
            message=message,
            status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST,
        )
