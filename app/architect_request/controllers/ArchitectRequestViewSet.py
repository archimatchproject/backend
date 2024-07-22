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
from app.architect_request.serializers.ArchitectRequestRescheduleSerializer import (
    ArchitectRequestRescheduleSerializer,
)
from app.architect_request.serializers.ArchitectRequestSerializer import ArchitectAcceptSerializer
from app.architect_request.serializers.ArchitectRequestSerializer import (
    ArchitectRequestInputSerializer,
)
from app.architect_request.serializers.ArchitectRequestSerializer import ArchitectRequestSerializer
from app.architect_request.services.ArchitectRequestService import ArchitectRequestService
from app.core.pagination import CustomPagination
from app.core.serializers.NoteSerializer import NoteSerializer


class ArchitectRequestViewSet(viewsets.ModelViewSet):
    """
    Viewset for the ArchitectRequest model.

    Provides CRUD operations and additional functionality for ArchitectRequest
    instances.

    Attributes:
        queryset (QuerySet): The queryset of ArchitectRequest instances.
        serializer_class (ArchitectRequestSerializer): The serializer class for
        ArchitectRequest
        instances.
    """

    queryset = ArchitectRequest.objects.all()
    serializer_class = ArchitectRequestSerializer
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
        return ArchitectRequestService.architect_request_paginated(request)

    def get_serializer_class(self):
        """
        Return the serializer class based on the request method.

        Uses ArchitectRequestInputSerializer for POST and PUT requests,
        and ArchitectRequestSerializer for other operations.

        Returns:
            Serializer Class: The appropriate serializer class based on the request method.
        """
        if self.action == "create_architect_request":
            return ArchitectRequestInputSerializer
        elif self.action == "admin_accept":
            return ArchitectAcceptSerializer
        elif self.action == "add_note":
            return NoteSerializer
        elif self.action == "reschedule":
            return ArchitectRequestRescheduleSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return ArchitectRequestInputSerializer
        return ArchitectRequestSerializer

    def get_permissions(self):
        """
        Return the list of permissions that this view requires.

        Applies different permissions based on the action being executed.

        Returns:
            list: The list of permission classes.
        """
        if self.action == "create_architect_request":
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated, ManageArchitectRequestPermission]
        return super().get_permissions()

    @action(detail=False, methods=["POST"], url_path="create-architect-request")
    def create_architect_request(self, request):
        """
        Custom action to create an ArchitectRequest.

        Uses an input serializer to validate data and calls the service to handle the
        creation logic.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            Response: The response object containing the result of the operation.
        """
        return ArchitectRequestService.add_architect_request(request.data)

    @action(
        detail=True,
        methods=["POST"],
        url_path="admin-accept",
        serializer_class=ArchitectAcceptSerializer,
    )
    def admin_accept(self, request, pk=None):
        """
        Custom action to accept an ArchitectRequest and create an Architect instance.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the ArchitectRequest to be accepted.

        Returns:
            Response: The response object containing the result of the operation.
        """
        return ArchitectRequestService.admin_accept_architect_request(pk, request)

    @action(
        detail=True,
        methods=["POST"],
        url_path="admin-refuse",
    )
    def admin_refuse(self, request, pk=None):
        """
        Custom action to refuse an ArchitectRequest.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the ArchitectRequest to be refused.

        Returns:
            Response: The response object containing the result of the operation.
        """
        return ArchitectRequestService.admin_refuse_architect_request(pk)

    @action(
        detail=True,
        methods=["POST"],
        url_path="admin-assign-responsable",
    )
    def admin_assign_responsable(self, request, pk=None):
        """
        Custom action to assign a responsible admin for an ArchitectRequest.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the ArchitectRequest to be updated.

        Returns:
            Response: The response object containing the result of the operation.
        """
        admin_id = request.data.get("admin_id")
        return ArchitectRequestService.admin_assign_responsable(pk, admin_id)

    @action(
        detail=True,
        methods=["POST"],
        url_path="add-note",
        serializer_class=NoteSerializer,
    )
    def add_note(self, request, pk=None):
        """
        Custom action to add a note to an ArchitectRequest.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the ArchitectRequest to which the note will be added.

        Returns:
            Response: The response object containing the result of the operation.
        """
        return ArchitectRequestService.add_note_to_architect_request(pk, request.data)

    @action(detail=False, methods=["GET"], url_path="project-categories")
    def get_project_categories(self, request):
        """
        Retrieve all project categories.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the list of project categories.
        """
        return ArchitectRequestService.get_all_project_categories()

    @action(detail=False, methods=["GET"], url_path="property-types")
    def get_property_types(self, request):
        """
        Retrieve all property types.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the list of property types.
        """
        return ArchitectRequestService.get_all_property_types()

    @action(detail=False, methods=["GET"], url_path="work-types")
    def get_work_types(self, request):
        """
        Retrieve all work types.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the list of work types.
        """
        return ArchitectRequestService.get_all_work_types()

    @action(detail=False, methods=["GET"], url_path="architectural-styles")
    def get_architectural_styles(self, request):
        """
        Retrieve all architectural styles.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the list of architectural styles.
        """
        return ArchitectRequestService.get_all_architectural_styles()

    @action(
        detail=True,
        methods=["PUT"],
        url_path="reschedule-meeting",
        serializer_class=ArchitectRequestRescheduleSerializer,
    )
    def reschedule(self, request, pk=None):
        """
        Custom action to reschedule an ArchitectRequest.

        Args:
            request (Request): The request object containing the input data.
            pk (str): The primary key of the ArchitectRequest to be rescheduled.

        Returns:
            Response: The response object containing the result of the operation.
        """
        return ArchitectRequestService.reschedule_architect_request(pk, request.data)

    @action(detail=False, methods=["GET"], url_path="time-slots")
    def get_time_slots(self, request):
        """
        Retrieve all available time slots.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response object containing the list of time slots.
        """
        return ArchitectRequestService.get_all_time_slots()
