"""
ViewSet module for the ArchitectReport model.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.moderation.controllers.ManageReportingPermission import ManageReportingPermission
from app.moderation.models.ArchitectReport import ArchitectReport
from app.moderation.serializers.ArchitectReportSerializer import ArchitectReportSerializer
from app.moderation.services.ArchitectReportService import ArchitectReportService
from app.core.exception_handler import handle_service_exceptions
from app.core.response_builder import build_response
from rest_framework import status


class ArchitectReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the ArchitectReport model.
    """

    queryset = ArchitectReport.objects.all()
    serializer_class = ArchitectReportSerializer

    def get_permissions(self):
        """
        Get the permissions that the view requires.

        Returns:
            list: List of permission instances.
        """
        if self.action in ["create", "get_reasons"]:
            return [IsAuthenticated()]
        elif self.action in [
            "update",
            "partial_update",
            "destroy",
            "list",
            "retrieve",
            "get_decisions",
            "change_status",
            "execute_decision",
        ]:
            return [IsAuthenticated(), ManageReportingPermission()]
        return super().get_permissions()

    @handle_service_exceptions
    def list(self, request, *args, **kwargs):
        """
        Override the list method to return grouped ArchitectReport objects.
        """
        success,data = ArchitectReportService.get_grouped_architect_reports()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)


    @handle_service_exceptions
    def create(self, request, *args, **kwargs):
        """
        Override the create method to use ArchitectReportService for handling the creation
        of an ArchitectReport.
        """
        success,data = ArchitectReportService.create_architect_report(request)
        return build_response(success=success, data=data, status=status.HTTP_201_CREATED)


    @action(detail=False)
    @handle_service_exceptions
    def get_decisions(self, request):
        """
        Retrieve all possible decisions for the corresponding type.
        """
        success,data = ArchitectReportService.get_decisions()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)


    @action(detail=False)
    @handle_service_exceptions
    def get_reasons(self, request):
        """
        Retrieve all possible reasons for the corresponding type.
        """
        success,data = ArchitectReportService.get_reasons()
        return build_response(success=success, data=data, status=status.HTTP_200_OK)


    @action(detail=True)
    @handle_service_exceptions
    def change_status(self, request, pk=None):
        """
        Change the status of an ArchitectReport.
        """
        success,data = ArchitectReportService.change_architect_report_status(request, pk)
        return build_response(success=success, data=data, status=status.HTTP_200_OK)


    @action(detail=True)
    @handle_service_exceptions
    def execute_decision(self, request):
        """
        Execute a decision on multiple architect reports.

        This method processes the decision for the provided report IDs.
        """
        success,message = ArchitectReportService.execute_decision(request)
        return build_response(success=success, message=message, status=status.HTTP_200_OK)

