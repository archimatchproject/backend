"""
ViewSet module for the OfficeReportArchitect model.
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from app.moderation.controllers.ManageReportingPermission import ManageReportingPermission
from app.moderation.models import OfficeReportArchitect
from app.moderation.serializers import OfficeReportArchitectSerializer
from app.moderation.services.OfficeReportArchitectService import OfficeReportArchitectService


class OfficeReportArchitectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the OfficeReportArchitect model.
    """

    queryset = OfficeReportArchitect.objects.all()
    serializer_class = OfficeReportArchitectSerializer

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        Returns:
            list: List of permission instances.
        """
        if self.action in [
            "update",
            "partial_update",
            "destroy",
            "list",
            "retrieve",
            "change_status",
            "execute_decision",
        ]:
            return [IsAuthenticated(), ManageReportingPermission()]

        elif self.action in ["get_decisions", "get_reasons", "create"]:
            return []
        return super().get_permissions()

    @handle_service_exceptions
    def list(self, request, *args, **kwargs):
        """
        Override the list method to return grouped OfficeReportArchitect objects.
        """
        return OfficeReportArchitectService.get_grouped_office_reports(request)

    @handle_service_exceptions
    def create(self, request, *args, **kwargs):
        """
        Override the create method to use OfficeReportArchitectService for handling the creation
        of an OfficeReportArchitect.
        """
        success, data = OfficeReportArchitectService.create_office_report(request)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)

    @action(detail=False)
    @handle_service_exceptions
    def get_decisions(self, request):
        """
        Retrieve all possible decisions for the corresponding type.
        """
        success, data = OfficeReportArchitectService.get_decisions()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=False)
    @handle_service_exceptions
    def get_reasons(self, request):
        """
        Retrieve all possible reasons for the corresponding type.
        """
        success, data = OfficeReportArchitectService.get_reasons()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=True)
    @handle_service_exceptions
    def change_status(self, request, pk=None):
        """
        Change the status of an OfficeReportArchitect.
        """
        success, data = OfficeReportArchitectService.change_office_report_status(request, pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)

    @action(detail=True)
    @handle_service_exceptions
    def execute_decision(self, request):
        """
        Execute a decision on multiple office reports.

        This method processes the decision for the provided report IDs.
        """
        success, message = OfficeReportArchitectService.execute_decision(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)
