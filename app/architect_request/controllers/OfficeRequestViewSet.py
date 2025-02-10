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
from app.core.serializers.NoteSerializer import NoteSerializer
from app.architect_request.serializers.OfficeRequestRescheduleSerializer import (
    OfficeRequestRescheduleSerializer,
)


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

    def get(self, request):
        """
        Handle GET request and return paginated Realization objects.

        This method retrieves all Realization objects from the database, applies
        pagination based on the parameters in the request, and returns the paginated
        results. If the pagination is not applied correctly, it returns a 400 Bad Request response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Response: A paginated response containing Realization objects or an error message.
        """
        return OfficeRequestService.office_request_paginated(request)

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

    @action(
        detail=True,
        methods=["POST"],
        url_path="office-admin-refuse",
    )
    @handle_service_exceptions
    def office_admin_refuse(self, request, pk=None):
        """
        Custom action to refuse an OfficeRequest.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the OfficeRequest to be refused.

        Returns:
            Response: The response object containing the result of the operation.
        """
        success, data = OfficeRequestService.admin_refuse_office_request(pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["POST"],
        url_path="office-admin-accept",
    )
    @handle_service_exceptions
    def office_admin_accept(self, request, pk=None):
        """
        Custom action to accept an OfficeRequest.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the OfficeRequest to be accepted.

        Returns:
            Response: The response object containing the result of the operation.
        """
        success, data = OfficeRequestService.admin_accept_office_request(pk, request)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["POST"],
        url_path="add-note",
        serializer_class=NoteSerializer,
    )
    @handle_service_exceptions
    def office_add_note(self, request, pk=None):
        """
        Custom action to add a note to an OfficeRequest.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the OfficeRequest to which the note will be added.

        Returns:
            Response: The response object containing the result of the operation.
        """
        success, data = OfficeRequestService.add_note_to_office_request(pk, request.data)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["PUT"],
        url_path="office-reschedule-meeting",
        serializer_class=OfficeRequestRescheduleSerializer,
    )
    @handle_service_exceptions
    def reschedule(self, request, pk=None):
        """
        Custom action to reschedule an OfficeRequest.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the OfficeRequest to be rescheduled.

        Returns:
            Response: The response object containing the result of the operation.
        """
        success, data = OfficeRequestService.reschedule_office_request(pk, request.data)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["POST"],
        url_path="admin-assign-office-responsable",
    )
    @handle_service_exceptions
    def admin_assign_office_responsable(self, request, pk=None):
        """
        Custom action to assign a responsible admin for an OfficeRequest.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the OfficeRequest to be updated.

        Returns:
            Response: The response object containing the result of the operation.
        """
        admin_id = request.data.get("admin_id")
        success, data = OfficeRequestService.admin_assign_office_responsable(pk, admin_id)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)
